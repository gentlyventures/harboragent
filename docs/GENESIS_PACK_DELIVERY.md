# Genesis Mission Readiness Pack Delivery System

This document describes the secure delivery system for the Harbor Agent — Genesis Mission Readiness Pack, including how to configure environment variables, deploy the Cloudflare Worker, and test the system.

## Architecture Overview

The delivery system consists of:

1. **Cloudflare Worker** (`workers/personalized-download/src/index.ts`)
   - Verifies Stripe checkout sessions
   - Generates secure download links
   - Handles download requests
   - Processes Stripe webhooks
   - Sends email notifications via Postmark

2. **Stripe Integration**
   - Payment processing
   - Session verification
   - Purchase validation
   - Webhook events (`checkout.session.completed`)

3. **Postmark Email Service**
   - Sends download emails automatically after payment
   - Uses confirmed sender signature (`hello@harboragent.dev`)
   - HTML email templates with download links

4. **Download Origin (Cloudflare R2)**
   - R2 bucket hosting the pack ZIP file
   - Public URL serves files after Worker verification

## Environment Variables

### Where Each Key Lives

#### 1. Cloudflare Worker Secrets (via Wrangler)

These secrets are stored in Cloudflare and accessed by the Worker at runtime:

- `STRIPE_SECRET_KEY`: Stripe API secret key (starts with `sk_`)
- `DOWNLOAD_ORIGIN_URL`: URL where pack files are hosted (Cloudflare R2)
  - Current: R2 bucket public URL (e.g., `https://pub-xxxxx.r2.dev/harbor-agent-genesis-pack-v1.0.zip`)
  - See `docs/R2_SETUP.md` for R2 bucket setup
- `POSTMARK_SERVER_TOKEN`: Postmark server token for sending emails
  - Get from: https://account.postmarkapp.com/servers
- `POSTMARK_FROM_EMAIL`: Email address to send from (e.g., `hello@harboragent.dev`)
- `POSTMARK_FROM_NAME`: Display name for sender (e.g., `Harbor Agent`)
- `GENESIS_PACK_PRICE_ID`: (Optional) Stripe Price ID for the product
- `STRIPE_WEBHOOK_SECRET`: (Optional) Stripe webhook signing secret for webhook verification

**How to set Wrangler secrets:**

```bash
# Install Wrangler CLI if not already installed
npm install -g wrangler

# Authenticate with Cloudflare
wrangler login

# Set each secret (you'll be prompted to enter the value)
wrangler secret put STRIPE_SECRET_KEY
wrangler secret put DOWNLOAD_ORIGIN_URL
wrangler secret put POSTMARK_SERVER_TOKEN
wrangler secret put POSTMARK_FROM_EMAIL
wrangler secret put POSTMARK_FROM_NAME
wrangler secret put GENESIS_PACK_PRICE_ID  # Optional
wrangler secret put STRIPE_WEBHOOK_SECRET  # Optional (for webhook signature verification)
```

**Note:** Secrets set via `wrangler secret put` are encrypted and stored securely in Cloudflare. They are NOT visible in `wrangler.toml` or in your code.

#### 2. GitHub Actions Secrets

These are used by CI/CD workflows to deploy the Worker:

- `CLOUDFLARE_ACCOUNT_ID`: Your Cloudflare account ID
- `CLOUDFLARE_API_TOKEN`: API token with Workers permissions (see setup guide below)
- `STRIPE_SECRET_KEY`: Same as Worker secret (for deployment)
- `DOWNLOAD_ORIGIN_URL`: Same as Worker secret (for deployment)
- `GENESIS_PACK_PRICE_ID`: Same as Worker secret (for deployment)

**How to set GitHub secrets:**

1. Go to your repository on GitHub
2. Navigate to: **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret with its name and value

**Important:** GitHub Actions secrets are used during deployment but are NOT passed to the Worker at runtime. The Worker reads its secrets from Cloudflare's secure storage.

**Cloudflare API Token Setup:**

For detailed instructions on creating the `CLOUDFLARE_API_TOKEN` with the correct permissions and IP filtering, see: `docs/CLOUDFLARE_API_TOKEN_SETUP.md`

#### 3. Local Development (.env file)

For local testing and development scripts:

- Copy `.env.example` to `.env`
- Fill in values for local testing
- The `.env` file is gitignored and never committed

**How to use .env locally:**

```bash
# Node.js scripts (using dotenv)
npm install dotenv
# Then in your script:
require('dotenv').config();

# Python scripts (using python-dotenv)
pip install python-dotenv
# Then in your script:
from dotenv import load_dotenv
load_dotenv()
```

## Worker Configuration

### wrangler.toml

The `wrangler.toml` file contains Worker configuration:

```toml
name = "harboragent-personalized-download"
account_id = "TODO"  # Set your Cloudflare account ID
```

**Required setup steps:**

1. **Set account_id:**
   - Get your account ID from: https://dash.cloudflare.com/
   - Look in the right sidebar
   - Replace `TODO` in `wrangler.toml`

2. **Configure routes (optional):**
   - For custom domain: Add route configuration
   - For workers.dev: No route needed (uses default subdomain)

3. **Secrets:** Set via `wrangler secret put` (not in toml file)

## Testing the Worker Locally

### Using Wrangler Dev

```bash
# Install Wrangler
npm install -g wrangler

# Authenticate
wrangler login

# Set secrets for local dev (optional, uses .env if available)
wrangler secret put STRIPE_SECRET_KEY --env dev

# Run local dev server
wrangler dev
```

The Worker will be available at `http://localhost:8787`

### Testing Endpoints

```bash
# Health check
curl http://localhost:8787/health

# Verify session (POST)
curl -X POST http://localhost:8787/verify-session \
  -H "Content-Type: application/json" \
  -d '{"session_id": "cs_test_..."}'

# Download (GET)
curl "http://localhost:8787/download?session_id=cs_test_..."
```

## Deployment

### Manual Deployment

```bash
wrangler deploy
```

### Automated Deployment

GitHub Actions automatically deploys when:
- Code is pushed to `main` branch
- Changes are made to `workers/` or `wrangler.toml`

See `.github/workflows/deploy-worker.yml` for details.

## Stripe Webhook Configuration

To enable automatic email delivery after payment, configure a Stripe webhook:

### 1. Create Webhook Endpoint in Stripe

1. Go to: https://dashboard.stripe.com/webhooks
2. Click **Add endpoint**
3. Set **Endpoint URL** to: `https://download.harboragent.dev/webhook`
4. Select events to listen to:
   - `checkout.session.completed`
5. Click **Add endpoint**

### 2. Get Webhook Signing Secret

1. After creating the endpoint, click on it
2. Find **Signing secret** (starts with `whsec_`)
3. Copy the secret

### 3. Set Webhook Secret in Worker

```bash
wrangler secret put STRIPE_WEBHOOK_SECRET
# Paste the signing secret from Stripe
```

### 4. Test the Webhook

After configuration, test a purchase:
1. Complete a test checkout in Stripe
2. Check Stripe webhook logs for successful delivery
3. Verify email is sent to customer
4. Check Worker logs: `wrangler tail`

**Note:** The webhook handler will automatically send a download email to the customer when `checkout.session.completed` is received and payment is successful.

## Security Best Practices

1. **Never commit secrets:**
   - `.env` is gitignored
   - Secrets are stored in Cloudflare, not in code
   - GitHub secrets are encrypted

2. **No logging of secrets:**
   - Worker code never logs `env.STRIPE_SECRET_KEY`
   - No console.log of sensitive data
   - Error messages don't expose secrets

3. **Session verification:**
   - All downloads require valid Stripe session
   - Sessions are verified via Stripe API
   - Expired or invalid sessions are rejected

4. **HTTPS only:**
   - Worker only serves over HTTPS
   - Download origin should use HTTPS

## Troubleshooting

### Worker can't access secrets

- Verify secrets are set: `wrangler secret list`
- Ensure you're using the correct environment
- Check that secrets are set for production, not just dev

### Stripe verification fails

- Verify `STRIPE_SECRET_KEY` is correct
- Check that session ID is valid
- Ensure session is completed and paid

### Download redirect fails

- Verify `DOWNLOAD_ORIGIN_URL` is correct
- Check that origin URL is accessible
- Ensure origin accepts the session_id parameter

## Support

For issues or questions:
- Check Cloudflare Workers logs: `wrangler tail`
- Review Stripe dashboard for session status
- Check GitHub Actions logs for deployment issues

