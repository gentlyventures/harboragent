# Deployment Workflow for Harbor Agent

## Standard Workflow

When you want to update the site, just say **"update the site"** (or similar plain English) and the assistant will:

1. **Build** the site (`npm run build`)
2. **Deploy** to Cloudflare Pages (`wrangler pages deploy dist --project-name=harbor-agent`)
3. **Commit & Push** changes to GitHub (if there are uncommitted changes)

## Manual Commands

If you want to run it yourself:

```bash
# Just build and deploy (no git)
./deploy.sh

# Build, deploy, and commit changes
./deploy.sh --commit "Your commit message"

# Build, deploy, commit, and push to GitHub
./deploy.sh --commit "Your commit message" --push
```

## What the Assistant Will Do

When you say "update the site" or "deploy the site":
- ✅ Build the React app
- ✅ Deploy to Cloudflare Pages via Wrangler
- ✅ Commit any uncommitted changes
- ✅ Push to GitHub main branch

The site will be live at: https://harboragent.dev
