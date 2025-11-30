# Harbor Agent Website - Frontend

This is the React/Vite frontend for harboragent.dev, built with modern web technologies and integrated with Stripe for the Genesis Professional Pack checkout.

## Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **React Router** - Client-side routing
- **Stripe.js** - Payment processing

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn/pnpm

### Installation

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.example .env

# Edit .env with your Stripe keys
# VITE_STRIPE_PUBLISHABLE_KEY=pk_test_...
# VITE_STRIPE_PRICE_ID=price_...
```

### Development

```bash
# Start dev server (runs on http://localhost:3000)
npm run dev
```

### Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Hero.tsx        # Landing page hero section
│   ├── WhatIsGenesis.tsx
│   ├── Features.tsx
│   ├── Pricing.tsx
│   ├── PricingCard.tsx
│   ├── CTA.tsx
│   └── Footer.tsx
├── pages/              # Page components
│   ├── Landing.tsx     # Main landing page
│   └── Success.tsx     # Post-payment success page
├── hooks/              # Custom React hooks
│   └── useStripeCheckout.ts
├── App.tsx             # Main app with routing
├── main.tsx           # Entry point
└── index.css          # Global styles
```

## Stripe Integration

The frontend integrates with Stripe for checkout. Currently, the checkout flow requires a backend API endpoint.

### Current Implementation

The `useStripeCheckout` hook attempts to:
1. Call `/api/create-checkout-session` to create a Stripe checkout session
2. Redirect to Stripe Checkout
3. After payment, Stripe redirects to `/success?session_id={id}`
4. The success page verifies the session with the Cloudflare Worker

### Backend API Required

You need to create a backend endpoint that:

**POST /api/create-checkout-session**

```typescript
// Request body
{
  priceId: string,
  successUrl: string,
  cancelUrl: string
}

// Response
{
  sessionId: string
}
```

The endpoint should:
1. Use your Stripe secret key (server-side only)
2. Create a checkout session:
   ```typescript
   const session = await stripe.checkout.sessions.create({
     mode: 'payment',
     line_items: [{ price: priceId, quantity: 1 }],
     success_url: successUrl,
     cancel_url: cancelUrl,
   })
   ```
3. Return `{ sessionId: session.id }`

### Alternative: Direct Stripe Checkout

If you prefer not to use a backend API, you can modify `useStripeCheckout.ts` to use Stripe's hosted checkout pages directly. However, this requires setting up the checkout session via Stripe Dashboard or using Stripe's payment links.

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `VITE_STRIPE_PUBLISHABLE_KEY` | Stripe publishable key | Yes (for checkout) |
| `VITE_STRIPE_PRICE_ID` | Stripe price ID for Professional Pack | Yes (for checkout) |
| `VITE_WORKER_URL` | Cloudflare Worker URL for download verification | Yes |

## Deployment

### Vercel / Netlify

1. Connect your repository
2. Set environment variables in the dashboard
3. Deploy

### Manual Build

```bash
npm run build
# Upload dist/ folder to your hosting provider
```

## Features

- ✅ Modern, responsive design with Tailwind CSS
- ✅ Genesis Mission explanation
- ✅ Free tier vs Professional Pack comparison
- ✅ Stripe checkout integration (requires backend API)
- ✅ Post-payment success page with download link
- ✅ Cloudflare Worker integration for secure downloads
- ✅ GitHub integration for free tier

## Notes

- The free tier links directly to the GitHub repository
- The Professional Pack requires Stripe checkout
- After payment, users are redirected to the Cloudflare Worker for secure download
- The Worker verifies the Stripe session before allowing download

## Support

For issues or questions:
- Email: support@gentlyventures.com
- GitHub: https://github.com/gentlyventures/harboragent

