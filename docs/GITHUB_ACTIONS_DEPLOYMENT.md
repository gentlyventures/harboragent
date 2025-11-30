# GitHub Actions Deployment Guide (Future Use)

> **Note:** GitHub Actions requires payment and is not currently available.  
> For immediate deployment, see: [Manual Frontend Deployment Guide](./MANUAL_FRONTEND_DEPLOYMENT.md)

This guide explains how to deploy the Harbor Agent frontend using GitHub Actions, which bypasses Lovable's read-only file restrictions.

## Why GitHub Actions?

Lovable marks certain config files (`tsconfig.json`, `tsconfig.node.json`, `package.json`) as read-only, which prevents the build system from using your updated configurations. By using GitHub Actions, we build directly from your GitHub repository, using the correct config files you've committed.

## Setup

### 1. Required Secrets

Add these secrets to your GitHub repository:

1. Go to: **Settings** → **Secrets and variables** → **Actions**
2. Add the following secrets:

   - **`CLOUDFLARE_API_TOKEN`**: Your Cloudflare API token
     - Create at: https://dash.cloudflare.com/profile/api-tokens
     - Permissions needed: `Account` → `Cloudflare Pages` → `Edit`
   
   - **`CLOUDFLARE_ACCOUNT_ID`**: Your Cloudflare account ID
     - Find at: https://dash.cloudflare.com/ → Right sidebar → Account ID
     - Example: `1e3a745b2bf8490fc60ea23c480dc530`

### 2. Workflow File

The workflow file is already created at `.github/workflows/deploy.yml`. It will:

- Trigger on pushes to `main` branch
- Build the app using `npm run build` (which uses your correct config files)
- Deploy to Cloudflare Pages

### 3. First Deployment

Once secrets are configured:

1. Push to `main` branch (or manually trigger via **Actions** tab → **Deploy to Cloudflare Pages** → **Run workflow**)
2. The workflow will build and deploy automatically
3. Check the **Actions** tab to see build progress

## How It Works

1. **Checkout**: Gets your code from GitHub (including the correct config files)
2. **Setup Node.js**: Sets up Node.js 20 with npm caching
3. **Install**: Runs `npm ci` to install dependencies
4. **Build**: Runs `npm run build` using your `tsconfig.json`, `tsconfig.node.json`, and `package.json` from GitHub
5. **Deploy**: Deploys the `dist` folder to Cloudflare Pages

## Troubleshooting

### Build Fails

- Check the **Actions** tab for error logs
- Verify your config files are correct on GitHub
- Ensure `npm run build` works locally

### Deployment Fails

- Verify `CLOUDFLARE_API_TOKEN` has correct permissions
- Verify `CLOUDFLARE_ACCOUNT_ID` is correct
- Check Cloudflare Pages dashboard for errors

### Secrets Not Found

- Ensure secrets are added to GitHub repository settings
- Secrets must be named exactly: `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`

## Manual Trigger

You can manually trigger the workflow:

1. Go to **Actions** tab in GitHub
2. Select **Deploy to Cloudflare Pages** workflow
3. Click **Run workflow** → **Run workflow**

## Benefits

✅ Uses your correct config files from GitHub  
✅ Bypasses Lovable's read-only restrictions  
✅ Automated deployment on every push to `main`  
✅ Full control over build process  
✅ Build logs visible in GitHub Actions

