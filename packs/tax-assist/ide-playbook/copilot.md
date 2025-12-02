<!-- path: packs/tax-assist/ide-playbook/copilot.md -->

# Harbor Agent — IDE / Copilot Playbook (Tax Assist v0.1)

This playbook defines how to use AI coding assistants (GitHub Copilot Chat, Cursor, Claude Code, etc.) safely and effectively when working toward 2025 tax year readiness.

Before using these prompts, ensure the assistant can see:

- /packs/tax-assist/docs/checklist.md  
- /packs/tax-assist/docs/gap-analysis.md  
- /packs/tax-assist/docs/security-guidance.md  
- /packs/tax-assist/docs/roadmap.md  

---

## 1. Workspace Initialization Prompt

Use this once per repository when starting 2025 tax year alignment.

    You are assisting with aligning this tax preparation practice to Harbor Agent's 2025 Tax Year Readiness Pack.

    Rules:

    - Always reference /packs/tax-assist/docs/checklist.md before proposing changes.

    - Never remove client data, tax return files, or audit logs.

    - Do not modify security or credential files.

    - When generating code, prefer creating new files or clearly marked blocks over silent edits.

    - Always produce a diff-style summary before suggesting changes.

    - Ask for clarification when encountering ambiguous requirements.

    - Never expose client PII (Personally Identifiable Information) in code or logs.

    Tasks:

    1. Scan this repository for 2025 tax year readiness gaps using checklist.md and gap-analysis.md.

    2. Produce a prioritized list of issues by domain (Forms & Data, Software & Tools, Workflows, Security & Compliance, Documentation & Training).

    3. Propose small, safe batches of changes (no more than 5 files at a time).

---

## 2. Form Processing Alignment Prompt

Use when focusing on tax form parsing, data extraction, or form processing code.

    You are aligning form processing workflows with 2025 tax year readiness.

    Focus on:

    - Form parsing (W-2s, 1099s, K-1s, Form 1099-DA)

    - Data extraction and validation

    - Form-specific processing logic

    - Integration with tax software

    Tasks:

    1. Identify areas where form parsing is incomplete or needs updates for 2025.

    2. Suggest how to add support for new forms (Form 1099-DA, updated K-1 schedules).

    3. Ensure data extraction handles 2025 form changes correctly.

    4. Propose changes in small batches and explain the impact of each.

---

## 3. Tax Calculation Alignment Prompt

Use when updating tax calculation logic or calculation engines.

    You are aligning tax calculation logic with 2025 tax year requirements.

    Focus on:

    - Tax bracket tables

    - Standard deduction amounts

    - Retirement contribution limits

    - Mileage rates

    - QBI deduction calculations

    Tasks:

    1. Identify where 2025 tax year values need to be updated (brackets, deductions, limits).

    2. Verify calculation logic matches 2025 IRS requirements.

    3. Suggest how to add or update calculation functions for 2025 changes.

    4. Ensure calculations are accurate and testable.

---

## 4. E-Filing Integration Alignment Prompt

Use when updating e-filing integration code or MeF schema compliance.

    You are aligning e-filing integration with 2025 tax year requirements.

    Focus on:

    - Modernized e-File (MeF) schema compliance

    - E-file transmission protocols

    - Acknowledgment processing

    - Error handling

    Tasks:

    1. Identify where MeF schema updates are needed for 2025.

    2. Verify e-file transmission handles 2025 form changes.

    3. Ensure acknowledgment processing works correctly.

    4. Test error handling for new validation rules.

---

## 5. Data Processing Alignment Prompt

Use when focusing on client data processing, document management, or data entry workflows.

    You are aligning data processing workflows with 2025 tax year readiness.

    Focus on:

    - Document scanning and OCR

    - Data extraction from PDFs

    - Data validation and quality checks

    - Client data organization

    Tasks:

    1. Identify areas where data processing needs updates for 2025 forms.

    2. Suggest how to add support for new document types (Form 1099-DA).

    3. Ensure data validation handles 2025 requirements.

    4. Propose improvements to data quality assurance.

---

## 6. Security and Compliance Alignment Prompt

Use when updating security measures, access controls, or compliance procedures.

    You are aligning security and compliance with tax preparation best practices.

    Focus on:

    - Client data encryption

    - Access controls and user permissions

    - Audit logging

    - Privacy and confidentiality

    Tasks:

    1. Identify potential security weaknesses in client data handling.

    2. Verify encryption is applied to client data at rest and in transit.

    3. Ensure access controls follow principle of least privilege.

    4. Confirm audit logging captures all necessary events.

---

## 7. Workflow Automation Alignment Prompt

Use when implementing or updating workflow automation, client communication, or quality assurance processes.

    You are aligning workflow automation with 2025 tax year readiness.

    Focus on:

    - Client intake automation

    - Document processing automation

    - Quality assurance automation

    - Client communication automation

    Tasks:

    1. Identify workflow bottlenecks that could be automated.

    2. Suggest how to automate repetitive tasks (data entry, validation, communication).

    3. Ensure automation maintains data quality and security.

    4. Propose improvements to workflow efficiency.

---

## 8. Documentation Alignment Prompt

Use when updating practice documentation, training materials, or client communication templates.

    You are aligning documentation with current practice workflows and 2025 tax year requirements.

    Focus on:

    - Workflow documentation

    - Form-specific preparation guides

    - Client communication templates

    - Training materials

    Tasks:

    1. Compare existing docs to current workflows and 2025 requirements.

    2. Identify mismatches and missing sections.

    3. Suggest updates to documentation for 2025 changes.

    4. Propose a small set of concrete doc edits.

---

## 9. Guardrails for All Copilot Usage

Whenever using these prompts:

- Do not weaken security controls or remove logging.  
- Do not introduce client PII into code or logs.  
- Do not silently alter tax calculation logic without verification.  
- Always prefer suggestions and diffs over direct, large-scale modifications.  
- Never expose client data in code comments or documentation.  
- Verify all tax calculations against official IRS guidance.  

These rules are meant to keep AI assistance aligned with 2025 tax year readiness goals without creating new risks or compliance issues.

---

## 10. Tax-Specific Considerations

**Client Data Protection:**
- Never log or expose SSNs, EINs, or other sensitive client data
- Ensure all client data access is logged and auditable
- Verify encryption is applied to all client data

**Tax Calculation Accuracy:**
- Always verify calculations against official IRS guidance
- Test calculation logic with known test cases
- Document calculation assumptions and sources

**Form Processing:**
- Verify form parsing handles all required fields
- Test with actual form samples when possible
- Ensure form data validation is comprehensive

**E-Filing Compliance:**
- Verify MeF schema compliance before e-filing
- Test e-file transmission end-to-end
- Ensure acknowledgment processing is reliable

