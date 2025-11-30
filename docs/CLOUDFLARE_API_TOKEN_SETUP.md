# Cloudflare API Token Setup Guide

This guide provides exact permissions and IP filtering configuration for the Cloudflare API token used to deploy the Harbor Agent Worker via GitHub Actions.

## Required Permissions

### Account-Level Permissions

For deploying Workers via Wrangler, you need:

1. **Workers Scripts: Edit**
   - Allows creating, updating, and deleting Workers scripts
   - Required for `wrangler deploy`
   - When set at account level, this includes implicit account access

**Note:** "Account: Read" is not available as a separate permission option in Cloudflare's API token interface. The account-level access is automatically included when you grant Workers Scripts permissions at the account level.

### Zone-Level Permissions (Optional)

Only needed if you're using custom domain routes:

1. **Workers Routes: Edit**
   - Allows configuring Workers routes for specific zones
   - Only needed if `wrangler.toml` has route configuration

2. **Zone: Read**
   - Allows reading zone details
   - Only needed if using custom routes

**Note:** If you're using the default `workers.dev` subdomain (no custom routes), you don't need zone-level permissions.

## Client IP Address Filtering

### Recommended: Restrict to GitHub Actions IPs

For maximum security, restrict the token to GitHub Actions IP addresses only. This ensures the token can only be used from GitHub's CI/CD runners.

### GitHub Actions IP Ranges

GitHub Actions uses the following IP ranges (as of 2024):

```
# GitHub Actions hosted runners (all regions)
140.82.112.0/20
143.55.64.0/20
185.199.108.0/22
192.30.252.0/22

# GitHub Actions hosted runners (additional ranges)
140.82.112.0/20
143.55.64.0/20
185.199.108.0/22
192.30.252.0/22
```

**Important:** GitHub Actions IP ranges can change. For the most up-to-date list:

1. Visit: https://api.github.com/meta
2. Look for the `actions` array in the JSON response
3. Use those CIDR ranges

Alternatively, you can use GitHub's IP allowlist API:
```bash
curl https://api.github.com/meta | jq '.actions[]'
```

### Alternative: No IP Filtering (Less Secure)

If you need to use the token from multiple locations (local development, other CI systems), you can skip IP filtering. However, this is less secure and not recommended for production tokens.

## Step-by-Step Token Creation

### 1. Navigate to API Tokens

1. Log into [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Click your profile icon (top right)
3. Select **My Profile**
4. Click **API Tokens** in the left sidebar
5. Click **Create Token**

### 2. Choose Token Type

- Select **Create Custom Token** (not "Edit Cloudflare Workers" template)
- Click **Get Started**

### 3. Configure Permissions

#### Account Resources

1. Under **Account**, select your account
2. Add this permission:
   - ✅ **Workers Scripts: Edit**
   - (Optional) **Workers Scripts: Read** - helpful for validation but not required

#### Zone Resources (Only if using custom routes)

If your `wrangler.toml` has route configuration:

1. Under **Zone**, select the zone(s) where you'll deploy
2. Add these permissions:
   - ✅ **Workers Routes: Edit**
   - ✅ **Zone: Read**

**If using workers.dev subdomain only:** Skip zone resources entirely.

### 4. Set Client IP Address Filtering

1. Scroll to **Client IP Address Filtering**
2. Select **Restrict to specific IP addresses**
3. Add GitHub Actions IP ranges (one per line or comma-separated):

```
140.82.112.0/20
143.55.64.0/20
185.199.108.0/22
192.30.252.0/22
```

**Note:** Cloudflare accepts CIDR notation (e.g., `140.82.112.0/20`) or individual IPs.

### 5. Set Token Expiration (Recommended)

1. Under **Time to Live (TTL) Constraints**
2. Set an expiration date (e.g., 1 year from now)
3. This ensures tokens are rotated regularly

### 6. Review and Create

1. Review all settings
2. Click **Continue to summary**
3. Review the summary
4. Click **Create Token**
5. **IMPORTANT:** Copy the token immediately - you won't be able to see it again!

## Token Storage

### Add to GitHub Secrets

1. Go to your repository on GitHub
2. Navigate to: **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `CLOUDFLARE_API_TOKEN`
5. Value: Paste the token you just created
6. Click **Add secret**

### Security Best Practices

1. **Never commit the token** to version control
2. **Store only in GitHub Secrets** (encrypted at rest)
3. **Rotate regularly** (set expiration date)
4. **Use least privilege** (only required permissions)
5. **Monitor usage** in Cloudflare dashboard

## Verification

### Test the Token

After adding to GitHub Secrets, test the deployment:

```bash
# The token should work from GitHub Actions
# You can also test locally (if not using IP filtering):
export CLOUDFLARE_API_TOKEN="your_token_here"
wrangler deploy --dry-run
```

### Check Token Permissions

View token details in Cloudflare:
1. Go to **My Profile** → **API Tokens**
2. Find your token in the list
3. Click to view details and verify permissions

## Troubleshooting

### "Insufficient permissions" error

- Verify **Workers Scripts: Edit** is set at account level
- Ensure the token is scoped to the correct account
- If using routes, verify zone permissions

### "IP address not allowed" error

- Check that GitHub Actions IP ranges are correct
- Verify IP filtering settings in token configuration
- If testing locally, temporarily disable IP filtering or add your IP

### Token not working in GitHub Actions

- Verify token is correctly added to GitHub Secrets
- Check that secret name matches: `CLOUDFLARE_API_TOKEN`
- Verify token hasn't expired
- Check GitHub Actions logs for specific error messages

## References

- [Cloudflare API Token Documentation](https://developers.cloudflare.com/fundamentals/api/get-started/account-owned-tokens/)
- [Restricting Tokens by IP](https://developers.cloudflare.com/fundamentals/api/how-to/restrict-tokens/)
- [GitHub Actions IP Ranges](https://api.github.com/meta)
- [Wrangler Deployment Guide](https://developers.cloudflare.com/workers/ci-cd/builds/configuration/)

## Summary

**Minimum Required Permissions:**
- Account: **Workers Scripts: Edit**, **Account: Read**
- Zone: None (unless using custom routes)

**Recommended IP Filtering:**
- Restrict to GitHub Actions IP ranges (see above)

**Token Storage:**
- Store in GitHub Secrets as `CLOUDFLARE_API_TOKEN`
- Never commit to version control

