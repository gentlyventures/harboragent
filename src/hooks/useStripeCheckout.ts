import { useState } from 'react'
import { loadStripe } from '@stripe/stripe-js'

const STRIPE_PUBLISHABLE_KEY = import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY || ''
const STRIPE_PRICE_ID = import.meta.env.VITE_STRIPE_PRICE_ID || ''

export function useStripeCheckout() {
  const [isLoading, setIsLoading] = useState(false)

  const handleCheckout = async () => {
    if (!STRIPE_PUBLISHABLE_KEY || !STRIPE_PRICE_ID) {
      alert('Stripe configuration is missing. Please set VITE_STRIPE_PUBLISHABLE_KEY and VITE_STRIPE_PRICE_ID environment variables.')
      return
    }

    setIsLoading(true)

    try {
      const stripe = await loadStripe(STRIPE_PUBLISHABLE_KEY)
      
      if (!stripe) {
        throw new Error('Failed to load Stripe')
      }

      // Create checkout session via your backend API
      // For now, we'll use Stripe Checkout directly with the price ID
      // In production, you should create a session via your backend
      const response = await fetch('/api/create-checkout-session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          priceId: STRIPE_PRICE_ID,
          successUrl: `${window.location.origin}/success?session_id={CHECKOUT_SESSION_ID}`,
          cancelUrl: `${window.location.origin}/#pricing`,
        }),
      })

      if (response.ok) {
        const { sessionId } = await response.json()
        const result = await stripe.redirectToCheckout({ sessionId })
        
        if (result.error) {
          throw new Error(result.error.message)
        }
      } else {
        // Backend API not available - provide helpful error message
        const errorText = await response.text().catch(() => 'Unknown error')
        console.error('Backend API error:', errorText)
        throw new Error(
          'Checkout service is currently unavailable. Please contact support@gentlyventures.com to complete your purchase.'
        )
      }
    } catch (error) {
      console.error('Checkout error:', error)
      alert('Unable to start checkout. Please contact support@gentlyventures.com')
    } finally {
      setIsLoading(false)
    }
  }

  return {
    handleCheckout,
    isLoading,
  }
}

