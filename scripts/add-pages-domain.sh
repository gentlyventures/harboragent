#!/bin/bash
# Add custom domain to Cloudflare Pages project via API

# Configuration
ACCOUNT_ID="1e3a745b2bf8490fc60ea23c480dc530"
PROJECT_NAME="harbor-agent"
DOMAIN="harboragent.dev"

# Check if API token is set
if [ -z "$CLOUDFLARE_API_TOKEN" ]; then
    echo "Error: CLOUDFLARE_API_TOKEN environment variable is not set"
    echo ""
    echo "To set it:"
    echo "  export CLOUDFLARE_API_TOKEN='your-api-token'"
    echo ""
    echo "Or create a .env file with:"
    echo "  CLOUDFLARE_API_TOKEN=your-api-token"
    echo ""
    exit 1
fi

echo "Adding custom domain $DOMAIN to Pages project $PROJECT_NAME..."
echo ""

# Add domain to Pages project
echo "Making API request..."
RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST \
  "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects/$PROJECT_NAME/domains" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"domain\":\"$DOMAIN\"}")

# Extract HTTP code and response body
HTTP_CODE=$(echo "$RESPONSE" | grep "HTTP_CODE:" | cut -d: -f2)
BODY=$(echo "$RESPONSE" | sed '/HTTP_CODE:/d')

echo "HTTP Status Code: $HTTP_CODE"
echo ""

# Check if successful
if echo "$BODY" | grep -q '"success":true'; then
    echo "✅ Successfully added $DOMAIN to Pages project!"
    echo ""
    echo "Response:"
    echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"
    echo ""
    echo "Next steps:"
    echo "1. Verify DNS record exists: CNAME @ → harbor-agent.pages.dev (Proxied)"
    echo "2. Wait 5-10 minutes for SSL certificate provisioning"
    echo "3. Test: https://$DOMAIN"
elif echo "$BODY" | grep -q '"already exists"'; then
    echo "⚠️  Domain already exists in this or another project"
    echo ""
    echo "Response:"
    echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"
    echo ""
    echo "This might be okay - check if the domain is already connected in Pages dashboard"
elif [ "$HTTP_CODE" = "401" ]; then
    echo "❌ Authentication failed - check your API token"
    echo ""
    echo "Response:"
    echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"
    exit 1
elif [ "$HTTP_CODE" = "403" ]; then
    echo "❌ Permission denied - API token needs 'Cloudflare Pages:Edit' permission"
    echo ""
    echo "Response:"
    echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"
    exit 1
else
    echo "❌ Failed to add domain (HTTP $HTTP_CODE)"
    echo ""
    echo "Full Response:"
    echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"
    echo ""
    echo "Common issues:"
    echo "- API token doesn't have Pages:Edit permission"
    echo "- Domain already exists in another project"
    echo "- DNS record not found or incorrect"
    echo "- Project name might be wrong (current: $PROJECT_NAME)"
    exit 1
fi

