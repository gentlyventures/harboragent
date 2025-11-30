# Quick Start Guide - Harbor Agent Website

## 🚀 Getting the Frontend Running

### 1. Install Dependencies

```bash
npm install
```

### 2. Set Up Environment Variables

Copy the template and add your Stripe keys:

```bash
cp env.template .env
```

Edit `.env` and add:
- `VITE_STRIPE_PUBLISHABLE_KEY` - From Stripe Dashboard
- `VITE_STRIPE_PRICE_ID` - Your Professional Pack price ID
- `VITE_WORKER_URL` - Already set to the default Cloudflare Worker

### 3. Start Development Server

```bash
npm run dev
```

The site will open at `http://localhost:3000`

## 📋 What Was Built

### ✅ Complete React/Vite Application
- Modern React 18 with TypeScript
- Vite for fast development and builds
- Tailwind CSS for styling
- React Router for navigation

### ✅ Landing Page Components
- **Hero Section** - Eye-catching introduction with gradient background
- **What is Genesis** - Explains the DOE Genesis Mission
- **Features** - Shows what problems the pack solves
- **Pricing** - Free tier vs Professional Pack comparison
- **CTA Section** - Call-to-action for purchasing
- **Footer** - Links and company information

### ✅ Stripe Integration
- Checkout flow ready (requires backend API endpoint)
- Success page with download verification
- Cloudflare Worker integration for secure downloads

### ✅ Success Page
- Verifies Stripe session with Cloudflare Worker
- Provides secure download link
- Shows next steps for users

## 🔧 Next Steps

### Backend API Required

The Stripe checkout currently expects a backend API at `/api/create-checkout-session`. You have two options:

**Option 1: Create Backend API** (Recommended)
- Create an endpoint that creates Stripe checkout sessions
- See `FRONTEND_README.md` for API specification

**Option 2: Use Stripe Payment Links**
- Create a payment link in Stripe Dashboard
- Update `useStripeCheckout.ts` to redirect to the payment link
- Simpler but less customizable

### Deployment

**Vercel/Netlify:**
1. Connect repository
2. Set environment variables
3. Deploy

**Manual:**
```bash
npm run build
# Upload dist/ folder to your hosting
```

## 📁 Project Structure

```
harbor_agent/
├── src/
│   ├── components/     # UI components
│   ├── pages/         # Page components
│   ├── hooks/         # Custom hooks
│   └── ...
├── index.html
├── package.json
├── vite.config.ts
└── tailwind.config.js
```

## 🎨 Design Features

- Modern gradient backgrounds
- Responsive design (mobile-first)
- Smooth animations
- Professional color scheme (blue/purple)
- Accessible components

## 📚 Documentation

- `FRONTEND_README.md` - Detailed frontend documentation
- `env.template` - Environment variable template
- Component files include inline documentation

## 🐛 Troubleshooting

**Stripe checkout not working?**
- Check environment variables are set
- Verify backend API endpoint exists (or use payment links)
- Check browser console for errors

**Build errors?**
- Run `npm install` again
- Check Node.js version (18+)
- Clear `node_modules` and reinstall

## 📞 Support

- Email: support@gentlyventures.com
- GitHub: https://github.com/gentlyventures/harboragent

