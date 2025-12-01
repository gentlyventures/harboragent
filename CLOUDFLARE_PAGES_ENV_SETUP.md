# Cloudflare Pages Environment Variables Setup

**Required for:** Frontend build to include Stripe configuration

## Environment Variables Needed

These need to be set in Cloudflare Pages for the build process:

1. **VITE_STRIPE_PUBLISHABLE_KEY**
   - Value: `pk_live_...` (Your Stripe publishable key)
   - Purpose: Stripe publishable key for client-side checkout
   - Get from: https://dashboard.stripe.com/apikeys

2. **VITE_STRIPE_PRICE_ID**
   - Value: `price_...` (Your Stripe price ID for $199 product)
   - Purpose: Stripe price ID for $199 one-time purchase
   - Get from: Stripe Dashboard → Products → Your $199 product

3. **VITE_WORKER_URL** (optional, has default)
   - Value: `https://download.harboragent.dev`
   - Purpose: Worker endpoint URL for checkout session creation

## How to Set in Cloudflare Pages Dashboard

1. Go to: https://dash.cloudflare.com/
2. Navigate to: **Workers & Pages** → **harbor-agent** project
3. Click **Settings** tab
4. Scroll to **Environment variables** section
5. Click **Add variable** for each:
   - Name: `VITE_STRIPE_PUBLISHABLE_KEY`
     Value: `pk_live_...` (Your actual publishable key from Stripe)
   - Name: `VITE_STRIPE_PRICE_ID`
     Value: `price_...` (Your actual price ID from Stripe)
   - Name: `VITE_WORKER_URL` (optional)
     Value: `https://download.harboragent.dev`
6. Select **Production** environment (or both Production and Preview)
7. Click **Save**

## Alternative: Set via Cloudflare API

```bash
# Get your Cloudflare API token
# Then set environment variables:

curl -X PUT "https://api.cloudflare.com/client/v4/accounts/1e3a745b2bf8490fc60ea23c480dc530/pages/projects/harbor-agent" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "deployment_configs": {
      "production": {
        "env_vars": {
          "VITE_STRIPE_PUBLISHABLE_KEY": {
            "value": "pk_live_YOUR_ACTUAL_KEY_HERE"
          },
          "VITE_STRIPE_PRICE_ID": {
            "value": "price_YOUR_ACTUAL_PRICE_ID_HERE"
          },
          "VITE_WORKER_URL": {
            "value": "https://download.harboragent.dev"
          }
        }
      }
    }
  }'
```

## Current Status

✅ **Stripe Configuration:**
- Price ID: Created in Stripe (check Stripe Dashboard)
- Amount: $199.00 USD
- Type: One-time payment
- Product: Genesis Mission Readiness Pack

✅ **Publishable Key:**
- Key: Set in Cloudflare Pages environment variables
- Mode: Live (production)
- Note: Publishable keys are safe to expose in client-side code

✅ **Local Build:**
- Environment variables set in `.env`
- Build completed successfully
- Site deployed with embedded keys

⚠️ **For Automatic Builds:**
- Environment variables need to be set in Cloudflare Pages dashboard
- This ensures future builds (via GitHub integration) include the keys

## Verification

After setting environment variables, trigger a new build:
1. Make a small change and push to GitHub (if auto-deploy is enabled)
2. Or manually trigger a build in Cloudflare Pages dashboard
3. Check build logs to verify env vars are available
4. Test checkout flow on the live site

---

**Note:** The publishable key is safe to expose in client-side code. The secret key remains secure in the Worker.

