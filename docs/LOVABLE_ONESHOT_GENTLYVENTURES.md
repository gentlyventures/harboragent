# Lovable One-Shot Implementation: Harbor Agent Genesis Pack for Gently Ventures

Use this prompt in Lovable after the audit is complete. This prompt implements the Genesis Pack product page following all existing patterns.

---

## One-Shot Implementation Prompt

```
You are implementing the Harbor Agent Genesis Pack product page for Gently Ventures, following the exact patterns and architecture identified in the audit.

## Context Recap

**The Genesis Pack** is a technical readiness toolkit for engineering teams preparing for the DOE Genesis Mission. It includes:
- Free tier (open source on GitHub)
- Professional Pack (paid, includes full checklists, playbooks, templates, etc.)

**Target Audience:** Engineering leads, ML teams, security/compliance teams at organizations preparing for Genesis collaboration.

**Technical Integration:**
- Stripe checkout → Supabase Edge Function → Cloudflare Worker redirect
- Worker URL: https://harboragent-personalized-download.dave-1e3.workers.dev/download?session_id={session_id}

## Implementation Requirements

### 1. Create Product Page

**File:** `src/pages/products/HarborAgent.tsx`

Follow the exact structure and patterns from GPT Extender Lite and Bootloader pages.

**Page Structure:**

```tsx
import { Layout } from '@/components/Layout';
import { HarborAgentHero } from './harbor-agent/HarborAgentHero';
import { TierComparison } from './harbor-agent/TierComparison';
import { HowItWorks } from './harbor-agent/HowItWorks';
import { FAQ } from './harbor-agent/FAQ';
import { supabase } from '@/lib/supabase';

export default function HarborAgent() {
  const handlePurchase = async () => {
    // Call Supabase Edge Function to create Stripe checkout
    const { data, error } = await supabase.functions.invoke('harbor-agent-checkout', {
      body: { tier: 'professional' }
    });
    
    if (data?.url) {
      window.location.href = data.url;
    }
  };

  return (
    <Layout>
      <HarborAgentHero onPurchase={handlePurchase} />
      
      {/* What is Genesis Mission? */}
      <section className="section-padding bg-gradient-to-br from-desert-50 to-sage-50">
        <div className="content-container">
          <h2 className="text-2xl sm:text-3xl lg:text-4xl font-serif font-light mb-6">
            What is the Genesis Mission?
          </h2>
          <p className="text-lg text-warmBrown-700 max-w-3xl">
            The Genesis Mission is a U.S. Department of Energy (DOE) initiative launched in late 2025 
            to unify AI, advanced scientific computing, and cross-disciplinary research. While not a 
            binding regulation, it's a major alignment point for energy-sector vendors, applied AI 
            companies, scientific computing partners, and federal contractors.
          </p>
        </div>
      </section>

      {/* What's in the Pack */}
      <section className="section-padding">
        <div className="content-container">
          <h2 className="text-2xl sm:text-3xl lg:text-4xl font-serif font-light mb-8">
            What's in the Genesis Pack?
          </h2>
          {/* Content about free vs pro tiers */}
        </div>
      </section>

      <TierComparison />
      <HowItWorks />
      <FAQ />
      
      {/* Final CTA - Dark Section */}
      <section className="section-padding bg-charcoal-900 text-white">
        <div className="content-container text-center">
          <h2 className="text-2xl sm:text-3xl lg:text-4xl font-serif font-light mb-6">
            Ready to Prepare Your Team?
          </h2>
          <button 
            onClick={handlePurchase}
            className="premium-button text-lg px-8 py-4"
          >
            Get the Full Pack
          </button>
        </div>
      </section>
    </Layout>
  );
}
```

### 2. Create Hero Component

**File:** `src/pages/products/harbor-agent/HarborAgentHero.tsx`

Follow the exact pattern from GPT Extender Lite hero:

```tsx
export function HarborAgentHero({ onPurchase }: { onPurchase: () => void }) {
  return (
    <section className="section-padding bg-gradient-to-br from-desert-50 to-sage-50">
      <div className="content-container">
        {/* Badge */}
        <div className="inline-block px-4 py-2 bg-sage-100 text-sage-700 rounded-full text-sm font-medium mb-6">
          DOE Genesis Mission Readiness
        </div>

        {/* Title */}
        <h1 className="text-4xl sm:text-5xl lg:text-6xl xl:text-7xl font-serif font-light mb-6">
          Harbor Agent Genesis Pack
        </h1>

        {/* Subtitle */}
        <p className="text-xl text-warmBrown-700 max-w-3xl mb-8">
          AI-native engineering toolkit to help teams prepare for credible collaboration 
          under the DOE Genesis Mission. Includes readiness checklists, copilot playbooks, 
          governance templates, and proposal frameworks.
        </p>

        {/* Social Proof */}
        <div className="mb-8">
          <p className="text-sm text-warmBrown-600 mb-2">Trusted by engineering teams at:</p>
          <div className="flex flex-wrap gap-4 text-sm text-warmBrown-500">
            <span>Energy Sector Companies</span>
            <span>•</span>
            <span>Applied AI Organizations</span>
            <span>•</span>
            <span>Federal Contractors</span>
          </div>
        </div>

        {/* CTAs */}
        <div className="flex flex-col sm:flex-row gap-4">
          <button 
            onClick={onPurchase}
            className="premium-button text-lg px-8 py-4"
          >
            Get the Full Pack
          </button>
          <a 
            href="https://github.com/gentlyventures/harboragent"
            target="_blank"
            rel="noopener noreferrer"
            className="px-8 py-4 bg-white/90 backdrop-blur-sm border border-sage-200/30 rounded-xl text-sage-700 hover:bg-white transition-all duration-300 text-center"
          >
            View Free Resources
          </a>
        </div>
      </div>
    </section>
  );
}
```

### 3. Create Tier Comparison Component

**File:** `src/pages/products/harbor-agent/TierComparison.tsx`

Follow the Bootloader tier pattern with feature comparison:

```tsx
export function TierComparison() {
  const freeFeatures = [
    'Executive Summary',
    'Technical Overview',
    'Partial Readiness Checklist',
    'Gap Analysis Worksheet',
    'Security & Governance Guidance',
    'Roadmap (30/60/90 days)',
    'Partial AI Copilot Playbooks',
  ];

  const proFeatures = [
    'Everything in Free Tier',
    'Full 80-120 Item Checklist',
    'Complete Copilot/Cursor/Claude Code Playbooks',
    'Secure Submission Bundle Templates',
    'Reproducibility Kits',
    'Fully Editable Proposal Template',
    'Full Schema Suite (JSON & YAML)',
    '12-Month Roadmap',
    'Example Partner Pitch Materials',
    'Internal Governance Binder Templates',
    'Enterprise Documentation Templates',
  ];

  return (
    <section className="section-padding bg-white">
      <div className="content-container">
        <h2 className="text-2xl sm:text-3xl lg:text-4xl font-serif font-light mb-12 text-center">
          Free vs Professional Pack
        </h2>
        
        <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
          {/* Free Tier Card */}
          <div className="premium-card p-8">
            <div className="mb-6">
              <div className="inline-block px-4 py-2 bg-sage-100 text-sage-700 rounded-full text-sm font-medium mb-4">
                Free Tier
              </div>
              <h3 className="text-2xl font-serif font-light mb-2">Open Source</h3>
              <p className="text-warmBrown-600">Available on GitHub</p>
            </div>
            <ul className="space-y-3 mb-8">
              {freeFeatures.map((feature, i) => (
                <li key={i} className="flex items-start">
                  <svg className="w-5 h-5 text-sage-600 mr-2 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="text-warmBrown-700">{feature}</span>
                </li>
              ))}
            </ul>
            <a 
              href="https://github.com/gentlyventures/harboragent"
              target="_blank"
              rel="noopener noreferrer"
              className="block w-full px-6 py-3 bg-white border border-sage-200 rounded-xl text-sage-700 hover:bg-sage-50 text-center transition-all duration-300"
            >
              View on GitHub
            </a>
          </div>

          {/* Professional Pack Card */}
          <div className="premium-card p-8 border-2 border-gold-500">
            <div className="mb-6">
              <div className="inline-block px-4 py-2 bg-gold-500/10 text-gold-700 rounded-full text-sm font-medium mb-4">
                Professional Pack
              </div>
              <h3 className="text-2xl font-serif font-light mb-2">Full Toolkit</h3>
              <p className="text-warmBrown-600">Complete readiness framework</p>
            </div>
            <ul className="space-y-3 mb-8">
              {proFeatures.map((feature, i) => (
                <li key={i} className="flex items-start">
                  <svg className="w-5 h-5 text-gold-500 mr-2 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="text-warmBrown-700">{feature}</span>
                </li>
              ))}
            </ul>
            <button 
              onClick={() => {/* Will be passed from parent */}}
              className="premium-button w-full text-lg px-6 py-3"
            >
              Get the Full Pack
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
```

### 4. Create How It Works Component

**File:** `src/pages/products/harbor-agent/HowItWorks.tsx`

```tsx
export function HowItWorks() {
  const steps = [
    {
      number: '1',
      title: 'Purchase the Pack',
      description: 'Get instant access to the complete Genesis readiness toolkit',
    },
    {
      number: '2',
      title: 'Download Your Resources',
      description: 'Receive secure download link with all templates, checklists, and playbooks',
    },
    {
      number: '3',
      title: 'Start Your Readiness Journey',
      description: 'Use AI copilots (Cursor, GitHub Copilot) with the included playbooks to align your systems',
    },
    {
      number: '4',
      title: 'Prepare Your Proposal',
      description: 'Use the editable templates to create credible partner proposals',
    },
  ];

  return (
    <section className="section-padding bg-gradient-to-br from-desert-50 to-sage-50">
      <div className="content-container">
        <h2 className="text-2xl sm:text-3xl lg:text-4xl font-serif font-light mb-12 text-center">
          How It Works
        </h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {steps.map((step, i) => (
            <div key={i} className="premium-card p-6 text-center">
              <div className="w-16 h-16 bg-sage-600 text-white rounded-full flex items-center justify-center text-2xl font-serif font-light mx-auto mb-4">
                {step.number}
              </div>
              <h3 className="text-xl font-serif font-light mb-3">{step.title}</h3>
              <p className="text-warmBrown-600">{step.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
```

### 5. Create FAQ Component

**File:** `src/pages/products/harbor-agent/FAQ.tsx`

```tsx
export function FAQ() {
  const faqs = [
    {
      question: 'What is the Genesis Mission?',
      answer: 'The Genesis Mission is a U.S. Department of Energy initiative to unify AI, advanced scientific computing, and cross-disciplinary research. While not a binding regulation, it creates alignment points for organizations in energy, AI, and scientific computing sectors.',
    },
    {
      question: 'Who is this pack for?',
      answer: 'Engineering leads, ML teams, security/compliance teams, data engineers, and infrastructure teams at organizations preparing for potential Genesis collaboration or proposal cycles.',
    },
    {
      question: 'What\'s the difference between Free and Professional?',
      answer: 'The free tier includes foundational documentation and partial checklists. The Professional Pack includes complete checklists (80-120 items), full AI copilot playbooks, editable templates, governance binders, and proposal frameworks.',
    },
    {
      question: 'How do I use this with AI copilots?',
      answer: 'The pack includes playbooks designed for Cursor, GitHub Copilot, and Claude Code. These give your AI assistant the context and rules needed to help align your codebase with Genesis readiness requirements safely.',
    },
    {
      question: 'Is this legal advice?',
      answer: 'No. This pack is not legal advice, regulatory guidance, or an official DOE document. It is a technical readiness framework based on publicly available information.',
    },
  ];

  return (
    <section className="section-padding">
      <div className="content-container max-w-3xl mx-auto">
        <h2 className="text-2xl sm:text-3xl lg:text-4xl font-serif font-light mb-12 text-center">
          Frequently Asked Questions
        </h2>
        <div className="space-y-6">
          {faqs.map((faq, i) => (
            <div key={i} className="premium-card p-6">
              <h3 className="text-lg font-serif font-light mb-3">{faq.question}</h3>
              <p className="text-warmBrown-700">{faq.answer}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
```

### 6. Create Supabase Edge Function

**File:** `supabase/functions/harbor-agent-checkout/index.ts`

```typescript
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import Stripe from 'https://esm.sh/stripe@14.21.0?target=deno';

const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY') || '', {
  apiVersion: '2023-10-16',
  httpClient: Stripe.createFetchHttpClient(),
});

serve(async (req) => {
  try {
    const { tier } = await req.json();
    
    // Create Stripe Checkout Session
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [
        {
          price: Deno.env.get('GENESIS_PACK_PRICE_ID') || '', // Set this in Supabase secrets
          quantity: 1,
        },
      ],
      mode: 'payment',
      success_url: `https://harboragent-personalized-download.dave-1e3.workers.dev/download?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${req.headers.get('origin')}/products/harbor-agent?canceled=true`,
    });

    return new Response(
      JSON.stringify({ url: session.url }),
      { headers: { 'Content-Type': 'application/json' } }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
});
```

### 7. Update Routing

**File:** `src/App.tsx`

Add route:
```tsx
import HarborAgent from './pages/products/HarborAgent';

// In routes:
<Route path="/products/harbor-agent" element={<HarborAgent />} />
```

### 8. Update Tools Page

**File:** `src/pages/Tools.tsx`

Add to tools array:
```tsx
{
  id: 'harbor-agent',
  name: 'Harbor Agent Genesis Pack',
  description: 'AI-native toolkit for DOE Genesis Mission readiness',
  status: 'Live',
  href: '/products/harbor-agent',
  category: 'Compliance & Readiness',
}
```

### 9. Update Module Registry

**File:** `src/config/moduleRegistry.ts`

Add Harbor Agent module metadata following existing pattern.

## Design System Compliance

- Use `premium-card` class for all cards
- Use `premium-button` class for primary CTAs
- Use `section-padding` for consistent spacing
- Use `content-container` for max-width containers
- Follow color tokens: `sage-600`, `gold-500`, `charcoal-900`, `desert-50`
- Use Playfair Display for headings, Inter for body
- Follow mobile-first responsive patterns

## Content Notes

- Keep tone: calm, expert, minimalist, high-trust
- Avoid hype language
- Focus on clarity and precision
- Target VP/C-suite leaders

## Testing Checklist

- [ ] Page loads at `/products/harbor-agent`
- [ ] Hero section displays correctly
- [ ] Tier comparison shows free vs pro
- [ ] Purchase button triggers Stripe checkout
- [ ] After payment, redirects to Cloudflare Worker
- [ ] Mobile responsive
- [ ] Matches existing design patterns
- [ ] Appears in Tools page listing

Implement this complete solution following all existing patterns exactly.
```

---

## Additional Setup Required

After implementation, you'll need to:

1. **Set Supabase Secrets:**
   - `STRIPE_SECRET_KEY` - Your Stripe secret key
   - `GENESIS_PACK_PRICE_ID` - Stripe Price ID for the Professional Pack

2. **Deploy Edge Function:**
   - The function will auto-deploy when you save it

3. **Test the Flow:**
   - Click "Get the Full Pack"
   - Complete Stripe checkout
   - Verify redirect to Cloudflare Worker
   - Confirm download works

4. **Add to Navigation (Optional):**
   - Consider adding to main nav if this becomes a key product

