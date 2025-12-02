import Header from '../components/Header'
import Hero from '../components/Hero'
import WhatIsTaxAssist from '../components/WhatIsTaxAssist'
import Features from '../components/Features'
import Pricing from '../components/Pricing'
import FAQ from '../components/FAQ'
import CTA from '../components/CTA'
import Footer from '../components/Footer'
import PageMeta from '../components/PageMeta'

export default function TaxAssistPack() {
  return (
    <div className="min-h-screen bg-white">
      <PageMeta
        title="Harbor Agent – AI Tax Assistant Pack ($199)"
        description="Buy the AI Tax Assistant Readiness Pack for $199. Prepare for 2025 tax year with readiness checklists, form processing guides, and AI copilot playbooks."
        ogTitle="Harbor Agent – AI Tax Assistant Pack ($199)"
        ogDescription="Buy the AI Tax Assistant Readiness Pack for $199. Prepare for 2025 tax year with readiness checklists, form processing guides, and AI copilot playbooks."
      />
      <Header />
      <Hero variant="tax-assist" />
      <WhatIsTaxAssist />
      <Features />
      <Pricing />
      <FAQ />
      <CTA />
      <Footer />
    </div>
  )
}

