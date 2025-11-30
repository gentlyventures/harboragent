# Deployment Guide for harboragent.dev

## Quick Answer

**If Cloudflare Pages is connected to your GitHub repo:**
1. Commit your changes
2. Push to `main` branch
3. Cloudflare Pages automatically builds and deploys

**If not connected, use manual deployment (see below)**

---

## Option 1: Auto-Deploy via Cloudflare Pages Integration (Recommended)

### How to Check if It's Set Up

1. Go to: https://dash.cloudflare.com/
2. Navigate to **Workers & Pages** → **harbor-agent** project
3. Check the **Settings** tab → **Builds & deployments**
4. If you see "Connected to GitHub" with your repo, it's set up!

### How It Works

When you push to GitHub:
1. Cloudflare Pages detects the push
2. Automatically runs: `npm ci && npm run build`
3. Deploys the `dist/` folder
4. Site updates at `harboragent.dev`

### To Deploy Now

```bash
# 1. Commit your changes
git add .
git commit -m "Refactor: Harbor Agent as product line, Genesis as Pack #1"

# 2. Push to GitHub
git push origin main

# 3. Check deployment status
# Go to: https://dash.cloudflare.com/ → Workers & Pages → harbor-agent → Deployments
```

---

## Option 2: Manual Deployment (If Auto-Deploy Not Set Up)

### Prerequisites

- Node.js 20+ installed
- Wrangler CLI installed (you have it: `/Users/dwmini/.nvm/versions/node/v22.18.0/bin/wrangler`)
- Cloudflare account access

### Steps

```bash
# 1. Build the site locally
npm ci
npm run build

# 2. Deploy to Cloudflare Pages
wrangler pages deploy dist --project-name=harbor-agent
```

### Verify Deployment

After deployment, check:
- https://harboragent.dev (main site)
- https://dash.cloudflare.com/ → Workers & Pages → harbor-agent → Deployments

---

## Option 3: Enable GitHub Actions (Future)

The GitHub Actions workflow exists but is currently disabled. To enable:

1. Edit `.github/workflows/deploy.yml`
2. Remove or comment out: `if: false  # DISABLED`
3. Add Cloudflare secrets to GitHub:
   - `CLOUDFLARE_API_TOKEN`
   - `CLOUDFLARE_ACCOUNT_ID`
4. Push the change
5. GitHub Actions will deploy on every push to `main`

---

## Current Status

Based on your repo:
- ✅ Wrangler CLI installed
- ✅ Build script configured (`npm run build`)
- ✅ Output directory: `dist/`
- ⚠️ GitHub Actions workflow exists but is disabled

**Most likely:** Cloudflare Pages is directly connected to your GitHub repo, so **just push to GitHub** and it will auto-deploy!

---

## Troubleshooting

### Build Fails
- Check Cloudflare Pages build logs
- Verify `package.json` dependencies are correct
- Ensure Node.js version matches (should be 20+)

### Deployment Doesn't Update
- Check if Cloudflare Pages is connected to the correct branch (`main`)
- Verify the build completed successfully
- Check for any deployment errors in Cloudflare dashboard

### Manual Deployment Fails
- Ensure you're logged in: `wrangler login`
- Verify project name: `harbor-agent`
- Check you have Cloudflare Pages permissions

