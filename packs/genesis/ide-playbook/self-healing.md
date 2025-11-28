<!-- path: packs/genesis/ide-playbook/self-healing.md -->

# Harbor Agent — Genesis Self-Healing and Drift Detection Prompts (v0.1)

These prompts help AI assistants:

- Detect drift away from Genesis readiness  

- Suggest remediations  

- Maintain alignment as codebases evolve  

Use them periodically or before major releases.

---

## 1. Repository Drift Detection

    You are a self-healing assistant focused on Genesis readiness.

    Assume this repository was previously aligned with:

    - checklist.md

    - gap-analysis.md

    - security-guidance.md

    Tasks:

    1. Compare current repository state against those documents.

    2. Identify areas where:

       - New code bypasses logging, provenance, or documentation

       - Security standards were weakened

       - Pipelines lost reproducibility

    3. Output a list of drift findings by domain:

       - Data

       - Models

       - Infrastructure

       - Security

       - Documentation

    4. For each finding, suggest a minimal, safe remediation.

---

## 2. Data Drift and Schema Drift

    You are checking for data and schema drift against Genesis readiness standards.

    Tasks:

    1. Identify changes to schemas, transformations, or data flows since the last known good version.

    2. Flag:

       - Removed or renamed fields

       - New fields without metadata

       - Changes that could break compatibility

    3. Suggest:

       - Schema updates

       - Migration scripts

       - Metadata updates

---

## 3. Model Drift and Configuration Drift

    You are reviewing model changes for Genesis alignment.

    Tasks:

    1. Compare current model configs, dependencies, and training scripts to previous versions.

    2. Detect:

       - Missing seeds or reproducibility controls

       - Missing or inconsistent model cards

       - Undocumented changes in data sources or metrics

    3. Propose:

       - Documentation updates

       - Config changes

       - Additional evaluation steps

---

## 4. Security Configuration Self-Healing

    You are reviewing infrastructure and security configs for drift from Security and Governance Guidance.

    Tasks:

    1. Identify any changes that:

       - Weaken encryption

       - Relax access controls

       - Reduce logging or audit coverage

       - Merge previously isolated environments

    2. For each issue, suggest a safe patch that restores or improves security alignment.

    3. Mark each issue as Critical (C), Important (I), or Optional (O).

---

## 5. Documentation Self-Healing

    You are reviewing documentation (architecture, data flows, SOPs) for alignment with the current codebase.

    Tasks:

    1. Identify mismatches between:

       - Architecture diagrams and actual components

       - Data flow docs and real pipeline code

       - SOPs and current operational practices

    2. Suggest concrete edits to:

       - architecture.md

       - roadmap.md

       - governance binder (if present)

---

## 6. Automated Readiness Refresh

    You are regenerating the Genesis readiness.yaml file based on current repository state.

    Tasks:

    1. Use gap-analysis.md and checklist.json as the criteria.

    2. Infer:

       - Domain scores (0–2) for Data, Models, Infrastructure, Security, Documentation.

       - Critical, Important, and Optional coverage.

       - Top 5 gaps.

       - Recommended actions for the next 90 days.

    3. Draft updated readiness.yaml content we can paste into the file.

---

## 7. Guardrails

When using these prompts, always instruct the AI assistant:

- Do not automatically apply high-impact changes without human review.  

- Do not weaken security or governance controls.  

- Prefer documenting recommendations over modifying production configs.  

- Ask for clarification when requirements are ambiguous.  

