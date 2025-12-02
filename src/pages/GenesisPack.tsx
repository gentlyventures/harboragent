import Header from '../components/Header'
import Hero from '../components/Hero'
import WhatIsGenesis from '../components/WhatIsGenesis'
import Features from '../components/Features'
import Pricing from '../components/Pricing'
import FAQ from '../components/FAQ'
import CTA from '../components/CTA'
import Footer from '../components/Footer'
import PageMeta from '../components/PageMeta'

export default function GenesisPack() {
  return (
    <div className="min-h-screen bg-white">
      <PageMeta
        title="Harbor Agent – Genesis Pack ($199)"
        description="Buy the Genesis Mission Readiness Pack for $199. Includes developer-ready compliance templates, automation scripts, and policy kits."
        ogTitle="Harbor Agent – Genesis Pack ($199)"
        ogDescription="Buy the Genesis Mission Readiness Pack for $199. Includes developer-ready compliance templates, automation scripts, and policy kits."
      />
      <Header />
      <Hero variant="genesis" />
      <WhatIsGenesis />
      <Features />
      <Pricing />
      <FAQ />
      <CTA />
      <Footer />
    </div>
  )
}

