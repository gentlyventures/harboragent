# Cloudflare Pages Environment Variables Setup

**Required for:** Frontend build to include Stripe configuration

## Environment Variables Needed

These need to be set in Cloudflare Pages for the build process:

1. **VITE_STRIPE_PUBLISHABLE_KEY**
   - Value: `pk_live_519LJSQE5Ht8pVL1uTp4kZb0t6HiRk5xeMaLLR80mGlBbW6aIC3Wk7WeG2XReEpfX1iTrwPaGPRQfZbTdsP3dqQmE00OyDS5kgT`
   - Purpose: Stripe publishable key for client-side checkout

2. **VITE_STRIPE_PRICE_ID**
   - Value: `price_1SZQOvE5Ht8pVL1uaWvlmgxK`
   - Purpose: Stripe price ID for $199 one-time purchase

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
     Value: `pk_live_519LJSQE5Ht8pVL1uTp4kZb0t6HiRk5xeMaLLR80mGlBbW6aIC3Wk7WeG2XReEpfX1iTrwPaGPRQfZbTdsP3dqQmE00OyDS5kgT`
   - Name: `VITE_STRIPE_PRICE_ID`
     Value: `price_1SZQOvE5Ht8pVL1uaWvlmgxK`
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
            "value": "pk_live_519LJSQE5Ht8pVL1uTp4kZb0t6HiRk5xeMaLLR80mGlBbW6aIC3Wk7WeG2XReEpfX1iTrwPaGPRQfZbTdsP3dqQmE00OyDS5kgT"
          },
          "VITE_STRIPE_PRICE_ID": {
            "value": "price_1SZQOvE5Ht8pVL1uaWvlmgxK"
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

✅ **Stripe Price Created:**
- Price ID: `price_1SZQOvE5Ht8pVL1uaWvlmgxK`
- Amount: $199.00 USD
- Type: One-time payment
- Product: Genesis Mission Readiness Pack

✅ **Publishable Key:**
- Key: `pk_live_519LJSQE5Ht8pVL1uTp4kZb0t6HiRk5xeMaLLR80mGlBbW6aIC3Wk7WeG2XReEpfX1iTrwPaGPRQfZbTdsP3dqQmE00OyDS5kgT`
- Mode: Live (production)

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

