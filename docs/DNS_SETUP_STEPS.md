# DNS Setup for harboragent.dev → Cloudflare Pages

## Quick Answer

**Yes, you need to change the A record** to point to Cloudflare Pages instead of `185.158.133.1`.

## Step-by-Step Instructions

### 1. Update the A Record

1. Go to: https://dash.cloudflare.com/ → Select `harboragent.dev` → **DNS** → **Records**
2. Find the **A record** for `harboragent.dev` (currently `185.158.133.1`)
3. Click **Edit**
4. **Replace it with a CNAME record**:
   - Click **Delete** on the A record
   - Click **Add record**
   - **Type**: CNAME
   - **Name**: `@` (this represents the apex domain `harboragent.dev`)
   - **Target**: `harbor-agent.pages.dev`
   - **Proxy status**: **Proxied** (orange cloud icon) ✅
   - Click **Save**

### 2. Why CNAME Instead of A Record?

- Cloudflare Pages uses CNAME records
- Cloudflare automatically handles "CNAME flattening" for apex domains
- This is the standard way to connect Pages to a custom domain

### 3. Verify

After saving, wait 1-5 minutes for DNS propagation, then:
- Visit: https://harboragent.dev
- It should show your Cloudflare Pages site

### 4. Worker Subdomain (Already Done)

The worker route `download.harboragent.dev` is already configured and deployed. No additional DNS changes needed - Cloudflare handles this automatically when the worker route is active.

## Current Status

- ✅ Worker deployed with route: `download.harboragent.dev/*`
- ⏳ A record needs to be changed to CNAME pointing to `harbor-agent.pages.dev`

## Troubleshooting

**If the site doesn't load after 5 minutes:**
- Check that the CNAME record shows "Proxied" (orange cloud)
- Verify the target is exactly: `harbor-agent.pages.dev`
- Check SSL/TLS settings in Cloudflare (should be "Full" or "Full (strict)")

