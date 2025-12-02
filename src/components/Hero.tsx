interface HeroProps {
  variant?: 'brand' | 'genesis' | 'tax-assist'
}

export default function Hero({ variant = 'genesis' }: HeroProps) {
  if (variant === 'tax-assist') {
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
              Harbor Agent — Pack #2
            </div>
            
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold text-gray-900 mb-6 leading-tight">
              Prepare for the
              <span className="block text-transparent bg-clip-text bg-gradient-to-r from-primary-600 to-accent-600">
                2025 Tax Year
              </span>
            </h1>
            
            <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-3xl mx-auto leading-relaxed">
              The Harbor Agent — AI Tax Assistant Readiness Pack helps Individual Tax Preparers prepare for the 2025 
              filing season with readiness checklists, form processing guides, and AI-native workflows that work 
              directly in your IDE.
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

  if (variant === 'brand') {
    return (
      <section className="relative bg-gradient-to-br from-primary-50 via-white to-accent-50 overflow-hidden">
        {/* Background decoration */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-primary-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob"></div>
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-accent-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-2000"></div>
        </div>

        <div className="relative container-custom section-padding">
          <div className="max-w-5xl mx-auto">
            {/* Trust Indicators - Above the fold */}
            <div className="flex flex-wrap justify-center gap-4 mb-8">
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <svg className="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                <span>Trusted by Engineering Teams</span>
              </div>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <svg className="w-5 h-5 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                  <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd" />
                </svg>
                <span>AI-Native by Design</span>
              </div>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <svg className="w-5 h-5 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                <span>Developer-Ready Artifacts</span>
              </div>
            </div>

            <div className="text-center mb-8">
            <div className="inline-flex items-center px-4 py-2 rounded-full bg-primary-100 text-primary-800 text-sm font-medium mb-6">
              <span className="w-2 h-2 bg-primary-600 rounded-full mr-2 animate-pulse"></span>
              Platform for Compliance & Readiness
            </div>
            
            
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold text-gray-900 mb-6 leading-tight">
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-600 to-accent-600">
                Harbor Agent
              </span>
            </h1>
            
            <p className="text-xl md:text-2xl text-gray-700 mb-4 max-w-3xl mx-auto leading-relaxed font-medium">
              AI-native compliance & readiness platform. Turn complex regulations into developer-ready tools your team can actually use.
            </p>
            
            <p className="text-lg text-gray-600 mb-8 max-w-3xl mx-auto leading-relaxed">
              Each Harbor Agent pack provides complete toolkits—checklists, templates, AI playbooks, and workflows—for preparing your team for specific government and industry initiatives.
            </p>
          </div>

          {/* Pack CTAs - Prominent placement */}
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100 mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
                Explore Our Packs
              </h2>
              <div className="grid md:grid-cols-2 gap-6">
                <a
                  href="/packs/genesis-mission"
                  className="group bg-gradient-to-br from-primary-50 to-primary-100 p-6 rounded-xl border-2 border-primary-200 hover:border-primary-400 transition-all duration-200 hover:shadow-lg"
                >
                  <div className="flex items-center justify-between mb-3">
                    <span className="px-3 py-1 bg-primary-600 text-white text-xs font-semibold rounded-full">
                      Pack #1
                    </span>
                    <svg className="w-5 h-5 text-primary-600 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">Genesis Mission Pack</h3>
                  <p className="text-gray-600 mb-4">DOE Genesis Mission readiness for engineering teams</p>
                  <div className="flex items-center text-primary-600 font-semibold">
                    <span>View Pack</span>
                  </div>
                </a>

                <a
                  href="/packs/tax-assist"
                  className="group bg-gradient-to-br from-accent-50 to-accent-100 p-6 rounded-xl border-2 border-accent-200 hover:border-accent-400 transition-all duration-200 hover:shadow-lg"
                >
                  <div className="flex items-center justify-between mb-3">
                    <span className="px-3 py-1 bg-accent-600 text-white text-xs font-semibold rounded-full">
                      Pack #2
                    </span>
                    <svg className="w-5 h-5 text-accent-600 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">Tax Assist Pack</h3>
                  <p className="text-gray-600 mb-4">2025 Tax Year readiness for Individual Tax Preparers</p>
                  <div className="flex items-center text-accent-600 font-semibold">
                    <span>View Pack</span>
                  </div>
                </a>
              </div>
            </div>

            <div className="text-center">
              <a
                href="https://github.com/gentlyventures/harboragent"
                target="_blank"
                rel="noopener noreferrer"
                className="btn-secondary text-lg px-8 py-4 inline-flex items-center space-x-2"
              >
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 0C4.477 0 0 4.484 0 10.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0110 4.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.203 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.942.359.31.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482C17.146 18.197 20 14.442 20 10.017 20 4.484 15.522 0 10 0z" clipRule="evenodd" />
                </svg>
                <span>Free Tier on GitHub</span>
              </a>
            </div>
          </div>
          </div>
        </div>
      </section>
    )
  }

  // Genesis variant (default)
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
            Harbor Agent — Pack #1
          </div>
          
          <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold text-gray-900 mb-6 leading-tight">
            Prepare for the
            <span className="block text-transparent bg-clip-text bg-gradient-to-r from-primary-600 to-accent-600">
              Genesis Mission
            </span>
          </h1>
          
          <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-3xl mx-auto leading-relaxed">
            The Harbor Agent — Genesis Mission Readiness Pack helps engineering, ML, and security teams prepare for 
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

