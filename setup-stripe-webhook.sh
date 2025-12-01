#!/bin/bash
# Quick script to help set up Stripe webhook secret

echo "🔧 Stripe Webhook Setup Helper"
echo ""
echo "Step 1: Create webhook in Stripe Dashboard"
echo "   → Go to: https://dashboard.stripe.com/webhooks"
echo "   → Click 'Add endpoint'"
echo "   → URL: https://download.harboragent.dev/webhook"
echo "   → Event: checkout.session.completed"
echo "   → Click 'Add endpoint'"
echo ""
echo "Step 2: Get the webhook signing secret"
echo "   → Click on the webhook you just created"
echo "   → Find 'Signing secret' section"
echo "   → Click 'Reveal' and copy the secret (starts with whsec_)"
echo ""
read -p "Step 3: Paste the webhook secret here (whsec_...): " webhook_secret

if [ -z "$webhook_secret" ]; then
  echo "❌ No secret provided. Exiting."
  exit 1
fi

if [[ ! $webhook_secret =~ ^whsec_ ]]; then
  echo "⚠️  Warning: Secret should start with 'whsec_'"
  read -p "Continue anyway? (y/n): " confirm
  if [ "$confirm" != "y" ]; then
    exit 1
  fi
fi

echo ""
echo "Setting webhook secret in Cloudflare Worker..."
echo "$webhook_secret" | wrangler secret put STRIPE_WEBHOOK_SECRET

if [ $? -eq 0 ]; then
  echo ""
  echo "✅ Webhook secret set successfully!"
  echo ""
  echo "Next steps:"
  echo "1. Test the webhook by creating a test payment in Stripe"
  echo "2. Check webhook delivery status in Stripe dashboard"
  echo "3. Verify email is sent to customer"
  echo ""
  echo "Monitor Worker logs:"
  echo "  wrangler tail"
else
  echo ""
  echo "❌ Failed to set webhook secret. Please try manually:"
  echo "  wrangler secret put STRIPE_WEBHOOK_SECRET"
fi

