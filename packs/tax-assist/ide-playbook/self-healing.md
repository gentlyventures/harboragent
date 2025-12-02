<!-- path: packs/tax-assist/ide-playbook/self-healing.md -->

# Harbor Agent — Tax Assist Self-Healing and Drift Detection Prompts (v0.1)

These prompts help AI assistants:

- Detect drift away from 2025 tax year readiness  
- Suggest remediations  
- Maintain alignment as tax preparation workflows evolve  

Use them periodically or before major releases.

---

## 1. Practice Drift Detection

    You are a self-healing assistant focused on 2025 tax year readiness.

    Assume this tax preparation practice was previously aligned with:

    - checklist.md
    - gap-analysis.md
    - security-guidance.md

    Tasks:

    1. Compare current practice state against those documents.

    2. Identify areas where:

       - New workflows bypass quality assurance or documentation
       - Security standards were weakened
       - Form processing lost accuracy or completeness
       - Tax calculations drifted from 2025 requirements

    3. Output a list of drift findings by domain:

       - Forms & Data
       - Software & Tools
       - Workflows
       - Security & Compliance
       - Documentation & Training

    4. For each finding, suggest a minimal, safe remediation.

---

## 2. Form Processing Drift

    You are checking for form processing drift against 2025 tax year requirements.

    Tasks:

    1. Identify changes to form parsing, data extraction, or form processing since the last known good version.

    2. Flag:

       - Missing form support (Form 1099-DA, updated K-1s)
       - Incomplete form field extraction
       - Changes that could break form processing
       - Validation rules that need updates

    3. Suggest:

       - Form parsing updates
       - Data extraction improvements
       - Validation rule updates
       - Testing procedures

---

## 3. Tax Calculation Drift

    You are reviewing tax calculation changes for 2025 tax year alignment.

    Tasks:

    1. Compare current tax calculation logic to 2025 IRS requirements.

    2. Detect:

       - Outdated tax bracket tables
       - Incorrect standard deduction amounts
       - Wrong retirement contribution limits
       - Inaccurate mileage rate calculations
       - QBI deduction calculation errors

    3. Propose:

       - Calculation updates
       - Test case additions
       - Documentation updates
       - Verification procedures

---

## 4. E-Filing Integration Drift

    You are reviewing e-filing integration for drift from 2025 MeF requirements.

    Tasks:

    1. Identify any changes that:

       - Break MeF schema compliance
       - Weaken e-file transmission security
       - Reduce acknowledgment processing reliability
       - Introduce e-filing errors

    2. For each issue, suggest a safe patch that restores or improves e-filing alignment.

    3. Mark each issue as Critical (C), Important (I), or Optional (O).

---

## 5. Security Configuration Self-Healing

    You are reviewing security and compliance configs for drift from Security and Data Protection Guidance.

    Tasks:

    1. Identify any changes that:

       - Weaken client data encryption
       - Relax access controls
       - Reduce audit logging
       - Compromise client data privacy

    2. For each issue, suggest a safe patch that restores or improves security alignment.

    3. Mark each issue as Critical (C), Important (I), or Optional (O).

---

## 6. Workflow Self-Healing

    You are reviewing workflows for alignment with 2025 tax year readiness.

    Tasks:

    1. Identify mismatches between:

       - Documented workflows and actual practice
       - Quality assurance procedures and implementation
       - Client communication templates and usage
       - Training materials and staff knowledge

    2. Suggest concrete edits to:

       - Workflow documentation
       - Quality assurance checklists
       - Client communication templates
       - Training materials

---

## 7. Documentation Self-Healing

    You are reviewing documentation (workflows, form guides, training) for alignment with current practice and 2025 requirements.

    Tasks:

    1. Identify mismatches between:

       - Documentation and actual workflows
       - Form guides and current form processing
       - Training materials and 2025 requirements

    2. Suggest concrete edits to:

       - Workflow documentation
       - Form-specific preparation guides
       - Training materials
       - Client communication templates

---

## 8. Automated Readiness Refresh

    You are regenerating the 2025 tax year readiness.yaml file based on current practice state.

    Tasks:

    1. Use gap-analysis.md and tax-assist-checklist.json as the criteria.

    2. Infer:

       - Domain scores (0–2) for Forms & Data, Software & Tools, Workflows, Security & Compliance, Documentation & Training.

       - Critical, Important, and Optional coverage.

       - Top 5 gaps.

       - Recommended actions for the next 90 days.

    3. Draft updated readiness.yaml content we can paste into the file.

---

## 9. Form-Specific Drift Detection

    You are checking for drift in specific form processing (Form 1099-DA, K-1s, etc.).

    Tasks:

    1. Identify changes to form processing that could affect:

       - Form 1099-DA parsing and integration
       - K-1 schedule processing
       - Form 7203 (S Corporation basis) processing
       - Information return processing

    2. Flag:

       - Missing form support
       - Incomplete field extraction
       - Validation rule gaps
       - Integration issues

    3. Suggest:

       - Form processing updates
       - Testing procedures
       - Documentation updates

---

## 10. Client Data Protection Self-Healing

    You are reviewing client data protection measures for drift from security guidance.

    Tasks:

    1. Identify any changes that:

       - Expose client PII in logs or code
       - Weaken encryption
       - Reduce access control effectiveness
       - Compromise audit logging

    2. For each issue, suggest a safe remediation that restores or improves data protection.

    3. Mark each issue as Critical (C), Important (I), or Optional (O).

---

## 11. Guardrails

When using these prompts, always instruct the AI assistant:

- Do not automatically apply high-impact changes without human review.  
- Do not weaken security or compliance controls.  
- Prefer documenting recommendations over modifying production systems.  
- Ask for clarification when requirements are ambiguous.  
- Never expose client PII in code, logs, or documentation.  
- Verify all tax calculations against official IRS guidance.  

---

## 12. Tax-Specific Self-Healing Considerations

**Calculation Accuracy:**
- Always verify calculations against official IRS guidance
- Test with known test cases before applying changes
- Document calculation sources and assumptions

**Form Processing:**
- Test form parsing with actual form samples
- Verify all required fields are extracted
- Ensure validation rules are comprehensive

**Client Data Protection:**
- Never log or expose client PII
- Verify encryption is applied to all client data
- Ensure audit logging captures all necessary events

**E-Filing Compliance:**
- Verify MeF schema compliance before changes
- Test e-file transmission end-to-end
- Ensure acknowledgment processing is reliable

