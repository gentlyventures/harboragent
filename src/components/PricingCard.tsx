import { useStripeCheckout } from '../hooks/useStripeCheckout'

interface PricingCardProps {
  title: string
  price: string
  description: string
  features: string[]
  ctaText: string
  ctaLink: string
  isPrimary: boolean
  isProfessional?: boolean
}

export default function PricingCard({
  title,
  price,
  description,
  features,
  ctaText,
  ctaLink,
  isPrimary,
  isProfessional = false
}: PricingCardProps) {
  const { handleCheckout, isLoading } = useStripeCheckout()

  const handleClick = (e: React.MouseEvent) => {
    if (isProfessional) {
      e.preventDefault()
      handleCheckout()
    }
  }

  return (
    <div
      className={`relative rounded-2xl p-8 ${
        isPrimary
          ? 'bg-gradient-to-br from-primary-600 to-primary-700 text-white shadow-xl scale-105'
          : 'bg-white border-2 border-gray-200 text-gray-900 shadow-sm'
      }`}
    >
      {isPrimary && (
        <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
          <span className="bg-accent-500 text-white px-4 py-1 rounded-full text-sm font-semibold">
            Most Popular
          </span>
        </div>
      )}
      
      <div className="mb-6">
        <h3 className={`text-2xl font-bold mb-2 ${isPrimary ? 'text-white' : 'text-gray-900'}`}>
          {title}
        </h3>
        <div className="flex items-baseline mb-2">
          <span className={`text-4xl font-bold ${isPrimary ? 'text-white' : 'text-gray-900'}`}>
            {price}
          </span>
        </div>
        <p className={`text-sm ${isPrimary ? 'text-primary-100' : 'text-gray-600'}`}>
          {description}
        </p>
      </div>
      
      <ul className="space-y-3 mb-8">
        {features.map((feature, index) => (
          <li key={index} className="flex items-start">
            <span className={`mr-3 ${isPrimary ? 'text-primary-200' : 'text-primary-600'}`}>
              ✓
            </span>
            <span className={isPrimary ? 'text-primary-50' : 'text-gray-700'}>
              {feature}
            </span>
          </li>
        ))}
      </ul>
      
      {isProfessional ? (
        <button
          onClick={handleClick}
          disabled={isLoading}
          className={`w-full py-3 px-6 rounded-lg font-semibold transition-colors duration-200 ${
            isPrimary
              ? 'bg-white text-primary-600 hover:bg-primary-50'
              : 'bg-primary-600 text-white hover:bg-primary-700'
          } ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          {isLoading ? 'Processing...' : ctaText}
        </button>
      ) : (
        <a
          href={ctaLink}
          target="_blank"
          rel="noopener noreferrer"
          className={`block w-full text-center py-3 px-6 rounded-lg font-semibold transition-colors duration-200 ${
            isPrimary
              ? 'bg-white text-primary-600 hover:bg-primary-50'
              : 'bg-primary-600 text-white hover:bg-primary-700'
          }`}
        >
          {ctaText}
        </a>
      )}
    </div>
  )
}

