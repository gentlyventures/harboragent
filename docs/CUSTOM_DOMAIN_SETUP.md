# Custom Domain Setup for harboragent.dev

This guide explains how to connect `harboragent.dev` to your Cloudflare Pages deployment and configure the download worker subdomain.

## Overview

After bringing `harboragent.dev` into Cloudflare, you need to:

1. **Connect the main domain** (`harboragent.dev`) to Cloudflare Pages
2. **Configure the worker subdomain** (`download.harboragent.dev`) for secure downloads
3. **Update DNS records** if needed

## Step 1: Connect Domain to Cloudflare Pages

Since the domain is already in Cloudflare, you need to update DNS records manually. Your Pages project URL is: `harbor-agent.pages.dev`

### Update the A Record for harboragent.dev

1. Go to: https://dash.cloudflare.com/ → Select `harboragent.dev` → **DNS** → **Records**
2. Find the **A record** for `harboragent.dev` (currently pointing to `185.158.133.1`)
3. Click **Edit** on that A record
4. You have two options:

   **Option A: Use CNAME Flattening (Easiest)**
   - Delete the A record
   - Add a new **CNAME** record:
     - **Type**: CNAME
     - **Name**: `@` or `harboragent.dev` (apex)
     - **Target**: `harbor-agent.pages.dev`
     - **Proxy status**: Proxied (orange cloud) ✅
   - Cloudflare will automatically flatten the CNAME to work with apex domains

   **Option B: Keep A Record (If CNAME not supported)**
   - Change the **Content** from `185.158.133.1` to Cloudflare Pages IP
   - Get the IP from: **Workers & Pages** → **harbor-agent** → Check project details
   - Or use Cloudflare's Pages IPs (they provide these in the project settings)

**Recommended**: Use Option A (CNAME with flattening) - it's simpler and Cloudflare handles it automatically.

## Step 2: Configure Worker Subdomain

The download worker needs to be accessible at `download.harboragent.dev`.

### Update Worker Route

The `wrangler.toml` file is already configured with:

```toml
route = { pattern = "download.harboragent.dev/*", zone_name = "harboragent.dev" }
```

### Deploy Worker with Custom Route

```bash
cd /path/to/harbor_agent
wrangler deploy
```

This will:
- Deploy the worker
- Configure the route `download.harboragent.dev/*` to point to the worker
- Cloudflare will automatically create the DNS record

### Verify Worker Route

After deployment, verify the route is active:

```bash
wrangler routes list
```

You should see:
```
download.harboragent.dev/* → harboragent-personalized-download
```

## Step 3: Verify DNS Configuration

### Check DNS Records

In Cloudflare Dashboard:
1. Go to: **DNS** → **Records**
2. Verify these records exist:
   - `harboragent.dev` → CNAME to `harbor-agent.pages.dev` (or A/AAAA records)
   - `download.harboragent.dev` → Automatically created by Worker route

### Test Domains

After DNS propagation (usually 1-5 minutes):

1. **Main site**: https://harboragent.dev
2. **Download worker**: https://download.harboragent.dev/verify-session (should return JSON)

## Step 4: Update Environment Variables

Update your `.env` file (or Cloudflare Pages environment variables):

```bash
VITE_WORKER_URL=https://download.harboragent.dev
```

For **Cloudflare Pages** environment variables:
1. Go to: **Workers & Pages** → **harbor-agent** → **Settings** → **Environment variables**
2. Add: `VITE_WORKER_URL` = `https://download.harboragent.dev`
3. Redeploy the site

## Troubleshooting

### Domain Not Resolving

- Wait 5-10 minutes for DNS propagation
- Check DNS records in Cloudflare dashboard
- Verify domain is using Cloudflare nameservers

### Worker Route Not Working

- Verify `wrangler.toml` has the route configured
- Redeploy worker: `wrangler deploy`
- Check Worker routes in Cloudflare dashboard: **Workers & Pages** → **harboragent-personalized-download** → **Routes**

### SSL Certificate Issues

- Cloudflare automatically provisions SSL certificates
- Wait 5-10 minutes after domain connection
- Check **SSL/TLS** settings in Cloudflare dashboard

### Pages Not Loading

- Verify custom domain is connected in Pages project
- Check deployment status in Pages dashboard
- Ensure DNS records are correct

## Current Configuration

- **Main site**: `harboragent.dev` → Cloudflare Pages (`harbor-agent` project)
- **Download worker**: `download.harboragent.dev` → Cloudflare Worker (`harboragent-personalized-download`)
- **Fallback worker URL**: `https://harboragent-personalized-download.dave-1e3.workers.dev` (still works)

## Next Steps

After setup:
1. Test the main site: https://harboragent.dev
2. Test checkout flow (uses `download.harboragent.dev`)
3. Update any external links/documentation to use `harboragent.dev`

