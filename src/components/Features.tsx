export default function Features() {
  const features = [
    {
      title: "AI-Native by Design",
      description: "Works directly inside AI-augmented IDEs like Cursor, GitHub Copilot, Claude Code, and JetBrains AI",
      icon: "🤖"
    },
    {
      title: "Technical Readiness Framework",
      description: "Evaluate systems, identify gaps, modernize infrastructure, and strengthen governance",
      icon: "📋"
    },
    {
      title: "Structured Documentation",
      description: "Executive summaries, technical overviews, checklists, and gap analysis worksheets",
      icon: "📄"
    },
    {
      title: "Security & Governance",
      description: "Guidance for protecting sensitive data, maintaining provenance, and ensuring reproducibility",
      icon: "🛡️"
    },
    {
      title: "Roadmap Planning",
      description: "30/60/90 day → 6 → 12 month readiness roadmap with actionable milestones",
      icon: "🗺️"
    },
    {
      title: "Proposal Templates",
      description: "Ready-to-use templates for partner proposals and internal documentation",
      icon: "📝"
    }
  ]

  return (
    <section className="section-padding bg-gray-50">
      <div className="container-custom">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            What Problems Does It Solve?
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            The Genesis Pack helps engineering teams prepare for Genesis collaboration with practical, 
            AI-native tools and workflows
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="bg-white p-8 rounded-xl shadow-sm hover:shadow-md transition-shadow duration-200 border border-gray-100"
            >
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">
                {feature.title}
              </h3>
              <p className="text-gray-600 leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

