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
RESPONSE=$(curl -s -X POST \
  "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects/$PROJECT_NAME/domains" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"domain\":\"$DOMAIN\"}")

# Check if successful
if echo "$RESPONSE" | grep -q '"success":true'; then
    echo "✅ Successfully added $DOMAIN to Pages project!"
    echo ""
    echo "Response:"
    echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"
    echo ""
    echo "Next steps:"
    echo "1. Verify DNS record exists: CNAME @ → harbor-agent.pages.dev (Proxied)"
    echo "2. Wait 5-10 minutes for SSL certificate provisioning"
    echo "3. Test: https://$DOMAIN"
else
    echo "❌ Failed to add domain"
    echo ""
    echo "Response:"
    echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"
    echo ""
    echo "Common issues:"
    echo "- API token doesn't have Pages:Edit permission"
    echo "- Domain already exists in another project"
    echo "- DNS record not found or incorrect"
    exit 1
fi

