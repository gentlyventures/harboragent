<!-- path: packs/genesis/ide-playbook/qa-prompts.md -->

# Harbor Agent — Genesis QA Prompts (v0.1)

These prompts are designed for use with:

- GitHub Copilot Chat  

- Cursor  

- Claude Code  

- Other IDE-integrated AI assistants  

They focus on quality assurance and readiness verification for Genesis-aligned work.

Ensure the assistant can see:

- /packs/genesis/docs/checklist.md  

- /packs/genesis/docs/gap-analysis.md  

- /packs/genesis/docs/security-guidance.md  

- /packs/genesis/docs/roadmap.md  

---

## 1. Repository-Level Genesis Readiness QA

    You are acting as a Genesis Readiness QA assistant.

    Review this repository using:

    - /packs/genesis/docs/checklist.md

    - /packs/genesis/docs/gap-analysis.md

    - /packs/genesis/docs/security-guidance.md

    Tasks:

    1. Identify current strengths and weaknesses in Genesis readiness.

    2. List Critical (C) gaps by domain (Data, Models, Infrastructure, Security, Documentation).

    3. For each Critical gap, point to the specific files or areas that need changes.

    4. Suggest a concrete 30/60/90-day plan to address the top 5 gaps.

---

## 2. File-Level Compliance Check

    You are reviewing this file for Genesis readiness and security alignment.

    Use:

    - checklist.md

    - security-guidance.md

    Tasks:

    1. Identify any issues related to:

       - Data provenance

       - Reproducibility

       - Secrets handling

       - Logging and auditability

    2. Suggest specific changes in this file to improve alignment.

    3. Do NOT apply changes automatically. Only propose them and explain why.

---

## 3. Data Pipeline QA

    Act as a data engineering reviewer for Genesis readiness.

    Focus on:

    - Schemas

    - Metadata

    - Provenance

    - Exportability

    Tasks:

    1. Identify where schemas are implied but not explicitly defined.

    2. Flag missing metadata or lineage tracking steps.

    3. Suggest how to add:

       - Versioning

       - Classification labels

       - Export to JSON/Parquet/HDF5

    4. Propose changes in small, safe batches.

---

## 4. Model Pipeline QA

    You are an ML engineering reviewer checking Genesis readiness.

    Focus:

    - Reproducibility

    - Logging

    - Model cards

    - Exportability

    Tasks:

    1. Identify where training or inference is not reproducible.

    2. Check for missing logs of:

       - Training parameters

       - Dataset versions

       - Evaluation metrics

    3. Propose how to:

       - Add or improve model cards

       - Enable ONNX or container exports

    4. Propose changes, do not modify code automatically unless asked.

---

## 5. Security and Governance QA

    You are assessing security and governance readiness based on:

    - security-guidance.md

    - gap-analysis.md

    Tasks:

    1. Identify potential weaknesses in:

       - Secrets management

       - Encryption at rest/in transit

       - Access controls

       - Audit logs

       - Network segmentation

    2. Suggest specific technical remediation steps.

    3. Label each issue as Critical (C), Important (I), or Optional (O).

---

## 6. Proposal QA

    You are reviewing the Genesis Partner Proposal for clarity and completeness.

    Use:

    - proposal-template.md

    - roadmap.md

    Tasks:

    1. Check each section for missing information (Capabilities, Data, Models, Architecture, Security, Timeline).

    2. Suggest improvements to make the proposal more concrete and technically credible.

    3. Ensure claims are accurate and do not overstate regulatory or contractual relationships.

    4. Highlight any sections that should reference specific artifacts (diagrams, model cards, governance binder).

