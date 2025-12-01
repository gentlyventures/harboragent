# Context Prompt for New GPT-5 Agent: Harbor Agent Project

---

**You're stepping into an already-built project called Harbor Agent, developed collaboratively with another GPT-4/5 instance. Here's a comprehensive context summary so you don't need to re-learn everything:**

---

## 🧠 **Project Summary:**

* **Product**: Harbor Agent is a product line of AI-native compliance & readiness "packs" for emerging government/industry initiatives.

* **Genesis Pack** is Pack #1, focused on helping orgs prepare for U.S. Department of Energy's **Genesis Mission**.

* **ICP**: Technical leaders, AI/ML engineers, compliance/security teams in fast-moving startups and mid-size orgs pursuing federal or public-sector alignment (energy sector, grid operations, applied AI, scientific computing, fusion energy, materials science, climate tech).

* **Company**: Gently Ventures

---

## ✅ **What's Built & Deployed:**

### **Public Site & Infrastructure:**
* **Live site**: [`https://harboragent.dev`](https://harboragent.dev)
* **Repo**: [`github.com/gentlyventures/harboragent`](https://github.com/gentlyventures/harboragent)
* **Download Worker**: `https://download.harboragent.dev` (Cloudflare Worker)
* **Frontend**: React + TypeScript + Vite, deployed on Cloudflare Pages
* **Pricing**: $199 one-time purchase (freemium model: free tier + paid professional pack)

### **Payment & E-commerce:**
* ✅ **Stripe Checkout**: Full integration with redirect flow
* ✅ **Webhook system**: Handles `checkout.session.completed` events
* ✅ **100% off coupon support**: Fixed to handle `payment_status: "paid"` even when `amount_total: 0`
* ✅ **Session verification**: `/verify-session` endpoint with CORS headers for frontend

### **Download & Delivery System:**
* ✅ **Signed/expiring download links**: HMAC-SHA256 signed tokens with 24-hour expiration
  - Uses Web Crypto API (built-in, no external dependencies)
  - Endpoint: `/download-signed?token=...`
  - Automatic token generation in webhook and download handler
  - Fallback to unsigned links if token generation fails

* ✅ **Per-customer LICENSE.txt in ZIP files**: On-demand ZIP generation
  - Fetches base ZIP from `DOWNLOAD_ORIGIN_URL`
  - Adds personalized `LICENSE.txt` with customer email, organization, purchase date, session ID
  - Uses `jszip@3.10.1` library (~50KB)
  - Streams personalized ZIP directly to user (no R2 storage needed)
  - No additional Cloudflare permissions required

* ✅ **Cloudflare R2**: Hosts base ZIP file (read-only access)
* ✅ **Email delivery**: Postmark integration sends personalized HTML emails with download links
  - Email includes signed download link (24-hour expiration)
  - Button styling fixed (white text on blue background)
  - Customer info included in email

### **Technical Stack:**
* **Frontend**: React 18, TypeScript, Tailwind CSS, Vite
* **Worker**: TypeScript, Cloudflare Workers Runtime
* **Payment**: Stripe (Checkout Sessions API)
* **Email**: Postmark
* **Storage**: Cloudflare R2 (object storage)
* **Deployment**: GitHub Actions for automated deployments

### **Project Structure:**
```
/packs/genesis/
  docs/              # Documentation (executive summary, checklist, gap analysis, etc.)
  schemas/           # JSON/YAML schemas
  ide-playbook/      # AI copilot instructions (Cursor, GitHub Copilot, Claude Code)

/workers/
  personalized-download/  # Cloudflare Worker for secure downloads

/src/
  components/        # React components (Hero, Pricing, Features, etc.)
  pages/             # Landing, GenesisPack, Success pages
  hooks/             # Stripe checkout hook

/docs/              # Developer documentation
```

---

## 📋 **Product Content (Genesis Pack):**

The pack includes:

**Free Tier:**
- Executive Summary
- Technical Overview
- Partial Readiness Checklist
- Full Gap Analysis Worksheet
- Security & Governance Guidance
- Roadmap (30/60/90 → 6 → 12 months)
- AI Copilot Playbooks (partial)
- Machine-readable schemas (subset)

**Professional Pack ($199):**
- Full 80-120 item readiness checklist
- Complete AI copilot playbooks (Cursor, GitHub Copilot, Claude Code)
- Secure submission bundle templates
- Reproducibility kits
- Proposal template (fully editable)
- Full schema suite (JSON & YAML)
- 12-month roadmap
- Enterprise documentation templates
- Governance binder structure
- Automation & audit scripts

---

## ✅ **Security Features Implemented:**

* ✅ HMAC-SHA256 signed download tokens (24-hour expiration)
* ✅ Stripe session verification before download
* ✅ Per-customer LICENSE.txt with full license terms
* ✅ Personalized ZIP generation (on-demand, no storage overhead)
* ✅ Webhook signature verification framework (optional)
* ✅ CORS headers on all endpoints
* ✅ Error logging and debugging support
* ✅ Fallback mechanisms for resilience

**Note**: The Worker uses Web Crypto API (no external crypto dependencies). All signing keys are stored as Cloudflare Worker secrets.

---

## 🎯 **Current Status:**

### **Completed Features:**
1. ✅ Signed/expiring download links (HMAC-SHA256, 24-hour expiration)
2. ✅ Per-customer LICENSE.txt injection into ZIP files
3. ✅ On-demand ZIP generation (no R2 write permissions needed)
4. ✅ 100% off coupon handling (verification flow fixed)
5. ✅ Email delivery with personalized links
6. ✅ Frontend success page with verification
7. ✅ Full Stripe checkout flow
8. ✅ Webhook automation

### **Optional Future Enhancements:**
1. File watermarking/fingerprinting (low priority - could add customer ID to metadata)
2. One-time use tokens (single download enforcement) - currently links expire after 24 hours
3. Full webhook signature verification (currently basic structure validation)
4. Analytics tracking (download counts, conversion rates)
5. Multiple pack support (Genesis Pack is Pack #1, future packs planned)

---

## 📝 **Key Files to Know:**

### **For Marketing/Branding Work:**
* `PRODUCT_BRIEF_FOR_MARKETING.md` - Comprehensive product brief with ICP, messaging, positioning
* `BRAND_AUDIT_CONTENT.md` - Brand audit and content guidelines
* `src/pages/Landing.tsx` - Main landing page
* `src/components/` - All UI components

### **For Technical Work:**
* `workers/personalized-download/src/index.ts` - Main Worker code (download logic, webhook handler)
* `src/pages/Success.tsx` - Post-checkout success page
* `src/hooks/useStripeCheckout.ts` - Stripe checkout integration
* `wrangler.toml` - Cloudflare Worker configuration

### **For Product Content:**
* `packs/genesis/docs/` - All pack documentation
* `packs/genesis/ide-playbook/` - AI copilot instructions
* `README.md` - Project overview

### **Documentation & Deployment:**
* `DEPLOYMENT_GUIDE.md` - Deployment instructions
* `STRIPE_WEBHOOK_SETUP.md` - Webhook configuration
* `VERIFICATION_FLOW_AUDIT.md` - Verification flow details
* `IMPLEMENTATION_COMPLETE.md` - Recent implementation status

---

## 🛠️ **How to Help:**

### **For Marketing/Branding Tasks:**
* Review `PRODUCT_BRIEF_FOR_MARKETING.md` for messaging guidelines
* Understand the ICP (engineering leads, ML/data managers, security teams)
* Maintain "developer-ready, not consultant-ready" positioning
* Emphasize AI-native workflows and one-time $199 pricing
* Keep messaging technical and practical (not legal/regulatory)

### **For Technical Tasks:**
* The infrastructure is stable and deployed - avoid rehashing decisions
* Changes should maintain "zero overhead" unless adding clear value
* Worker code is in TypeScript, follows Cloudflare Workers patterns
* Frontend is React + TypeScript + Tailwind CSS
* All secrets are managed via `wrangler secret put`
* Deployment is automated via GitHub Actions

### **For Product Content Tasks:**
* Pack content lives in `/packs/genesis/`
* AI-native by design - all docs are meant to work with AI copilots
* Maintain the tone: engineering-focused, not legal-focused
* Based on publicly available DOE/White House materials
* Includes clear disclaimers: not legal advice, not regulatory guidance

---

## 🚨 **Important Constraints:**

1. **Licensing Model**: Per-organization license ($199 one-time, no subscriptions)
   - LICENSE.txt enforces this in delivered pack
   - Terms: no redistribution, no resale, internal use only

2. **No Legal/Regulatory Claims**: Product is engineering toolkit based on public info
   - Not legal advice
   - Not regulatory guidance
   - Not official DOE document

3. **Technical Focus**: Translation of policy into engineering practice
   - Based on NIST AI RMF principles where relevant
   - Developer-ready artifacts (not PDFs)
   - AI-native workflows (works with Cursor, Copilot, Claude Code)

4. **Future Packs**: Genesis Pack is Pack #1
   - Future packs may include: AI Act, FedRAMP, etc.
   - Architecture should support multiple packs

---

## 📧 **Next Task Context:**

The first actual prompt will be about the marketing brief (`PRODUCT_BRIEF_FOR_MARKETING.md`). This document contains:
- Complete product positioning
- ICP details
- Messaging pillars
- Use cases
- Pricing & delivery model
- Key differentiators
- Marketing messaging for each ICP segment
- Call-to-action framework
- Product positioning statement

**Focus areas for marketing work:**
- Website copy and messaging
- Landing page optimization
- SEO and content marketing
- Email campaigns
- Social media messaging
- Product descriptions

---

## 🔗 **Quick Reference:**

* **Live Site**: https://harboragent.dev
* **Download Worker**: https://download.harboragent.dev
* **Support Email**: support@gentlyventures.com
* **GitHub**: https://github.com/gentlyventures/harboragent
* **Stripe Dashboard**: https://dashboard.stripe.com
* **Cloudflare Dashboard**: https://dash.cloudflare.com
* **Postmark Dashboard**: https://account.postmarkapp.com

---

**Ready to proceed with marketing/branding work on the product brief!**

