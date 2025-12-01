# Stripe Webhook Setup - Quick Guide

**Status:** ✅ Worker deployed with webhook handler  
**Next Step:** Configure webhook in Stripe Dashboard

---

## Setup Steps

### 1. Go to Stripe Webhooks Dashboard

Visit: https://dashboard.stripe.com/webhooks

### 2. Add New Webhook Endpoint

1. Click **"Add endpoint"** button
2. Set **Endpoint URL** to:
   ```
   https://download.harboragent.dev/webhook
   ```
3. Click **"Select events"** or **"Select events to listen to"**
4. Check the box for:
   - ✅ `checkout.session.completed`
5. Click **"Add endpoint"**

### 3. Get Webhook Signing Secret

1. After creating the endpoint, click on it to view details
2. Find the **"Signing secret"** section
3. Click **"Reveal"** or **"Click to reveal"**
4. Copy the secret (starts with `whsec_`)

### 4. Set Webhook Secret in Worker

Run this command (replace `whsec_...` with your actual secret):

```bash
echo "whsec_YOUR_ACTUAL_SECRET_HERE" | wrangler secret put STRIPE_WEBHOOK_SECRET
```

**Or interactively:**
```bash
wrangler secret put STRIPE_WEBHOOK_SECRET
# Paste the signing secret when prompted
```

### 5. Test the Webhook

1. **Create a test checkout** in Stripe:
   - Go to: https://dashboard.stripe.com/test/payments
   - Use Stripe's test card: `4242 4242 4242 4242`
   - Complete a test purchase

2. **Check webhook delivery**:
   - Go to your webhook endpoint in Stripe
   - Check the "Recent events" section
   - Look for `checkout.session.completed` event
   - Status should be "Succeeded" (green)

3. **Verify email sent**:
   - Check the customer's email inbox
   - Should receive email from `hello@harboragent.dev`
   - Email contains download link

4. **Check Worker logs** (optional):
   ```bash
   wrangler tail
   ```
   Look for webhook processing logs

---

## Webhook Endpoint Details

- **URL:** `https://download.harboragent.dev/webhook`
- **Method:** `POST`
- **Event:** `checkout.session.completed`
- **Authentication:** Webhook signature verification (optional but recommended)

---

## What Happens When Webhook Fires

1. **Stripe sends webhook** → `POST /webhook` with event data
2. **Worker receives event** → Parses `checkout.session.completed`
3. **Worker verifies payment** → Checks `payment_status === 'paid'` and `status === 'complete'`
4. **Worker extracts email** → Gets customer email from session
5. **Worker sends email** → Postmark API sends HTML email with download link
6. **Customer receives email** → Can download pack from email link

---

## Troubleshooting

### Webhook not receiving events

- ✅ Verify endpoint URL is correct: `https://download.harboragent.dev/webhook`
- ✅ Check that `checkout.session.completed` event is selected
- ✅ Ensure webhook is enabled (not paused)
- ✅ Test with a real checkout session

### Email not sending

- ✅ Verify Postmark secrets are set: `wrangler secret list`
- ✅ Check Postmark dashboard for delivery status
- ✅ Verify sender signature is confirmed: `hello@harboragent.dev`
- ✅ Check Worker logs: `wrangler tail`

### Webhook returns errors

- ✅ Check Worker logs: `wrangler tail`
- ✅ Verify all required secrets are set
- ✅ Test webhook endpoint manually with curl (see below)

---

## Manual Webhook Test

You can test the webhook endpoint manually:

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

**Note:** This won't verify the signature, but will test the endpoint logic.

---

## Security Notes

- **Webhook Secret:** Optional but recommended for production
- **Signature Verification:** Currently basic - can be enhanced with full crypto verification
- **HTTPS Only:** Worker only accepts HTTPS requests
- **Email Security:** Download links are personalized and verified per session

---

## Support

- **Stripe Webhooks:** https://dashboard.stripe.com/webhooks
- **Worker Logs:** `wrangler tail`
- **Postmark Dashboard:** https://account.postmarkapp.com/
- **Worker Health:** https://download.harboragent.dev/health

---

**Once webhook is configured, the complete flow will be:**
1. Customer pays → Stripe checkout completes
2. Stripe sends webhook → Worker receives event
3. Worker sends email → Customer gets download link
4. Customer downloads → From email or success page

✅ **All automated!**

