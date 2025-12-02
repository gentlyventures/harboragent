import { Link } from 'react-router-dom'

export default function Header() {
  return (
    <header className="sticky top-0 z-50 bg-white border-b border-gray-200 shadow-sm">
      <div className="container-custom">
        <div className="flex items-center justify-between h-16">
          {/* Logo placeholder - will be replaced with actual logo */}
          <Link to="/" className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-primary-600 to-accent-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">HA</span>
            </div>
            <span className="text-xl font-bold text-gray-900">Harbor Agent</span>
          </Link>

          {/* Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <Link
              to="/packs/genesis-mission"
              className="text-gray-700 hover:text-primary-600 transition-colors font-medium"
            >
              Genesis Pack
            </Link>
            <Link
              to="/packs/tax-assist"
              className="text-gray-700 hover:text-primary-600 transition-colors font-medium"
            >
              Tax Assist Pack
            </Link>
            <a
              href="https://github.com/gentlyventures/harboragent"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-700 hover:text-primary-600 transition-colors font-medium"
            >
              GitHub
            </a>
          </nav>

          {/* Mobile menu button */}
          <button className="md:hidden text-gray-700">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>
    </header>
  )
}

