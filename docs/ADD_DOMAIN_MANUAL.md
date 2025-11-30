# Manual Steps to Add Domain to Cloudflare Pages

If the script doesn't work, here's how to do it manually:

## Step 1: Get Your API Token

1. Go to: https://dash.cloudflare.com/profile/api-tokens
2. Find your token (or create a new one with `Cloudflare Pages:Edit` permission)
3. Copy the token

## Step 2: Test the API Call

Run this curl command (replace `YOUR_API_TOKEN` with your actual token):

```bash
curl -X POST \
  "https://api.cloudflare.com/client/v4/accounts/1e3a745b2bf8490fc60ea23c480dc530/pages/projects/harbor-agent/domains" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"domain":"harboragent.dev"}'
```

## Step 3: Check the Response

### Success Response:
```json
{
  "result": {
    "domain": "harboragent.dev",
    "status": "pending"
  },
  "success": true
}
```

### Common Error Responses:

**Domain already exists:**
```json
{
  "errors": [{
    "code": 1004,
    "message": "Domain already exists"
  }],
  "success": false
}
```
→ This might be okay! Check if it's already connected.

**Permission denied:**
```json
{
  "errors": [{
    "code": 10000,
    "message": "Authentication error"
  }],
  "success": false
}
```
→ Check your API token permissions.

**Project not found:**
```json
{
  "errors": [{
    "code": 10009,
    "message": "Project not found"
  }],
  "success": false
}
```
→ Verify project name is `harbor-agent` (with hyphen, not underscore).

## Step 4: Verify Domain is Added

After successful API call:

1. Go to: https://dash.cloudflare.com/ → **Workers & Pages** → **harbor-agent**
2. Look for **Custom domains** or **Domains** section
3. You should see `harboragent.dev` listed

## Alternative: Check Existing Domains

To see what domains are already connected:

```bash
curl -X GET \
  "https://api.cloudflare.com/client/v4/accounts/1e3a745b2bf8490fc60ea23c480dc530/pages/projects/harbor-agent/domains" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json"
```

This will show all domains currently connected to the project.

