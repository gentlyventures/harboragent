# Manual Worker Deployment Guide

Since GitHub Actions requires payment, here's how to deploy manually:

## Option 1: Create New API Token (No IP Restrictions)

1. Go to: https://dash.cloudflare.com/ → My Profile → API Tokens
2. Create a new token (or edit existing one)
3. **Remove IP restrictions** (or add your local IP)
4. Use this token locally in `.env` instead of the GitHub Actions one

## Option 2: Use OAuth (Recommended)

1. **Remove API token from environment:**
   ```bash
   # Don't source .env file, or comment out CLOUDFLARE_API_TOKEN
   ```

2. **Login with OAuth:**
   ```bash
   wrangler login
   # This opens browser - complete authentication
   ```

3. **Set Worker secrets:**
   ```bash
   wrangler secret put STRIPE_SECRET_KEY
   # Paste your Stripe secret key
   
   wrangler secret put DOWNLOAD_ORIGIN_URL
   # Paste: https://github.com/gentlyventures/harboragent/releases/download/v1.0.0/harbor-agent-genesis-pack-v1.0.zip
   ```

4. **Deploy:**
   ```bash
   wrangler deploy
   ```

## Option 3: Set Secrets via Cloudflare Dashboard

1. Go to: https://dash.cloudflare.com/ → Workers & Pages
2. Find your Worker: `harboragent-personalized-download`
3. Go to **Settings** → **Variables and Secrets**
4. Add secrets:
   - `STRIPE_SECRET_KEY`: Your Stripe key
   - `DOWNLOAD_ORIGIN_URL`: `https://github.com/gentlyventures/harboragent/releases/download/v1.0.0/harbor-agent-genesis-pack-v1.0.zip`
5. Deploy via dashboard or `wrangler deploy`

## Current Status

✅ **GitHub Release created:** v1.0.0 with pack file  
✅ **Worker code ready:** `workers/personalized-download/src/index.ts`  
✅ **Configuration ready:** `wrangler.toml`  
⏳ **Need to deploy:** Worker to Cloudflare  

Once deployed, the Worker will be available at:
- `https://harboragent-personalized-download.YOUR_SUBDOMAIN.workers.dev`

## Quick Deploy Command

Once authenticated (OAuth or new token):

```bash
# Set secrets
echo "your_stripe_key" | wrangler secret put STRIPE_SECRET_KEY
echo "https://github.com/gentlyventures/harboragent/releases/download/v1.0.0/harbor-agent-genesis-pack-v1.0.zip" | wrangler secret put DOWNLOAD_ORIGIN_URL

# Deploy
wrangler deploy
```

That's it! The Worker will verify Stripe payments and redirect to GitHub Releases for download.

