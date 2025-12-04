import { useState, useEffect } from 'react'
import Header from '../components/Header'
import Footer from '../components/Footer'
import PageMeta from '../components/PageMeta'
import AdminLogin from '../components/AdminLogin'

// API base URL - configurable via environment variable
// Dev: defaults to http://127.0.0.1:8000 (local Harbor Ops API)
// Prod: set VITE_HARBOR_OPS_API_URL in Cloudflare Pages env vars (e.g., https://api.harboragent.dev)
const API_BASE_URL =
  import.meta.env.VITE_HARBOR_OPS_API_URL || "http://127.0.0.1:8000"

// Type definition matching PackLifecycle from pack-crm
type PackStage = 'idea' | 'validation' | 'scoring' | 'deep_dive' | 'build' | 'published'
type StageStatus = 'not_started' | 'in_progress' | 'completed'

interface PackGateDecisionNotes {
  validation?: string
  scoring?: string
  deep_dive?: string
}

interface PackCRM {
  ideaNotes: string | null
  icpSummary: string | null
  primaryPainPoints: string[]
  valueHypothesis: string | null
  pricingNotes: string | null
  competitionNotes: string | null
  gateDecisionNotes: PackGateDecisionNotes
}

interface PackLifecycle {
  slug: string
  name: string
  packNumber: number
  currentStage: PackStage
  stages: Record<PackStage, {
    status: StageStatus
    startedAt?: string
    completedAt?: string
    score?: number
    gate?: 'pass' | 'fail'
    researchArtifacts?: string[]
    publishedAt?: string
  }>
  metadata: {
    regulationName?: string
    targetAudience?: string[]
    price?: number
    createdAt: string
    updatedAt: string
  }
  research: {
    researchCompleted: boolean
    researchArtifacts: string[]
    researchNotes?: string
  }
  deployment: {
    frontendDeployed: boolean
    workerDeployed: boolean
    stripeConfigured: boolean
    r2Uploaded: boolean
  }
  crm: PackCRM
}

interface RevenueSummary {
  totalLeads: number
  totalSales?: number | null
  packs: Array<{
    slug: string
    leads: number
    sales: number
  }>
  note?: string | null
}

function getStageBadgeColor(stage: string): string {
  switch (stage) {
    case 'published':
      return 'bg-green-100 text-green-800'
    case 'build':
      return 'bg-blue-100 text-blue-800'
    case 'deep_dive':
      return 'bg-purple-100 text-purple-800'
    case 'scoring':
      return 'bg-yellow-100 text-yellow-800'
    case 'validation':
      return 'bg-orange-100 text-orange-800'
    case 'idea':
      return 'bg-gray-100 text-gray-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

function formatPrice(cents: number | undefined): string {
  if (!cents) return '—'
  return `$${(cents / 100).toFixed(2)}`
}

function formatDate(dateStr: string): string {
  try {
    return new Date(dateStr).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    })
  } catch {
    return dateStr
  }
}

function truncateText(text: string | null, maxLength: number): string {
  if (!text) return '—'
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

function getFileName(path: string): string {
  return path.split('/').pop() || path
}

interface PackCardProps {
  pack: PackLifecycle
  onRunResearch: (slug: string) => Promise<void>
}

function PackCard({ pack, onRunResearch }: PackCardProps) {
  const [isExpanded, setIsExpanded] = useState(false)
  const [isRunningResearch, setIsRunningResearch] = useState(false)
  const [researchMessage, setResearchMessage] = useState<string | null>(null)

  const handleRunResearch = async () => {
    setIsRunningResearch(true)
    setResearchMessage(null)
    try {
      await onRunResearch(pack.slug)
      setResearchMessage('Research pipeline completed successfully!')
      setTimeout(() => setResearchMessage(null), 5000)
    } catch (error) {
      setResearchMessage(`Error: ${error instanceof Error ? error.message : 'Unknown error'}`)
    } finally {
      setIsRunningResearch(false)
    }
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      {/* Header */}
      <div
        className="p-6 cursor-pointer hover:bg-gray-50 transition-colors"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-sm font-medium bg-primary-100 text-primary-800">
                #{pack.packNumber}
              </span>
              <h3 className="text-xl font-bold text-gray-900">{pack.name}</h3>
              <span
                className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStageBadgeColor(
                  pack.currentStage
                )}`}
              >
                {pack.currentStage.replace('_', ' ')}
              </span>
            </div>
            <p className="text-sm text-gray-600 mb-2">{pack.metadata.regulationName || '—'}</p>
            <div className="flex items-center gap-4 text-sm text-gray-500">
              <span>
                <code className="bg-gray-100 px-2 py-0.5 rounded text-xs">{pack.slug}</code>
              </span>
              {pack.metadata.price && <span>{formatPrice(pack.metadata.price)}</span>}
              <span>Updated: {formatDate(pack.metadata.updatedAt)}</span>
            </div>
          </div>
          <div className="ml-4">
            <svg
              className={`w-5 h-5 text-gray-400 transition-transform ${isExpanded ? 'rotate-180' : ''}`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </div>
      </div>

      {/* Expanded Content */}
      {isExpanded && (
        <div className="border-t border-gray-200 p-6 space-y-6">
          {/* Run Research Button - Only show for early-stage packs */}
          {pack.currentStage === 'idea' || pack.currentStage === 'validation' || pack.currentStage === 'scoring' ? (
            <div className="flex items-center justify-between p-4 bg-blue-50 rounded-lg border border-blue-200">
              <div>
                <h4 className="text-sm font-semibold text-blue-900 mb-1">Initial Research Pipeline</h4>
                <p className="text-xs text-blue-700">
                  Run the complete research pipeline (validation → scoring → deep dive) for new packs
                </p>
              </div>
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  handleRunResearch()
                }}
                disabled={isRunningResearch}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  isRunningResearch
                    ? 'bg-gray-300 text-gray-600 cursor-not-allowed'
                    : 'bg-blue-600 text-white hover:bg-blue-700'
                }`}
              >
                {isRunningResearch ? 'Running...' : 'Run Research Pipeline'}
              </button>
            </div>
          ) : (
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg border border-gray-200">
              <div>
                <h4 className="text-sm font-semibold text-gray-900 mb-1">Pack Updates</h4>
                <p className="text-xs text-gray-600">
                  Weekly automated checks for regulation changes, market updates, and user feedback are handled by the orchestrator cron job.
                </p>
              </div>
              <span className="text-xs text-gray-500 italic">Automated</span>
            </div>
          )}

          {researchMessage && (
            <div
              className={`p-3 rounded-lg text-sm ${
                researchMessage.startsWith('Error')
                  ? 'bg-red-50 text-red-800 border border-red-200'
                  : 'bg-green-50 text-green-800 border border-green-200'
              }`}
            >
              {researchMessage}
            </div>
          )}

          {/* Core Details */}
          <div>
            <h4 className="text-sm font-semibold text-gray-900 mb-3 uppercase tracking-wide">
              Core Details
            </h4>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-gray-600">Pack Number:</span>
                <span className="ml-2 font-medium text-gray-900">#{pack.packNumber}</span>
              </div>
              <div>
                <span className="text-gray-600">Slug:</span>
                <code className="ml-2 bg-gray-100 px-2 py-0.5 rounded text-xs">{pack.slug}</code>
              </div>
              <div>
                <span className="text-gray-600">Current Stage:</span>
                <span
                  className={`ml-2 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${getStageBadgeColor(
                    pack.currentStage
                  )}`}
                >
                  {pack.currentStage.replace('_', ' ')}
                </span>
              </div>
              <div>
                <span className="text-gray-600">Price:</span>
                <span className="ml-2 font-medium text-gray-900">{formatPrice(pack.metadata.price)}</span>
              </div>
            </div>
          </div>

          {/* CRM Overview */}
          <div>
            <h4 className="text-sm font-semibold text-gray-900 mb-3 uppercase tracking-wide">
              CRM Overview
            </h4>
            <div className="space-y-4 text-sm">
              <div>
                <div className="text-gray-600 font-medium mb-1">Idea Notes:</div>
                <div className="text-gray-900 bg-gray-50 p-3 rounded-lg">
                  {truncateText(pack.crm.ideaNotes, 200)}
                </div>
              </div>
              <div>
                <div className="text-gray-600 font-medium mb-1">ICP Summary:</div>
                <div className="text-gray-900">{pack.crm.icpSummary || '—'}</div>
              </div>
              {pack.crm.primaryPainPoints.length > 0 && (
                <div>
                  <div className="text-gray-600 font-medium mb-1">Primary Pain Points:</div>
                  <ul className="list-disc list-inside text-gray-900 space-y-1">
                    {pack.crm.primaryPainPoints.map((pain, idx) => (
                      <li key={idx}>{pain}</li>
                    ))}
                  </ul>
                </div>
              )}
              <div>
                <div className="text-gray-600 font-medium mb-1">Value Hypothesis:</div>
                <div className="text-gray-900">{pack.crm.valueHypothesis || '—'}</div>
              </div>
              <div>
                <div className="text-gray-600 font-medium mb-1">Pricing Notes:</div>
                <div className="text-gray-900">{pack.crm.pricingNotes || '—'}</div>
              </div>
              <div>
                <div className="text-gray-600 font-medium mb-1">Competition Notes:</div>
                <div className="text-gray-900">{pack.crm.competitionNotes || '—'}</div>
              </div>
            </div>
          </div>

          {/* Lifecycle */}
          <div>
            <h4 className="text-sm font-semibold text-gray-900 mb-3 uppercase tracking-wide">
              Lifecycle
            </h4>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-gray-600">Research Completed:</span>
                <span className={`ml-2 font-medium ${pack.research.researchCompleted ? 'text-green-600' : 'text-gray-400'}`}>
                  {pack.research.researchCompleted ? 'Yes' : 'No'}
                </span>
              </div>
              <div>
                <span className="text-gray-600">Research Artifacts:</span>
                <span className="ml-2 text-gray-900">
                  {pack.research.researchArtifacts.length > 0
                    ? pack.research.researchArtifacts.map(getFileName).join(', ')
                    : 'None'}
                </span>
              </div>
            </div>
          </div>

          {/* Gate Decisions */}
          {(pack.crm.gateDecisionNotes.validation ||
            pack.crm.gateDecisionNotes.scoring ||
            pack.crm.gateDecisionNotes.deep_dive) && (
            <div>
              <h4 className="text-sm font-semibold text-gray-900 mb-3 uppercase tracking-wide">
                Gate Decisions
              </h4>
              <div className="space-y-3 text-sm">
                {pack.crm.gateDecisionNotes.validation && (
                  <div>
                    <div className="text-gray-600 font-medium mb-1">Validation:</div>
                    <div className="text-gray-900 bg-gray-50 p-3 rounded-lg">
                      {pack.crm.gateDecisionNotes.validation}
                    </div>
                  </div>
                )}
                {pack.crm.gateDecisionNotes.scoring && (
                  <div>
                    <div className="text-gray-600 font-medium mb-1">Scoring:</div>
                    <div className="text-gray-900 bg-gray-50 p-3 rounded-lg">
                      {pack.crm.gateDecisionNotes.scoring}
                    </div>
                  </div>
                )}
                {pack.crm.gateDecisionNotes.deep_dive && (
                  <div>
                    <div className="text-gray-600 font-medium mb-1">Deep Dive:</div>
                    <div className="text-gray-900 bg-gray-50 p-3 rounded-lg">
                      {pack.crm.gateDecisionNotes.deep_dive}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Deployment Status */}
          <div>
            <h4 className="text-sm font-semibold text-gray-900 mb-3 uppercase tracking-wide">
              Deployment Status
            </h4>
            <div className="grid grid-cols-2 gap-2">
              <span
                className={`inline-flex items-center px-3 py-1.5 rounded text-sm font-medium ${
                  pack.deployment.frontendDeployed
                    ? 'bg-green-100 text-green-800'
                    : 'bg-gray-100 text-gray-600'
                }`}
              >
                {pack.deployment.frontendDeployed ? '✓' : '○'} Frontend
              </span>
              <span
                className={`inline-flex items-center px-3 py-1.5 rounded text-sm font-medium ${
                  pack.deployment.workerDeployed
                    ? 'bg-green-100 text-green-800'
                    : 'bg-gray-100 text-gray-600'
                }`}
              >
                {pack.deployment.workerDeployed ? '✓' : '○'} Worker
              </span>
              <span
                className={`inline-flex items-center px-3 py-1.5 rounded text-sm font-medium ${
                  pack.deployment.stripeConfigured
                    ? 'bg-green-100 text-green-800'
                    : 'bg-gray-100 text-gray-600'
                }`}
              >
                {pack.deployment.stripeConfigured ? '✓' : '○'} Stripe
              </span>
              <span
                className={`inline-flex items-center px-3 py-1.5 rounded text-sm font-medium ${
                  pack.deployment.r2Uploaded
                    ? 'bg-green-100 text-green-800'
                    : 'bg-gray-100 text-gray-600'
                }`}
              >
                {pack.deployment.r2Uploaded ? '✓' : '○'} R2
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

interface NewIdeaFormData {
  name: string
  ideaNotes: string
}

function NewIdeaForm({ onSuccess }: { onSuccess: () => void }) {
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [formData, setFormData] = useState<NewIdeaFormData>({
    name: '',
    ideaNotes: '',
  })
  const [isRecording, setIsRecording] = useState(false)
  const [isTranscribing, setIsTranscribing] = useState(false)
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null)

  // Auto-generate slug from name
  const generateSlug = (name: string): string => {
    return name
      .toLowerCase()
      .trim()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/(^-|-$)/g, '') || `idea-${Date.now()}`
  }

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const recorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm;codecs=opus',
      })
      
      const chunks: Blob[] = []
      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunks.push(event.data)
        }
      }
      
      recorder.onstop = async () => {
        const audioBlob = new Blob(chunks, { type: 'audio/webm' })
        await transcribeAudio(audioBlob)
        stream.getTracks().forEach((track) => track.stop())
      }
      
      recorder.start()
      setMediaRecorder(recorder)
      setIsRecording(true)
    } catch (err) {
      setError('Failed to access microphone. Please check permissions.')
      console.error('Error accessing microphone:', err)
    }
  }

  const stopRecording = () => {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
      mediaRecorder.stop()
      setIsRecording(false)
    }
  }

  const transcribeAudio = async (audioBlob: Blob) => {
    setIsTranscribing(true)
    setError(null)
    
    try {
      // Convert to format Whisper accepts (mp3, wav, etc.)
      // For now, send as webm - Whisper supports it
      const formData = new FormData()
      formData.append('audio_file', audioBlob, 'recording.webm')
      
      const response = await fetch(`${API_BASE_URL}/api/transcribe`, {
        method: 'POST',
        body: formData,
      })
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Transcription failed' }))
        throw new Error(errorData.detail || `HTTP ${response.status}`)
      }
      
      const data = await response.json()
      const transcript = data.text
      
      // Append transcript to ideaNotes
      setFormData((prev) => ({
        ...prev,
        ideaNotes: prev.ideaNotes
          ? prev.ideaNotes + '\n\n' + transcript
          : transcript,
      }))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to transcribe audio')
      console.error('Transcription error:', err)
    } finally {
      setIsTranscribing(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    setError(null)

    try {
      const name = formData.name.trim()
      const ideaNotes = formData.ideaNotes.trim()

      if (!name || !ideaNotes) {
        throw new Error('Please provide a pack name and idea notes')
      }

      const slug = generateSlug(name)

      const response = await fetch(`${API_BASE_URL}/api/packs`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          slug,
          name,
          ideaNotes,
          icpSummary: null,
          primaryPainPoints: null,
          valueHypothesis: null,
          pricingNotes: null,
          competitionNotes: null,
        }),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }))
        throw new Error(errorData.detail || `HTTP ${response.status}`)
      }

      // Clear form
      setFormData({
        name: '',
        ideaNotes: '',
      })

      // Notify parent to refresh
      onSuccess()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create pack')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">New Idea</h2>
      <p className="text-sm text-gray-600 mb-4">
        Brain dump your idea here — just like you do in ChatGPT. Type or use voice to capture your thoughts.
      </p>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Pack Name <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            required
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder="e.g., AI Safety Officer Readiness Pack"
          />
          <p className="mt-1 text-xs text-gray-500">
            Slug will be auto-generated: <code className="bg-gray-100 px-1 rounded">{formData.name ? generateSlug(formData.name) : '...'}</code>
          </p>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Idea Dump (text or voice) <span className="text-red-500">*</span>
          </label>
          <div className="relative">
            <textarea
              value={formData.ideaNotes}
              onChange={(e) => setFormData({ ...formData, ideaNotes: e.target.value })}
              rows={8}
              className="w-full px-3 py-2 pr-12 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-y"
              placeholder="Talk to yourself like you do in ChatGPT — describe the regulation, audience, pains, hypotheses, market opportunity, competition, pricing thoughts... anything that comes to mind. You can record voice notes and they'll be transcribed here."
            />
            <button
              type="button"
              onClick={isRecording ? stopRecording : startRecording}
              disabled={isTranscribing}
              className={`absolute top-2 right-2 p-2 rounded-lg border transition-colors ${
                isRecording
                  ? 'bg-red-100 border-red-400 text-red-700 hover:bg-red-200'
                  : isTranscribing
                  ? 'bg-gray-100 border-gray-300 text-gray-400 cursor-not-allowed'
                  : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
              }`}
              title={isRecording ? 'Stop recording' : isTranscribing ? 'Transcribing...' : 'Start voice recording'}
            >
              {isTranscribing ? (
                <svg className="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
              ) : isRecording ? (
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M6 6h12v12H6z" />
                </svg>
              ) : (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                </svg>
              )}
            </button>
          </div>
          <div className="mt-1 flex items-center gap-2 text-xs text-gray-500">
            {isRecording && (
              <span className="flex items-center gap-1 text-red-600">
                <span className="w-2 h-2 bg-red-600 rounded-full animate-pulse"></span>
                Recording...
              </span>
            )}
            {isTranscribing && (
              <span className="flex items-center gap-1 text-blue-600">
                <svg className="w-3 h-3 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Transcribing with OpenAI Whisper...
              </span>
            )}
            {!isRecording && !isTranscribing && (
              <span>Click the microphone to record voice notes. They'll be transcribed and appended here.</span>
            )}
          </div>
        </div>

        {error && (
          <div className="p-3 bg-red-50 text-red-800 rounded-lg border border-red-200 text-sm">
            {error}
          </div>
        )}

        <div className="flex justify-end">
          <button
            type="submit"
            disabled={isSubmitting}
            className={`px-6 py-2 rounded-lg font-medium transition-colors ${
              isSubmitting
                ? 'bg-gray-300 text-gray-600 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            {isSubmitting ? 'Creating...' : 'Create Pack'}
          </button>
        </div>
      </form>
    </div>
  )
}

function SalesSummary({ summary }: { summary: RevenueSummary | null }) {
  if (!summary) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Sales Summary</h2>
        <p className="text-gray-600">Loading sales data...</p>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">Sales Summary</h2>
      {summary.note ? (
        <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
          <p className="text-sm text-yellow-800">{summary.note}</p>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="p-4 bg-blue-50 rounded-lg">
              <div className="text-sm text-gray-600 mb-1">Total Leads</div>
              <div className="text-2xl font-bold text-gray-900">{summary.totalLeads}</div>
            </div>
            {summary.totalSales !== null && summary.totalSales !== undefined && (
              <div className="p-4 bg-green-50 rounded-lg">
                <div className="text-sm text-gray-600 mb-1">Total Sales</div>
                <div className="text-2xl font-bold text-gray-900">{summary.totalSales}</div>
              </div>
            )}
          </div>
          {summary.packs.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-gray-900 mb-2">Per Pack</h3>
              <div className="space-y-2">
                {summary.packs.map((pack) => (
                  <div key={pack.slug} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <span className="font-medium text-gray-900">{pack.slug}</span>
                    <div className="flex gap-4 text-sm">
                      <span className="text-gray-600">{pack.leads} leads</span>
                      {pack.sales > 0 && <span className="text-gray-600">{pack.sales} sales</span>}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default function AdminPacksPage() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [packs, setPacks] = useState<PackLifecycle[]>([])
  const [isLoadingPacks, setIsLoadingPacks] = useState(true)
  const [apiError, setApiError] = useState<string | null>(null)
  const [revenueSummary, setRevenueSummary] = useState<RevenueSummary | null>(null)

  const fetchPacks = async () => {
    setIsLoadingPacks(true)
    setApiError(null)
    try {
      const response = await fetch(`${API_BASE_URL}/api/packs`)
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }
      const data = await response.json()
      // Fetch full pack details for each
      const fullPacks = await Promise.all(
        data.map(async (summary: { slug: string }) => {
          const packResponse = await fetch(`${API_BASE_URL}/api/packs/${summary.slug}`)
          if (!packResponse.ok) {
            throw new Error(`Failed to fetch pack ${summary.slug}`)
          }
          return packResponse.json()
        })
      )
      setPacks(fullPacks)
    } catch (error) {
      setApiError(
        error instanceof Error
          ? error.message
          : 'Failed to fetch packs. Make sure the Harbor Ops API is running: python -m orchestrator api'
      )
    } finally {
      setIsLoadingPacks(false)
    }
  }

  const fetchRevenueSummary = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/revenue/summary`)
      if (response.ok) {
        const data = await response.json()
        setRevenueSummary(data)
      }
    } catch (error) {
      // Silently fail for revenue summary
      console.error('Failed to fetch revenue summary:', error)
    }
  }

  useEffect(() => {
    if (isAuthenticated) {
      fetchPacks()
      fetchRevenueSummary()
    }
  }, [isAuthenticated])

  const handleRunResearch = async (slug: string) => {
    const response = await fetch(`${API_BASE_URL}/api/packs/${slug}/runs/research`, {
      method: 'POST',
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }))
      throw new Error(errorData.detail || `HTTP ${response.status}`)
    }

    const result = await response.json()
    // Refresh packs to get updated research status
    await fetchPacks()
    return result
  }

  if (!isAuthenticated) {
    return <AdminLogin onAuthSuccess={() => setIsAuthenticated(true)} />
  }

  return (
    <div className="min-h-screen bg-white">
      <PageMeta
        title="Pack Admin — Harbor Agent"
        description="Pack lifecycle management dashboard"
      />
      <Header />

      <main className="section-padding">
        <div className="container-custom">
          <div className="mb-8">
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              Pack Admin Dashboard
            </h1>
            <p className="text-xl text-gray-600">
              View and manage pack lifecycle status and CRM data
            </p>
          </div>

          {apiError && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl">
              <h3 className="text-sm font-semibold text-red-900 mb-1">API Connection Error</h3>
              <p className="text-sm text-red-800">{apiError}</p>
              <p className="text-xs text-red-700 mt-2">
                Start the Harbor Ops API with: <code className="bg-red-100 px-1 py-0.5 rounded">python -m orchestrator api</code>
              </p>
            </div>
          )}

          <SalesSummary summary={revenueSummary} />

          <NewIdeaForm onSuccess={fetchPacks} />

          {isLoadingPacks ? (
            <div className="text-center py-12">
              <p className="text-gray-600">Loading packs...</p>
            </div>
          ) : packs.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-600">No packs found. Create your first pack using the form above.</p>
            </div>
          ) : (
            <div className="space-y-6">
              {packs.map((pack) => (
                <PackCard key={pack.slug} pack={pack} onRunResearch={handleRunResearch} />
              ))}
            </div>
          )}

          <div className="mt-8 p-6 bg-gray-50 rounded-xl">
            <h2 className="text-lg font-semibold text-gray-900 mb-2">
              Pack Lifecycle Stages
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 text-sm">
              <div>
                <div className="font-medium text-gray-900 mb-1">1. Idea</div>
                <div className="text-gray-600">Initial concept</div>
              </div>
              <div>
                <div className="font-medium text-gray-900 mb-1">2. Validation</div>
                <div className="text-gray-600">Validate concept</div>
              </div>
              <div>
                <div className="font-medium text-gray-900 mb-1">3. Scoring</div>
                <div className="text-gray-600">Score & gate</div>
              </div>
              <div>
                <div className="font-medium text-gray-900 mb-1">4. Deep Dive</div>
                <div className="text-gray-600">Research phase</div>
              </div>
              <div>
                <div className="font-medium text-gray-900 mb-1">5. Build</div>
                <div className="text-gray-600">Implementation</div>
              </div>
              <div>
                <div className="font-medium text-gray-900 mb-1">6. Published</div>
                <div className="text-gray-600">Live & deployed</div>
              </div>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}
