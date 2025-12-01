#!/bin/bash
# Script to rotate Stripe webhook secret
# This rotates the secret for webhook ID: we_1SZPyOE5Ht8pVL1u6W99VViB

set -e

WEBHOOK_ID="we_1SZPyOE5Ht8pVL1u6W99VViB"
WEBHOOK_URL="https://download.harboragent.dev/webhook"

echo "🔄 Rotating Stripe Webhook Secret"
echo ""
echo "Webhook ID: $WEBHOOK_ID"
echo "Webhook URL: $WEBHOOK_URL"
echo ""

# Check if Stripe CLI is installed
if ! command -v stripe &> /dev/null; then
    echo "❌ Stripe CLI not found. Installing..."
    echo "Please install Stripe CLI: https://stripe.com/docs/stripe-cli"
    echo ""
    echo "Or use the Stripe Dashboard:"
    echo "1. Go to: https://dashboard.stripe.com/webhooks/$WEBHOOK_ID"
    echo "2. Click 'Reveal' on the signing secret"
    echo "3. Click 'Reset secret'"
    echo "4. Copy the new secret and run:"
    echo "   echo 'whsec_NEW_SECRET' | wrangler secret put STRIPE_WEBHOOK_SECRET"
    exit 1
fi

# Check if logged in to Stripe CLI
if ! stripe config --list &> /dev/null; then
    echo "⚠️  Not logged in to Stripe CLI. Please run:"
    echo "   stripe login"
    exit 1
fi

echo "Step 1: Rotating webhook secret via Stripe API..."
NEW_SECRET=$(stripe webhooks update $WEBHOOK_ID --reset-secret --format json | jq -r '.signing_secret')

if [ -z "$NEW_SECRET" ] || [ "$NEW_SECRET" == "null" ]; then
    echo "❌ Failed to rotate secret. Trying alternative method..."
    echo ""
    echo "Please rotate manually via Stripe Dashboard:"
    echo "1. Go to: https://dashboard.stripe.com/webhooks/$WEBHOOK_ID"
    echo "2. Click 'Reveal' on the signing secret"
    echo "3. Click 'Reset secret'"
    echo "4. Copy the new secret (starts with whsec_)"
    read -p "Paste the new secret here: " NEW_SECRET
fi

if [ -z "$NEW_SECRET" ] || [[ ! $NEW_SECRET =~ ^whsec_ ]]; then
    echo "❌ Invalid secret format. Secret must start with 'whsec_'"
    exit 1
fi

echo ""
echo "✅ New secret obtained: ${NEW_SECRET:0:20}..."
echo ""

echo "Step 2: Updating Cloudflare Worker secret..."
echo "$NEW_SECRET" | wrangler secret put STRIPE_WEBHOOK_SECRET

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Webhook secret rotated successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Verify webhook is working by creating a test payment"
    echo "2. Check webhook delivery in Stripe dashboard"
    echo "3. Monitor Worker logs: wrangler tail"
    echo ""
    echo "⚠️  IMPORTANT: The old secret is now invalid. Any webhooks using the old secret will fail."
else
    echo ""
    echo "❌ Failed to update Cloudflare Worker secret."
    echo "Please update manually:"
    echo "  echo '$NEW_SECRET' | wrangler secret put STRIPE_WEBHOOK_SECRET"
    exit 1
fi

