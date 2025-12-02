export default function WhatHarborAgentDoes() {
  return (
    <section className="section-padding bg-white">
      <div className="container-custom">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              What Harbor Agent Does
            </h2>
            <p className="text-xl text-gray-600">
              Translating large, ambiguous government initiatives into developer-ready artifacts and AI-native workflows
            </p>
          </div>
          
          <div className="prose prose-lg max-w-none">
            <p className="text-gray-700 leading-relaxed mb-6">
              Harbor Agent is a platform from Gently Ventures. Each Harbor Agent Pack is a focused, 
              AI-native compliance and readiness toolkit for a specific government or industry initiative. 
              We translate large, ambiguous initiatives into developer-ready artifacts and AI-native workflows 
              that engineering, ML, and security teams can actually use.
            </p>
            
            <p className="text-gray-700 leading-relaxed mb-6">
              Instead of navigating complex regulatory frameworks and government documentation alone, engineering 
              teams can use Harbor Agent packs to:
            </p>
            
            <div className="bg-primary-50 border-l-4 border-primary-600 p-6 rounded-r-lg my-8">
              <ul className="space-y-3 text-gray-700">
                <li className="flex items-start">
                  <span className="text-primary-600 mr-2">•</span>
                  <span><strong>Inventory systems and assets</strong> — Assess current capabilities and identify gaps</span>
                </li>
                <li className="flex items-start">
                  <span className="text-primary-600 mr-2">•</span>
                  <span><strong>Modernize infrastructure</strong> — Align data, models, and infrastructure for reproducibility</span>
                </li>
                <li className="flex items-start">
                  <span className="text-primary-600 mr-2">•</span>
                  <span><strong>Strengthen governance</strong> — Implement security, provenance, and documentation practices</span>
                </li>
                <li className="flex items-start">
                  <span className="text-primary-600 mr-2">•</span>
                  <span><strong>Prepare proposals</strong> — Create credible, technically sound documentation for collaboration</span>
                </li>
                <li className="flex items-start">
                  <span className="text-primary-600 mr-2">•</span>
                  <span><strong>Use AI safely</strong> — Leverage AI coding assistants with structured guidance and guardrails</span>
                </li>
              </ul>
            </div>
            
            <p className="text-gray-700 leading-relaxed">
              Harbor Agent packs are designed to work <strong>directly inside AI-augmented IDEs</strong> like Cursor, 
              GitHub Copilot Chat, VS Code with Claude Code, and JetBrains AI. The prompts and guidance files 
              give your assistant the rules, boundaries, and context it needs to operate safely and effectively.
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}

