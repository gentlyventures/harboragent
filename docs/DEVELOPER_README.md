# Developer & Maintainer Documentation

This document is for developers working on this repository, deploying the Worker, and maintaining the infrastructure.

## 🚀 Secure Download System

This repository includes a **Cloudflare Worker** that handles secure, verified downloads of the Genesis Professional Pack.

### Worker Details

- **Worker URL:** `https://harboragent-personalized-download.dave-1e3.workers.dev`
- **Worker Name:** `harboragent-personalized-download`
- **Location:** `workers/personalized-download/src/index.ts`

### How It Works

1. Customer completes Stripe checkout → Receives session ID
2. Customer visits Worker `/download?session_id=...` endpoint
3. Worker verifies payment with Stripe API
4. If valid, redirects to secure GitHub Releases download

### Architecture

```
Customer → Stripe Checkout → Worker (/download) → GitHub Releases
                ↓
         Session Verification
                ↓
         Secure Redirect
```

### Endpoints

- `GET /health` - Health check endpoint
- `GET /download?session_id=...` - Download endpoint (verifies Stripe session)
- `POST /verify-session` - API endpoint to verify session validity

### Deployment

**Current Status:** ✅ Deployed and live

**Deployment Methods:**
- **Automated:** GitHub Actions (when payment is active)
- **Manual:** `wrangler deploy` (see `docs/MANUAL_DEPLOYMENT.md`)

### Configuration

- **Config File:** `wrangler.toml`
- **Secrets:** Set via `wrangler secret put` or Cloudflare dashboard
  - `STRIPE_SECRET_KEY` - Stripe API secret key
  - `DOWNLOAD_ORIGIN_URL` - GitHub Releases URL
  - `GENESIS_PACK_PRICE_ID` - (Optional) Stripe Price ID

### File Hosting

Files are hosted on **GitHub Releases**:
- Current version: v1.0.0
- URL: `https://github.com/gentlyventures/harboragent/releases/download/v1.0.0/harbor-agent-genesis-pack-v1.0.zip`
- See `docs/RELEASE_SETUP.md` for creating new releases

### Documentation

- **Delivery System:** `docs/GENESIS_PACK_DELIVERY.md`
- **Release Setup:** `docs/RELEASE_SETUP.md`
- **API Token Setup:** `docs/CLOUDFLARE_API_TOKEN_SETUP.md`
- **Manual Deployment:** `docs/MANUAL_DEPLOYMENT.md`
- **R2 Alternative:** `docs/R2_SETUP.md` (if moving away from GitHub Releases)

### Development

**Local Testing:**
```bash
cd workers/personalized-download
wrangler dev
```

**Deploy:**
```bash
wrangler deploy
```

**View Logs:**
```bash
wrangler tail
```

### Maintenance

- **Update Worker:** Edit `workers/personalized-download/src/index.ts`
- **Update Secrets:** Use `wrangler secret put` or Cloudflare dashboard
- **Create New Release:** Use GitHub Releases UI or `docs/RELEASE_SETUP.md`
- **Update DOWNLOAD_ORIGIN_URL:** When new release is created, update the secret

### Troubleshooting

See `docs/GENESIS_PACK_DELIVERY.md` for troubleshooting guide.

