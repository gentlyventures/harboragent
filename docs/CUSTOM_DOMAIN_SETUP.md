# Custom Domain Setup for harboragent.dev

This guide explains how to connect `harboragent.dev` to your Cloudflare Pages deployment and configure the download worker subdomain.

## Overview

After bringing `harboragent.dev` into Cloudflare, you need to:

1. **Connect the main domain** (`harboragent.dev`) to Cloudflare Pages
2. **Configure the worker subdomain** (`download.harboragent.dev`) for secure downloads
3. **Update DNS records** if needed

## Step 1: Connect Domain to Cloudflare Pages

### Via Cloudflare Dashboard

1. Go to: https://dash.cloudflare.com/ → **Workers & Pages**
2. Click on your **harbor-agent** project
3. Go to **Custom domains** tab
4. Click **Set up a custom domain**
5. Enter: `harboragent.dev`
6. Click **Continue**
7. Cloudflare will automatically configure DNS records

### DNS Records Created

Cloudflare Pages will automatically create:
- **CNAME** record: `harboragent.dev` → `harbor-agent.pages.dev`
- Or **A/AAAA** records if using apex domain

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

