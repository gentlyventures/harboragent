# Stripe Webhook Setup - Ready to Configure

**Status:** ✅ Worker endpoint ready and tested  
**Action Required:** Create webhook in Stripe Dashboard

---

## ✅ What's Already Done

1. ✅ Worker deployed with webhook handler
2. ✅ Webhook endpoint tested and responding: `https://download.harboragent.dev/webhook`
3. ✅ Postmark email integration ready
4. ✅ All secrets configured (except webhook secret)

---

## 🚀 Quick Setup (2 Steps)

### Step 1: Create Webhook in Stripe

1. **Go to Stripe Webhooks:**
   - https://dashboard.stripe.com/webhooks
   - Or: Stripe Dashboard → Developers → Webhooks

2. **Click "Add endpoint"**

3. **Configure:**
   - **Endpoint URL:** `https://download.harboragent.dev/webhook`
   - **Description:** (optional) "Harbor Agent download email delivery"
   - **Events to send:** Click "Select events"
     - ✅ Check: `checkout.session.completed`
   - Click **"Add endpoint"**

4. **Get Signing Secret:**
   - Click on the webhook you just created
   - Find **"Signing secret"** section
   - Click **"Reveal"** or **"Click to reveal"**
   - **Copy the secret** (starts with `whsec_`)

### Step 2: Set Webhook Secret

**Option A: Use the helper script:**
```bash
./setup-stripe-webhook.sh
```

**Option B: Manual command:**
```bash
wrangler secret put STRIPE_WEBHOOK_SECRET
# Paste the secret when prompted
```

**Option C: One-liner (replace with your secret):**
```bash
echo "whsec_YOUR_SECRET_HERE" | wrangler secret put STRIPE_WEBHOOK_SECRET
```

---

## ✅ Verification

After setting the secret, test it:

1. **Create a test payment:**
   - Go to: https://dashboard.stripe.com/test/payments
   - Use test card: `4242 4242 4242 4242`
   - Complete a checkout

2. **Check webhook delivery:**
   - Go to your webhook in Stripe
   - Check "Recent events" section
   - Should see `checkout.session.completed` with status "Succeeded"

3. **Verify email sent:**
   - Check the customer email inbox
   - Should receive email from `hello@harboragent.dev`
   - Email contains download link

4. **Check Worker logs:**
   ```bash
   wrangler tail
   ```

---

## 📋 Current Configuration

- **Webhook URL:** `https://download.harboragent.dev/webhook`
- **Event:** `checkout.session.completed`
- **Worker Status:** ✅ Deployed and responding
- **Postmark:** ✅ Configured
- **Email From:** `hello@harboragent.dev` (Harbor Agent)

---

## 🔍 Troubleshooting

### Webhook not receiving events
- ✅ Verify URL is correct: `https://download.harboragent.dev/webhook`
- ✅ Check event is selected: `checkout.session.completed`
- ✅ Ensure webhook is enabled (not paused)
- ✅ Test with a real checkout session

### Email not sending
- ✅ Verify Postmark secrets: `wrangler secret list | grep POSTMARK`
- ✅ Check Postmark dashboard for delivery status
- ✅ Verify sender signature confirmed: `hello@harboragent.dev`
- ✅ Check Worker logs: `wrangler tail`

### Webhook returns errors
- ✅ Check Worker logs: `wrangler tail`
- ✅ Verify all secrets are set: `wrangler secret list`
- ✅ Test endpoint manually (see test command below)

---

## 🧪 Manual Test

Test the webhook endpoint directly:

```bash
curl -X POST https://download.harboragent.dev/webhook \
  -H "Content-Type: application/json" \
  -H "stripe-signature: test" \
  -d '{
    "type": "checkout.session.completed",
    "data": {
      "object": {
        "id": "cs_test_123",
        "payment_status": "paid",
        "status": "complete",
        "customer_email": "test@example.com",
        "customer_details": {
          "email": "test@example.com"
        }
      }
    }
  }'
```

**Expected response:** `{"received":true}`

---

## 📞 Support

- **Stripe Webhooks:** https://dashboard.stripe.com/webhooks
- **Worker Logs:** `wrangler tail`
- **Postmark Dashboard:** https://account.postmarkapp.com/
- **Worker Health:** https://download.harboragent.dev/health

---

**Once webhook is configured, the complete automated flow will be:**
1. ✅ Customer pays → Stripe checkout completes
2. ✅ Stripe sends webhook → Worker receives event
3. ✅ Worker sends email → Customer gets download link automatically
4. ✅ Customer downloads → From email or success page

**Everything is ready - just need to create the webhook in Stripe! 🚀**

