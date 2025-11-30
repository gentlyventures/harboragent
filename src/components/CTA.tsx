import { useStripeCheckout } from '../hooks/useStripeCheckout'

export default function CTA() {
  const { handleCheckout, isLoading } = useStripeCheckout()

  return (
    <section className="section-padding bg-gradient-to-r from-primary-600 to-accent-600">
      <div className="container-custom">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Ready to Prepare for Genesis?
          </h2>
          <p className="text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
            Get the complete Professional Pack with full toolkits, templates, and enterprise-ready 
            documentation to accelerate your Genesis readiness.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={handleCheckout}
              disabled={isLoading}
              className="btn-primary bg-white text-primary-600 hover:bg-primary-50 text-lg px-8 py-4 disabled:opacity-50"
            >
              {isLoading ? 'Processing...' : 'Get Professional Pack'}
            </button>
            <a
              href="https://github.com/gentlyventures/harboragent"
              target="_blank"
              rel="noopener noreferrer"
              className="btn-secondary border-white text-white hover:bg-white/10 text-lg px-8 py-4"
            >
              Start with Free Tier
            </a>
          </div>
          <p className="mt-6 text-sm text-primary-200">
            Questions? Contact us at support@gentlyventures.com
          </p>
        </div>
      </div>
    </section>
  )
}

