import { useEffect, useState } from 'react'
import { useSearchParams, Link } from 'react-router-dom'

export default function Success() {
  const [searchParams] = useSearchParams()
  const [isVerifying, setIsVerifying] = useState(true)
  const [isValid, setIsValid] = useState(false)
  const sessionId = searchParams.get('session_id')

  useEffect(() => {
    const verifySession = async () => {
      if (!sessionId) {
        setIsVerifying(false)
        setIsValid(false)
        return
      }

      try {
        const workerUrl = import.meta.env.VITE_WORKER_URL || 'https://harboragent-personalized-download.dave-1e3.workers.dev'
        const response = await fetch(`${workerUrl}/verify-session`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ session_id: sessionId }),
        })

        const data = await response.json()
        setIsValid(data.valid)
      } catch (error) {
        console.error('Verification error:', error)
        setIsValid(false)
      } finally {
        setIsVerifying(false)
      }
    }

    verifySession()
  }, [sessionId])

  if (isVerifying) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Verifying your purchase...</p>
        </div>
      </div>
    )
  }

  if (!isValid) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="max-w-md mx-auto text-center px-4">
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-6">
            <p className="font-semibold">Verification Failed</p>
            <p className="text-sm mt-2">
              We couldn't verify your purchase. Please contact support if you completed a payment.
            </p>
          </div>
          <Link
            to="/"
            className="btn-primary"
          >
            Return to Home
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-accent-50">
      <div className="container-custom py-24">
        <div className="max-w-2xl mx-auto text-center">
          <div className="mb-8">
            <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg
                className="w-12 h-12 text-green-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M5 13l4 4L19 7"
                />
              </svg>
            </div>
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              Thank You for Your Purchase!
            </h1>
            <p className="text-xl text-gray-600 mb-8">
              Your Genesis Professional Pack is ready to download.
            </p>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">
              Download Your Pack
            </h2>
            <p className="text-gray-600 mb-6">
              Click the button below to securely download your Genesis Professional Pack. 
              The download link is personalized and verified.
            </p>
            {sessionId && (
              <a
                href={`https://harboragent-personalized-download.dave-1e3.workers.dev/download?session_id=${sessionId}`}
                className="btn-primary text-lg px-8 py-4 inline-block"
              >
                Download Professional Pack
              </a>
            )}
          </div>

          <div className="bg-primary-50 border border-primary-200 rounded-lg p-6 mb-8 text-left">
            <h3 className="font-semibold text-gray-900 mb-3">What's Next?</h3>
            <ol className="space-y-2 text-gray-700 list-decimal list-inside">
              <li>Download and extract the Professional Pack</li>
              <li>Review the full checklist and playbooks</li>
              <li>Start with the gap analysis worksheet</li>
              <li>Use the AI copilot playbooks in your IDE</li>
              <li>Follow the 12-month roadmap for alignment</li>
            </ol>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/"
              className="btn-secondary"
            >
              Return to Home
            </Link>
            <a
              href="mailto:support@gentlyventures.com"
              className="btn-primary"
            >
              Contact Support
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}

