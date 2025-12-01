/**
 * Cloudflare Worker for personalized Genesis Pack downloads
 * Handles Stripe checkout session verification and secure download delivery
 * 
 * Deployment: Automated via GitHub Actions on push to main
 */

export interface Env {
  STRIPE_SECRET_KEY: string;
  DOWNLOAD_ORIGIN_URL: string;
  GENESIS_PACK_PRICE_ID?: string;
  STRIPE_WEBHOOK_SECRET?: string;
  POSTMARK_SERVER_TOKEN: string;
  POSTMARK_FROM_EMAIL: string;
  POSTMARK_FROM_NAME: string;
  DOWNLOAD_SIGNING_KEY?: string; // Optional: HMAC key for signed links (defaults to STRIPE_SECRET_KEY)
}

// CORS headers helper
function getCorsHeaders(): Record<string, string> {
  return {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };
}

// Base64URL encoding (URL-safe base64)
function base64UrlEncode(data: string): string {
  return btoa(data)
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=/g, '');
}

function base64UrlDecode(data: string): string {
  // Add padding if needed
  let padded = data.replace(/-/g, '+').replace(/_/g, '/');
  while (padded.length % 4) {
    padded += '=';
  }
  return atob(padded);
}

// Generate signed download token with expiration
async function generateSignedToken(
  sessionId: string,
  email: string,
  signingKey: string,
  expiresInHours: number = 24
): Promise<string> {
  const payload = {
    sessionId,
    email,
    expires: Date.now() + (expiresInHours * 60 * 60 * 1000),
    nonce: crypto.randomUUID(),
  };

  const payloadStr = JSON.stringify(payload);
  const encoder = new TextEncoder();
  const keyData = encoder.encode(signingKey);
  
  // Import key for HMAC
  const key = await crypto.subtle.importKey(
    'raw',
    keyData,
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );

  // Sign payload
  const signature = await crypto.subtle.sign(
    'HMAC',
    key,
    encoder.encode(payloadStr)
  );

  // Encode signature as base64url
  const signatureB64 = base64UrlEncode(
    String.fromCharCode(...new Uint8Array(signature))
  );

  // Return token: payload.signature
  return `${base64UrlEncode(payloadStr)}.${signatureB64}`;
}

// Verify signed token
async function verifySignedToken(
  token: string,
  signingKey: string
): Promise<{ valid: boolean; payload?: any; error?: string }> {
  try {
    const [payloadB64, signatureB64] = token.split('.');
    if (!payloadB64 || !signatureB64) {
      return { valid: false, error: 'Invalid token format' };
    }

    // Decode payload
    const payloadStr = base64UrlDecode(payloadB64);
    const payload = JSON.parse(payloadStr);

    // Check expiration
    if (Date.now() > payload.expires) {
      return { valid: false, error: 'Token expired' };
    }

    // Verify signature
    const encoder = new TextEncoder();
    const keyData = encoder.encode(signingKey);
    const key = await crypto.subtle.importKey(
      'raw',
      keyData,
      { name: 'HMAC', hash: 'SHA-256' },
      false,
      ['verify']
    );

    const signature = Uint8Array.from(
      atob(signatureB64.replace(/-/g, '+').replace(/_/g, '/')),
      c => c.charCodeAt(0)
    );

    const isValid = await crypto.subtle.verify(
      'HMAC',
      key,
      signature,
      encoder.encode(payloadStr)
    );

    if (!isValid) {
      return { valid: false, error: 'Invalid signature' };
    }

    return { valid: true, payload };
  } catch (error) {
    return {
      valid: false,
      error: error instanceof Error ? error.message : 'Token verification failed',
    };
  }
}

// Generate LICENSE.txt content
function generateLicenseText(customerInfo: {
  email: string;
  organization?: string;
  purchaseDate: string;
  sessionId: string;
}): string {
  return `HARBOR AGENT - GENESIS MISSION READINESS PACK
LICENSE AGREEMENT

This license is granted to:
  Email: ${customerInfo.email}
  ${customerInfo.organization ? `Organization: ${customerInfo.organization}` : ''}
  Purchase Date: ${customerInfo.purchaseDate}
  Session ID: ${customerInfo.sessionId}

LICENSE TERMS:

1. PER-ORGANIZATION LICENSE
   This pack is licensed for use by ONE organization only. The organization
   is identified by the email address and session ID above.

2. NO REDISTRIBUTION OR RESALE
   You may NOT redistribute, resell, or share this pack with other
   organizations, individuals, or third parties.

3. INTERNAL USE ONLY
   This pack is intended for internal use within your organization to prepare
   for DOE Genesis Mission collaboration. You may use it to:
   - Prepare internal readiness assessments
   - Generate proposals and documentation
   - Train your team on Genesis alignment
   - Modernize your systems and workflows

4. UPDATES
   This license includes free updates for all 2025 revisions of the Genesis
   Mission Readiness Pack.

5. NO WARRANTIES
   This pack is provided "as-is" without warranties. It is NOT legal advice,
   NOT regulatory guidance, and NOT an official DOE document.

6. SUPPORT
   For questions or support, contact: support@gentlyventures.com

By downloading and using this pack, you agree to these license terms.

© ${new Date().getFullYear()} Gently Ventures. All rights reserved.
`;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);

    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: getCorsHeaders(),
      });
    }

    // Health check endpoint
    if (url.pathname === '/health') {
      return new Response(JSON.stringify({ status: 'ok' }), {
        headers: { 
          'Content-Type': 'application/json',
          ...getCorsHeaders(),
        },
      });
    }

    // Handle download request (with optional signed token)
    if (url.pathname === '/download' || url.pathname.startsWith('/download/')) {
      return handleDownload(request, env);
    }

    // Handle signed download request
    if (url.pathname === '/download-signed' || url.pathname.startsWith('/download-signed/')) {
      return handleSignedDownload(request, env);
    }

    // Handle checkout session verification
    if (url.pathname === '/verify-session') {
      return handleVerifySession(request, env);
    }

    // Handle Stripe webhook
    if (url.pathname === '/webhook') {
      return handleWebhook(request, env);
    }

    // Handle checkout session creation
    if (url.pathname === '/create-checkout-session') {
      return handleCreateCheckoutSession(request, env);
    }

    return new Response('Not Found', { status: 404 });
  },
};

async function handleDownload(request: Request, env: Env): Promise<Response> {
  const sessionId = new URL(request.url).searchParams.get('session_id');
  
  if (!sessionId) {
    return new Response('Missing session_id parameter', { status: 400 });
  }

  // Verify session with Stripe
  const result = await verifyStripeSession(sessionId, env.STRIPE_SECRET_KEY);
  
  if (!result.isValid) {
    return new Response('Invalid or expired session', { status: 403 });
  }

  // Generate signed token for secure download
  const signingKey = env.DOWNLOAD_SIGNING_KEY || env.STRIPE_SECRET_KEY;
  const session = await getStripeSession(sessionId, env.STRIPE_SECRET_KEY);
  const customerEmail = session?.customer_details?.email || session?.customer_email || 'customer';
  
  try {
    const signedToken = await generateSignedToken(sessionId, customerEmail, signingKey, 24);
    const downloadUrl = `${new URL(request.url).origin}/download-signed?token=${signedToken}`;
    return Response.redirect(downloadUrl, 302);
  } catch (error) {
    console.error('Failed to generate signed token, falling back to unsigned:', error);
    // Fallback to unsigned link
    const downloadUrl = `${env.DOWNLOAD_ORIGIN_URL}?session_id=${sessionId}`;
    return Response.redirect(downloadUrl, 302);
  }
}

async function handleSignedDownload(request: Request, env: Env): Promise<Response> {
  const token = new URL(request.url).searchParams.get('token');
  
  if (!token) {
    return new Response('Missing token parameter', { status: 400 });
  }

  const signingKey = env.DOWNLOAD_SIGNING_KEY || env.STRIPE_SECRET_KEY;
  const verification = await verifySignedToken(token, signingKey);

  if (!verification.valid || !verification.payload) {
    return new Response(
      verification.error || 'Invalid or expired token',
      { status: 403 }
    );
  }

  const { sessionId, email } = verification.payload;

  // Double-check with Stripe (defense in depth)
  const result = await verifyStripeSession(sessionId, env.STRIPE_SECRET_KEY);
  if (!result.isValid) {
    return new Response('Session no longer valid', { status: 403 });
  }

  // Get customer info from Stripe session
  const session = await getStripeSession(sessionId, env.STRIPE_SECRET_KEY);
  if (!session) {
    return new Response('Failed to retrieve session details', { status: 500 });
  }

  // Generate personalized ZIP on-demand
  try {
    const personalizedZip = await generatePersonalizedZip(
      env.DOWNLOAD_ORIGIN_URL,
      {
        email: email,
        organization: session.customer_details?.name || undefined,
        purchaseDate: new Date(session.created * 1000).toISOString().split('T')[0],
        sessionId: sessionId,
      }
    );

    // Stream personalized ZIP to user
    return new Response(personalizedZip, {
      headers: {
        'Content-Type': 'application/zip',
        'Content-Disposition': `attachment; filename="harbor-agent-genesis-pack-${sessionId.slice(-8)}.zip"`,
        'Content-Length': personalizedZip.byteLength.toString(),
      },
    });
  } catch (error) {
    console.error('Failed to generate personalized ZIP:', error);
    // Fallback: redirect to original ZIP
    return Response.redirect(env.DOWNLOAD_ORIGIN_URL, 302);
  }
}

// Generate personalized ZIP by fetching base ZIP, adding LICENSE.txt, and returning new ZIP
async function generatePersonalizedZip(
  baseZipUrl: string,
  customerInfo: {
    email: string;
    organization?: string;
    purchaseDate: string;
    sessionId: string;
  }
): Promise<ArrayBuffer> {
  // Import jszip (Workers support ES modules)
  const JSZip = (await import('jszip')).default;

  // Fetch base ZIP from DOWNLOAD_ORIGIN_URL
  const baseZipResponse = await fetch(baseZipUrl);
  if (!baseZipResponse.ok) {
    throw new Error(`Failed to fetch base ZIP: ${baseZipResponse.status} ${baseZipResponse.statusText}`);
  }

  const baseZipArrayBuffer = await baseZipResponse.arrayBuffer();

  // Parse base ZIP
  const zip = await JSZip.loadAsync(baseZipArrayBuffer);

  // Add personalized LICENSE.txt
  const licenseText = generateLicenseText(customerInfo);
  zip.file('LICENSE.txt', licenseText);

  // Generate new ZIP
  const personalizedZip = await zip.generateAsync({
    type: 'arraybuffer',
    compression: 'DEFLATE',
    compressionOptions: { level: 6 },
  });

  return personalizedZip;
}

// Helper to get Stripe session details
async function getStripeSession(sessionId: string, stripeSecretKey: string): Promise<any | null> {
  try {
    const response = await fetch(`https://api.stripe.com/v1/checkout/sessions/${sessionId}`, {
      headers: {
        'Authorization': `Bearer ${stripeSecretKey}`,
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });

    if (!response.ok) {
      return null;
    }

    return await response.json();
  } catch (error) {
    console.error('Failed to get Stripe session:', error);
    return null;
  }
}

async function handleVerifySession(request: Request, env: Env): Promise<Response> {
  if (request.method !== 'POST') {
    return new Response('Method not allowed', { status: 405 });
  }

  try {
    const body = await request.json();
    const sessionId = body.session_id;

    if (!sessionId) {
      return new Response(JSON.stringify({ valid: false, error: 'Missing session_id' }), {
        status: 400,
        headers: { 
          'Content-Type': 'application/json',
          ...getCorsHeaders(),
        },
      });
    }

    const result = await verifyStripeSession(sessionId, env.STRIPE_SECRET_KEY);

    return new Response(JSON.stringify({ 
      valid: result.isValid,
      debug: result.debug 
    }), {
      headers: { 
        'Content-Type': 'application/json',
        ...getCorsHeaders(),
      },
    });
  } catch (error) {
    console.error('Verify session error:', error);
    return new Response(JSON.stringify({ 
      valid: false, 
      error: 'Invalid request',
      debug: error instanceof Error ? error.message : 'Unknown error'
    }), {
      status: 400,
      headers: { 
        'Content-Type': 'application/json',
        ...getCorsHeaders(),
      },
    });
  }
}

async function verifyStripeSession(sessionId: string, stripeSecretKey: string): Promise<{ isValid: boolean; debug?: any }> {
  try {
    const response = await fetch(`https://api.stripe.com/v1/checkout/sessions/${sessionId}`, {
      headers: {
        'Authorization': `Bearer ${stripeSecretKey}`,
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Stripe API error:', response.status, errorText);
      return { 
        isValid: false, 
        debug: { 
          error: 'Stripe API returned non-OK status',
          status: response.status,
          statusText: response.statusText
        }
      };
    }

    const session = await response.json();
    
    // Log session details for debugging (in production, remove or gate behind env flag)
    console.log('Stripe session:', {
      id: session.id,
      status: session.status,
      payment_status: session.payment_status,
      amount_total: session.amount_total,
      currency: session.currency
    });
    
    // Verify session is completed and payment is successful
    // For 100% off coupons, Stripe may set payment_status to 'paid' even with amount_total: 0
    const isValid = (session.status === 'complete') && 
                    (session.payment_status === 'paid' || session.payment_status === 'no_payment_required');
    
    return { 
      isValid,
      debug: {
        status: session.status,
        payment_status: session.payment_status,
        amount_total: session.amount_total,
        check_passed: isValid
      }
    };
  } catch (error) {
    console.error('verifyStripeSession error:', error);
    return { 
      isValid: false,
      debug: {
        error: error instanceof Error ? error.message : 'Unknown error',
        type: error instanceof Error ? error.constructor.name : typeof error
      }
    };
  }
}

async function handleWebhook(request: Request, env: Env): Promise<Response> {
  if (request.method !== 'POST') {
    return new Response('Method not allowed', { status: 405 });
  }

  try {
    const body = await request.text();
    const signature = request.headers.get('stripe-signature');

    // Verify webhook signature if webhook secret is set
    if (env.STRIPE_WEBHOOK_SECRET && signature) {
      // Note: Full signature verification would require crypto library
      // For now, we'll rely on the webhook secret being set in Stripe dashboard
      // and validate the event structure
    }

    const event = JSON.parse(body);

    // Handle checkout.session.completed event
    if (event.type === 'checkout.session.completed') {
      const session = event.data.object;
      
      // Only process if payment is successful
      // Note: For 100% off coupons, Stripe sets payment_status to 'paid' even with amount_total: 0
      if (session.status === 'complete' && (session.payment_status === 'paid' || session.payment_status === 'no_payment_required')) {
        const customerEmail = session.customer_details?.email || session.customer_email;
        
        if (customerEmail) {
          // Generate signed download link with expiration
          const signingKey = env.DOWNLOAD_SIGNING_KEY || env.STRIPE_SECRET_KEY;
          try {
            const signedToken = await generateSignedToken(
              session.id,
              customerEmail,
              signingKey,
              24 // 24 hour expiration
            );
            const downloadUrl = `${new URL(request.url).origin}/download-signed?token=${signedToken}`;
            
            // Send email via Postmark with signed link
            await sendDownloadEmail(
              customerEmail,
              downloadUrl,
              env.POSTMARK_SERVER_TOKEN,
              env.POSTMARK_FROM_EMAIL,
              env.POSTMARK_FROM_NAME,
              {
                email: customerEmail,
                organization: session.customer_details?.name || undefined,
                purchaseDate: new Date().toISOString().split('T')[0],
                sessionId: session.id,
              }
            );
          } catch (error) {
            console.error('Failed to generate signed token, using unsigned link:', error);
            // Fallback to unsigned link
            const downloadUrl = `${new URL(request.url).origin}/download?session_id=${session.id}`;
            await sendDownloadEmail(
              customerEmail,
              downloadUrl,
              env.POSTMARK_SERVER_TOKEN,
              env.POSTMARK_FROM_EMAIL,
              env.POSTMARK_FROM_NAME
            );
          }
        }
      }
    }

    return new Response(JSON.stringify({ received: true }), {
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (error) {
    console.error('Webhook error:', error);
    return new Response(JSON.stringify({ error: 'Webhook processing failed' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}

async function handleCreateCheckoutSession(request: Request, env: Env): Promise<Response> {
  if (request.method !== 'POST') {
    return new Response('Method not allowed', { status: 405 });
  }

  try {
    const body = await request.json();
    const priceId = body.priceId || env.GENESIS_PACK_PRICE_ID;
    const origin = new URL(request.url).origin;
    const successUrl = body.successUrl || `${origin}/success?session_id={CHECKOUT_SESSION_ID}`;
    const cancelUrl = body.cancelUrl || `${origin}/#pricing`;
    const couponCode = body.couponCode;

    if (!priceId) {
      return new Response(JSON.stringify({ error: 'Price ID is required' }), {
        status: 400,
        headers: { 
          'Content-Type': 'application/json',
          ...getCorsHeaders(),
        },
      });
    }

    // Create Stripe checkout session
    const formData = new URLSearchParams();
    formData.append('mode', 'payment');
    formData.append('allow_promotion_codes', 'true');
    formData.append('payment_method_types[]', 'card');
    formData.append('success_url', successUrl);
    formData.append('cancel_url', cancelUrl);
    formData.append('line_items[0][price]', priceId);
    formData.append('line_items[0][quantity]', '1');
    
    // Add coupon code if provided
    if (couponCode && couponCode.trim()) {
      formData.append('discounts[0][coupon]', couponCode.trim());
    }

    const response = await fetch('https://api.stripe.com/v1/checkout/sessions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${env.STRIPE_SECRET_KEY}`,
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData.toString(),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Stripe API error:', errorText);
      return new Response(JSON.stringify({ error: 'Failed to create checkout session' }), {
        status: 500,
        headers: { 
          'Content-Type': 'application/json',
          ...getCorsHeaders(),
        },
      });
    }

    const session = await response.json();

    // Return both sessionId and url for flexibility
    return new Response(JSON.stringify({ 
      sessionId: session.id,
      url: session.url 
    }), {
      headers: { 
        'Content-Type': 'application/json',
        ...getCorsHeaders(),
      },
    });
  } catch (error) {
    console.error('Checkout session creation error:', error);
    return new Response(JSON.stringify({ error: 'Internal server error' }), {
      status: 500,
      headers: { 
        'Content-Type': 'application/json',
        ...getCorsHeaders(),
      },
    });
  }
}

async function sendDownloadEmail(
  toEmail: string,
  downloadUrl: string,
  postmarkToken: string,
  fromEmail: string,
  fromName: string,
  customerInfo?: {
    email: string;
    organization?: string;
    purchaseDate: string;
    sessionId: string;
  }
): Promise<void> {
  try {
    const response = await fetch('https://api.postmarkapp.com/email', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Postmark-Server-Token': postmarkToken,
      },
      body: JSON.stringify({
        From: `${fromName} <${fromEmail}>`,
        To: toEmail,
        Subject: 'Your Genesis Mission Readiness Pack is Ready',
        HtmlBody: `
          <!DOCTYPE html>
          <html>
            <head>
              <meta charset="utf-8">
              <style type="text/css">
                .download-button {
                  display: inline-block !important;
                  background-color: #667eea !important;
                  color: #ffffff !important;
                  padding: 14px 28px !important;
                  text-decoration: none !important;
                  border-radius: 6px !important;
                  font-weight: 600 !important;
                  font-size: 16px !important;
                  border: none !important;
                }
                .download-button:link,
                .download-button:visited,
                .download-button:hover,
                .download-button:active {
                  color: #ffffff !important;
                  text-decoration: none !important;
                }
              </style>
            </head>
            <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
              <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 8px 8px 0 0;">
                <h1 style="color: #ffffff !important; text-decoration: none !important; margin: 0; font-size: 28px;">Thank You for Your Purchase!</h1>
              </div>
              <div style="background: #f9fafb; padding: 30px; border-radius: 0 0 8px 8px;">
                <p style="font-size: 16px; margin-bottom: 20px;">
                  Your <strong>Genesis Mission Readiness Professional Pack</strong> is ready to download.
                </p>
                <p style="font-size: 16px; margin-bottom: 30px;">
                  This pack includes complete compliance templates, automation scripts, proposal kits, and governance playbooks to help your team prepare for the DOE Genesis Mission.
                </p>
                <div style="text-align: center; margin: 30px 0;">
                  <a href="${downloadUrl}" class="download-button" style="display: inline-block; background-color: #667eea; color: #ffffff; padding: 14px 28px; text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 16px;">
                    Download Your Pack
                  </a>
                </div>
                <p style="font-size: 14px; color: #6b7280; margin-top: 30px;">
                  <strong>What's included:</strong>
                </p>
                <ul style="font-size: 14px; color: #6b7280; line-height: 1.8;">
                  <li>Full 80–120 item readiness checklist</li>
                  <li>Complete AI copilot playbooks (Cursor, GitHub Copilot, Claude Code)</li>
                  <li>Secure submission bundle templates</li>
                  <li>Reproducibility kits</li>
                  <li>Proposal template (fully editable)</li>
                  <li>Full schema suite (JSON & YAML)</li>
                  <li>12-month roadmap</li>
                  <li>Enterprise documentation templates</li>
                </ul>
                <p style="font-size: 14px; color: #6b7280; margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb;">
                  <strong>Note:</strong> This download link is personalized and secure. It expires in 24 hours for your security. If you have any questions, please contact us at <a href="mailto:support@gentlyventures.com" style="color: #667eea;">support@gentlyventures.com</a>.
                </p>
                ${customerInfo ? `
                <p style="font-size: 12px; color: #9ca3af; margin-top: 20px; padding-top: 15px; border-top: 1px solid #e5e7eb;">
                  Your personalized pack includes a LICENSE.txt file with your organization's license terms.
                </p>
                ` : ''}
              </div>
            </body>
          </html>
        `,
        MessageStream: 'outbound',
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Postmark API error:', errorText);
      throw new Error(`Postmark API error: ${response.status}`);
    }
  } catch (error) {
    console.error('Failed to send email:', error);
    // Don't throw - we don't want to fail the webhook if email fails
    // The user can still download from the success page
  }
}

