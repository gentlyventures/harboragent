# Fix Error 522: Connection Timed Out

Error 522 means Cloudflare can't connect to your Pages origin. This usually happens when the custom domain isn't properly registered in the Pages project.

## Solution: Register Domain in Pages Project

Even though you've added the DNS record, Cloudflare Pages needs the domain to be registered in the project settings.

### Option 1: Via Cloudflare Dashboard (If Available)

1. Go to: https://dash.cloudflare.com/ → **Workers & Pages**
2. Click on **harbor-agent** project
3. Look for **Custom domains** or **Domains** section
4. Click **Add custom domain** or **Connect domain**
5. Enter: `harboragent.dev`
6. Cloudflare will verify the DNS record and connect it

### Option 2: Via API Script (Recommended)

Use the provided script to add the domain via Cloudflare API:

```bash
# Set your API token (get it from Cloudflare dashboard)
export CLOUDFLARE_API_TOKEN='your-api-token-here'

# Run the script
./scripts/add-pages-domain.sh
```

Or manually via curl:

```bash
curl -X POST "https://api.cloudflare.com/client/v4/accounts/1e3a745b2bf8490fc60ea23c480dc530/pages/projects/harbor-agent/domains" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"domain":"harboragent.dev"}'
```

**Note**: Your API token needs `Account` → `Cloudflare Pages` → `Edit` permissions.

### Option 3: Verify DNS Record First

Before registering, make sure your DNS record is correct:

1. Go to: **DNS** → **Records** for `harboragent.dev`
2. Verify you have a CNAME record:
   - **Name**: `@` or `harboragent.dev`
   - **Target**: `harbor-agent.pages.dev` (exactly this, no trailing slash)
   - **Proxy status**: **Proxied** (orange cloud) ✅

### Option 4: Use Pages Subdomain Temporarily

While troubleshooting, you can access your site at:
- `https://harbor-agent.pages.dev`

This confirms the Pages project itself is working.

## Common Issues

### Wrong CNAME Target
- ❌ Wrong: `harbor-agent.pages.dev/`
- ✅ Correct: `harbor-agent.pages.dev`

### DNS Not Proxied
- The CNAME must have **Proxy status: Proxied** (orange cloud)
- If it's DNS-only (grey cloud), Pages won't work

### Domain Not Registered in Pages
- DNS record alone isn't enough
- Domain must be registered in Pages project settings

## Next Steps

1. Check if you can access: `https://harbor-agent.pages.dev` (this should work)
2. Verify DNS record is correct (see Option 3 above)
3. Try to register domain in Pages project (Option 1 or 2)
4. Wait 5-10 minutes after registration for SSL certificate provisioning

