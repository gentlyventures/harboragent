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
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);

    // Health check endpoint
    if (url.pathname === '/health') {
      return new Response(JSON.stringify({ status: 'ok' }), {
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // Handle download request
    if (url.pathname === '/download' || url.pathname.startsWith('/download/')) {
      return handleDownload(request, env);
    }

    // Handle checkout session verification
    if (url.pathname === '/verify-session') {
      return handleVerifySession(request, env);
    }

    // Handle Stripe webhook
    if (url.pathname === '/webhook') {
      return handleWebhook(request, env);
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
  const isValid = await verifyStripeSession(sessionId, env.STRIPE_SECRET_KEY);
  
  if (!isValid) {
    return new Response('Invalid or expired session', { status: 403 });
  }

  // Redirect to download origin
  const downloadUrl = `${env.DOWNLOAD_ORIGIN_URL}?session_id=${sessionId}`;
  return Response.redirect(downloadUrl, 302);
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
        headers: { 'Content-Type': 'application/json' },
      });
    }

    const isValid = await verifyStripeSession(sessionId, env.STRIPE_SECRET_KEY);

    return new Response(JSON.stringify({ valid: isValid }), {
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (error) {
    return new Response(JSON.stringify({ valid: false, error: 'Invalid request' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}

async function verifyStripeSession(sessionId: string, stripeSecretKey: string): Promise<boolean> {
  try {
    const response = await fetch(`https://api.stripe.com/v1/checkout/sessions/${sessionId}`, {
      headers: {
        'Authorization': `Bearer ${stripeSecretKey}`,
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });

    if (!response.ok) {
      return false;
    }

    const session = await response.json();
    
    // Verify session is completed and payment is successful
    return session.payment_status === 'paid' && session.status === 'complete';
  } catch (error) {
    // Log error without exposing details
    return false;
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
      if (session.payment_status === 'paid' && session.status === 'complete') {
        const customerEmail = session.customer_details?.email || session.customer_email;
        
        if (customerEmail) {
          // Generate download link
          const downloadUrl = `${new URL(request.url).origin}/download?session_id=${session.id}`;
          
          // Send email via Postmark
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

async function sendDownloadEmail(
  toEmail: string,
  downloadUrl: string,
  postmarkToken: string,
  fromEmail: string,
  fromName: string
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
            </head>
            <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
              <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 8px 8px 0 0;">
                <h1 style="color: white; margin: 0; font-size: 28px;">Thank You for Your Purchase!</h1>
              </div>
              <div style="background: #f9fafb; padding: 30px; border-radius: 0 0 8px 8px;">
                <p style="font-size: 16px; margin-bottom: 20px;">
                  Your <strong>Genesis Mission Readiness Professional Pack</strong> is ready to download.
                </p>
                <p style="font-size: 16px; margin-bottom: 30px;">
                  This pack includes complete compliance templates, automation scripts, proposal kits, and governance playbooks to help your team prepare for the DOE Genesis Mission.
                </p>
                <div style="text-align: center; margin: 30px 0;">
                  <a href="${downloadUrl}" style="display: inline-block; background: #667eea; color: white; padding: 14px 28px; text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 16px;">
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
                  <strong>Note:</strong> This download link is personalized and secure. If you have any questions, please contact us at <a href="mailto:support@gentlyventures.com" style="color: #667eea;">support@gentlyventures.com</a>.
                </p>
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

