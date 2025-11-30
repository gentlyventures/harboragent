import PricingCard from './PricingCard'

export default function Pricing() {
  const freeTierFeatures = [
    "Executive Summary",
    "Technical Overview",
    "Partial Readiness Checklist",
    "Gap Analysis Worksheet",
    "Security & Governance Guidance",
    "Roadmap (30/60/90 → 6 → 12 months)",
    "Partial AI Copilot Playbooks",
    "Machine-readable schemas (subset)",
    "Self-healing & QA patterns (partial)"
  ]

  const professionalFeatures = [
    "Full 80–120 item checklist",
    "Complete Copilot/Cursor/Claude Code playbooks",
    "Secure submission bundle templates",
    "Reproducibility kits",
    "Proposal template (fully editable)",
    "Full schema suite (JSON & YAML)",
    "12-month roadmap",
    "Example partner pitch materials",
    "Internal governance binder templates",
    "Enterprise documentation templates",
    "Genesis Ready internal statement"
  ]

  return (
    <section id="pricing" className="section-padding bg-white">
      <div className="container-custom">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Choose Your Pack
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Start with the free tier to evaluate your systems, or get the full Professional Pack 
            for complete readiness toolkits
          </p>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-5xl mx-auto">
          <PricingCard
            title="Free Tier"
            price="$0"
            description="Open source on GitHub"
            features={freeTierFeatures}
            ctaText="Get on GitHub"
            ctaLink="https://github.com/gentlyventures/harboragent"
            isPrimary={false}
          />
          <PricingCard
            title="Professional Pack"
            price="Contact for Pricing"
            description="Complete toolkit for enterprise teams"
            features={professionalFeatures}
            ctaText="Get Professional Pack"
            ctaLink="#checkout"
            isPrimary={true}
            isProfessional={true}
          />
        </div>
        
        <div className="mt-12 text-center">
          <p className="text-gray-600 mb-4">
            Both tiers help you:
          </p>
          <div className="flex flex-wrap justify-center gap-4 text-sm text-gray-700">
            <span className="px-4 py-2 bg-gray-100 rounded-full">Evaluate current systems</span>
            <span className="px-4 py-2 bg-gray-100 rounded-full">Understand Genesis patterns</span>
            <span className="px-4 py-2 bg-gray-100 rounded-full">Run AI-powered audits</span>
            <span className="px-4 py-2 bg-gray-100 rounded-full">Align data & models</span>
            <span className="px-4 py-2 bg-gray-100 rounded-full">Prepare documentation</span>
          </div>
        </div>
      </div>
    </section>
  )
}

