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

