import Hero from '../components/Hero'
import WhatIsGenesis from '../components/WhatIsGenesis'
import Features from '../components/Features'
import Pricing from '../components/Pricing'
import CTA from '../components/CTA'
import Footer from '../components/Footer'

export default function Landing() {
  return (
    <div className="min-h-screen bg-white">
      <Hero />
      <WhatIsGenesis />
      <Features />
      <Pricing />
      <CTA />
      <Footer />
    </div>
  )
}

