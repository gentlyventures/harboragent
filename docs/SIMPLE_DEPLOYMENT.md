# Simple Deployment Guide (No GitHub Actions)

Since GitHub Actions requires payment, here's the simplest way to deploy:

## Option 1: Manual Deployment (Once GitHub payment is resolved)

Once your GitHub payment is working, the workflow will deploy automatically. Until then:

1. **Set Worker secrets manually:**
   ```bash
   # Use OAuth (not API token with IP restrictions)
   wrangler login
   
   # Set secrets
   wrangler secret put STRIPE_SECRET_KEY
   wrangler secret put DOWNLOAD_ORIGIN_URL
   ```

2. **Deploy:**
   ```bash
   wrangler deploy
   ```

## Option 2: Use Cloudflare R2 (Free, No GitHub needed)

R2 is Cloudflare's object storage (like S3) with a generous free tier.

### Setup R2:

1. **Create R2 bucket:**
   - Go to: https://dash.cloudflare.com/ → R2
   - Create bucket: `harbor-agent-packs`
   - Upload your zip file

2. **Get R2 URL:**
   - R2 provides a public URL for objects
   - Format: `https://pub-xxxxx.r2.dev/harbor-agent-genesis-pack-v1.0.zip`

3. **Update Worker:**
   - Set `DOWNLOAD_ORIGIN_URL` to the R2 URL
   - Or modify Worker to serve directly from R2 (see below)

### Serve directly from R2 in Worker:

We can modify the Worker to fetch from R2 directly, eliminating the redirect:

```typescript
// Worker fetches from R2 and streams to user
const fileResponse = await env.R2_BUCKET.get('harbor-agent-genesis-pack-v1.0.zip');
return new Response(fileResponse.body, {
  headers: {
    'Content-Type': 'application/zip',
    'Content-Disposition': 'attachment; filename="harbor-agent-genesis-pack-v1.0.zip"'
  }
});
```

## Option 3: Keep GitHub Releases (Simplest)

GitHub Releases still works even if Actions are disabled! The file is already there:
- URL: `https://github.com/gentlyventures/harboragent/releases/download/v1.0.0/harbor-agent-genesis-pack-v1.0.zip`

Just deploy the Worker manually (once you can authenticate) and it will redirect to this URL.

## Recommendation

**Use Option 3 (GitHub Releases)** - it's already set up and working. Just deploy the Worker manually when you can, or wait for GitHub payment to resolve and Actions will deploy automatically.

The Worker just needs to verify Stripe payment and redirect - the file hosting is already handled by GitHub Releases.

