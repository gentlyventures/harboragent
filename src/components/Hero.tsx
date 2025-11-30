import { Link } from 'react-router-dom'

export default function Hero() {
  return (
    <section className="relative bg-gradient-to-br from-primary-50 via-white to-accent-50 overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-primary-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-accent-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-2000"></div>
      </div>

      <div className="relative container-custom section-padding">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center px-4 py-2 rounded-full bg-primary-100 text-primary-800 text-sm font-medium mb-6">
            <span className="w-2 h-2 bg-primary-600 rounded-full mr-2 animate-pulse"></span>
            AI-Native Engineering Tools
          </div>
          
          <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold text-gray-900 mb-6 leading-tight">
            Prepare for the
            <span className="block text-transparent bg-clip-text bg-gradient-to-r from-primary-600 to-accent-600">
              Genesis Mission
            </span>
          </h1>
          
          <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-3xl mx-auto leading-relaxed">
            The Harbor Agent Genesis Pack helps engineering, ML, and security teams prepare for 
            credible collaboration under the U.S. Department of Energy's Genesis Mission—using 
            AI-native workflows that work directly in your IDE.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <a
              href="https://github.com/gentlyventures/harboragent"
              target="_blank"
              rel="noopener noreferrer"
              className="btn-primary text-lg px-8 py-4"
            >
              Get Free Tier on GitHub
            </a>
            <a
              href="#pricing"
              className="btn-secondary text-lg px-8 py-4"
            >
              View Professional Pack
            </a>
          </div>
          
          <p className="mt-6 text-sm text-gray-500">
            Free tier available now • Professional Pack includes full toolkits
          </p>
        </div>
      </div>
    </section>
  )
}

