import Header from '../components/Header'
import Hero from '../components/Hero'
import AvailablePacks from '../components/AvailablePacks'
import WhatHarborAgentDoes from '../components/WhatHarborAgentDoes'
import WhoUsesHarborAgent from '../components/WhoUsesHarborAgent'
import LearnMore from '../components/LearnMore'
import Footer from '../components/Footer'
import ContactWidget from '../components/ContactWidget'
import PageMeta from '../components/PageMeta'

export default function Landing() {
  return (
    <div className="min-h-screen bg-white">
      <PageMeta
        title="Harbor Agent — AI-Native Compliance & Readiness Platform"
        description="Harbor Agent is a platform of AI-native compliance and readiness packs for fast-moving government and industry initiatives. Each pack turns complex regulations into developer-ready artifacts and AI-native workflows."
        ogTitle="Harbor Agent — AI-Native Compliance & Readiness Platform"
        ogDescription="AI-native compliance and readiness platform. Turn complex regulations into developer-ready tools your team can actually use."
      />
      <Header />
      <Hero variant="brand" />
      <AvailablePacks />
      <WhatHarborAgentDoes />
      <WhoUsesHarborAgent />
      <LearnMore />
      <Footer />
      <ContactWidget />
    </div>
  )
}

