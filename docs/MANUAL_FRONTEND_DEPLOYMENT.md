# Manual Frontend Deployment Guide

Since GitHub Actions isn't available and Lovable's build system has read-only config files, here's how to build and deploy manually using your correct config files.

## Why Manual Deployment?

- Lovable marks `tsconfig.json`, `tsconfig.node.json`, and `package.json` as read-only
- Your fixes are on GitHub but Lovable's build can't use them
- Manual build uses your correct config files from the repository
- Deploy directly to Cloudflare Pages using Wrangler

## Prerequisites

1. **Node.js 20+** installed locally
2. **Wrangler CLI** installed: `npm install -g wrangler`
3. **Cloudflare account** with Pages access

## Step 1: Build Locally

Build the app using your correct config files from GitHub:

```bash
# Clone/pull latest from GitHub (if not already)
git pull origin main

# Install dependencies
npm ci

# Build using your correct config files
npm run build
```

This will:
- Use your `tsconfig.json` with `baseUrl` and `paths`
- Use your `tsconfig.node.json` with `noEmit: false`
- Use your `package.json` with `build:dev` script
- Output to `dist/` directory

## Step 2: Deploy to Cloudflare Pages

### Option A: Using Wrangler CLI (Recommended)

```bash
# Login to Cloudflare (if not already)
wrangler login

# Deploy to Cloudflare Pages
wrangler pages deploy dist --project-name=harbor-agent
```

### Option B: Using Cloudflare Dashboard

1. Go to: https://dash.cloudflare.com/ → **Workers & Pages**
2. Click **Create application** → **Pages** → **Upload assets**
3. Drag and drop your `dist/` folder
4. Name it `harbor-agent`
5. Click **Deploy site**

## Step 3: Verify Deployment

After deployment, your site will be available at:
- `https://harbor-agent.pages.dev` (or your custom domain if configured)

## Quick Deploy Script

Create a simple script to automate this:

```bash
#!/bin/bash
# deploy.sh

echo "Building..."
npm ci
npm run build

echo "Deploying to Cloudflare Pages..."
wrangler pages deploy dist --project-name=harbor-agent

echo "Deployment complete!"
```

Make it executable and run:
```bash
chmod +x deploy.sh
./deploy.sh
```

## Troubleshooting

### Build Fails Locally

- Verify you're on the latest code: `git pull origin main`
- Check Node.js version: `node --version` (should be 20+)
- Clear cache: `rm -rf node_modules package-lock.json && npm install`

### Wrangler Login Issues

- Use OAuth: `wrangler login` (opens browser)
- Or set API token: `wrangler config` and paste your token

### Deployment Fails

- Verify `dist/` folder exists and has content
- Check Cloudflare account has Pages access
- Verify project name matches existing Pages project (or create new one)

## Benefits of Manual Deployment

✅ Uses your correct config files from GitHub  
✅ Bypasses Lovable's read-only restrictions  
✅ Full control over build process  
✅ Can test build locally before deploying  
✅ No GitHub Actions required  

## When to Use This

- When Lovable's build fails due to read-only files
- When you need to deploy immediately
- When testing config changes
- As a workaround until GitHub Actions is available

