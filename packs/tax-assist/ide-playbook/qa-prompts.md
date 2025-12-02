<!-- path: packs/tax-assist/ide-playbook/qa-prompts.md -->

# Harbor Agent — Tax Assist QA Prompts (v0.1)

These prompts are designed for use with:

- GitHub Copilot Chat  
- Cursor  
- Claude Code  
- Other IDE-integrated AI assistants  

They focus on quality assurance and readiness verification for 2025 tax year preparation.

Ensure the assistant can see:

- /packs/tax-assist/docs/checklist.md  
- /packs/tax-assist/docs/gap-analysis.md  
- /packs/tax-assist/docs/security-guidance.md  
- /packs/tax-assist/docs/roadmap.md  

---

## 1. Practice-Level 2025 Readiness QA

    You are acting as a 2025 Tax Year Readiness QA assistant.

    Review this tax preparation practice using:

    - /packs/tax-assist/docs/checklist.md
    - /packs/tax-assist/docs/gap-analysis.md
    - /packs/tax-assist/docs/security-guidance.md

    Tasks:

    1. Identify current strengths and weaknesses in 2025 tax year readiness.

    2. List Critical (C) gaps by domain (Forms & Data, Software & Tools, Workflows, Security & Compliance, Documentation & Training).

    3. For each Critical gap, point to the specific files, workflows, or areas that need changes.

    4. Suggest a concrete 30/60/90-day plan to address the top 5 gaps.

---

## 2. Form Processing QA

    You are reviewing form processing code for 2025 tax year readiness.

    Use:
    - checklist.md
    - technical-overview.md

    Tasks:

    1. Identify any issues related to:
       - Form 1099-DA parsing and processing
       - Updated K-1 schedule processing
       - Form 7203 (S Corporation basis) processing
       - Information return (W-2, 1099 series) processing

    2. Verify form parsing handles all required fields for 2025.

    3. Suggest specific changes to improve form processing accuracy and completeness.

    4. Do NOT apply changes automatically. Only propose them and explain why.

---

## 3. Tax Calculation QA

    Act as a tax calculation reviewer for 2025 tax year readiness.

    Focus on:
    - Tax bracket tables
    - Standard deduction amounts
    - Retirement contribution limits
    - Mileage rates
    - QBI deduction calculations

    Tasks:

    1. Verify all 2025 tax year values are correctly implemented.

    2. Flag any calculations that don't match 2025 IRS requirements.

    3. Suggest how to add:
       - Updated bracket tables
       - Correct standard deduction amounts
       - Accurate retirement contribution limits
       - Proper mileage rate calculations

    4. Propose changes in small, safe batches with test cases.

---

## 4. E-Filing Integration QA

    You are an e-filing integration reviewer checking 2025 tax year readiness.

    Focus:
    - MeF schema compliance
    - E-file transmission protocols
    - Acknowledgment processing
    - Error handling

    Tasks:

    1. Identify where MeF schema updates are needed for 2025.

    2. Check for missing or incorrect:
       - Schema version references
       - Form validation rules
       - Transmission error handling
       - Acknowledgment processing logic

    3. Propose how to:
       - Update MeF schema references
       - Improve error handling
       - Enhance acknowledgment processing

    4. Propose changes, do not modify code automatically unless asked.

---

## 5. Security and Compliance QA

    You are assessing security and compliance readiness based on:

    - security-guidance.md
    - gap-analysis.md

    Tasks:

    1. Identify potential weaknesses in:
       - Client data encryption (at rest and in transit)
       - Access controls and user permissions
       - Audit logging
       - Privacy and confidentiality measures
       - E-filing security

    2. Verify compliance with:
       - Circular 230 professional standards
       - IRS e-filing security requirements
       - Data protection best practices

    3. Suggest specific technical remediation steps.

    4. Label each issue as Critical (C), Important (I), or Optional (O).

---

## 6. Workflow QA

    You are reviewing tax preparation workflows for 2025 tax year readiness.

    Use:
    - checklist.md
    - roadmap.md
    - architecture.md

    Tasks:

    1. Check workflows for:
       - Client intake process updates
       - Document processing efficiency
       - Quality assurance procedures
       - E-filing workflow completeness
       - Client delivery processes

    2. Identify bottlenecks or inefficiencies.

    3. Suggest improvements to workflow automation and quality assurance.

    4. Ensure workflows handle 2025 form changes correctly.

---

## 7. Client Communication QA

    You are reviewing client communication materials for 2025 tax year changes.

    Use:
    - proposal-template.md
    - roadmap.md

    Tasks:

    1. Check client communication for:
       - Accuracy of 2025 tax law changes
       - Clarity of new requirements (Form 1099-DA, etc.)
       - Completeness of action items
       - Professional tone and accuracy

    2. Verify all 2025 changes are accurately communicated.

    3. Suggest improvements to make communications more helpful and actionable.

    4. Ensure no client-specific information is exposed in templates.

---

## 8. Data Processing QA

    You are reviewing data processing workflows for 2025 tax year readiness.

    Focus on:
    - Document scanning and OCR
    - Data extraction accuracy
    - Data validation rules
    - Quality assurance processes

    Tasks:

    1. Identify areas where data processing needs updates for 2025 forms.

    2. Verify data extraction handles new forms correctly (Form 1099-DA, updated K-1s).

    3. Check data validation rules for completeness and accuracy.

    4. Suggest improvements to data quality assurance.

---

## 9. Staff Training QA

    You are reviewing staff training materials for 2025 tax year readiness.

    Tasks:

    1. Verify training covers:
       - 2025 tax law changes
       - New forms (Form 1099-DA, Form 7203)
       - Digital asset reporting requirements
       - Updated K-1 processing
       - E-filing system updates

    2. Check training materials for accuracy and completeness.

    3. Suggest improvements to training effectiveness.

    4. Ensure training addresses all Critical readiness items.

---

## 10. Software Update QA

    You are reviewing tax software updates for 2025 tax year readiness.

    Tasks:

    1. Verify software updates include:
       - 2025 form library
       - Updated calculation logic
       - MeF schema compliance
       - New form support (Form 1099-DA, etc.)

    2. Check for compatibility issues or breaking changes.

    3. Suggest testing procedures for software updates.

    4. Ensure all Critical forms are supported.

