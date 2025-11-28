<!-- path: packs/genesis/ide-playbook/copilot.md -->

# Harbor Agent — IDE / Copilot Playbook (Genesis v0.1)

This playbook defines how to use AI coding assistants (GitHub Copilot Chat, Cursor, Claude Code, etc.) safely and effectively when working toward Genesis readiness.

Before using these prompts, ensure the assistant can see:

- /packs/genesis/docs/checklist.md  

- /packs/genesis/docs/gap-analysis.md  

- /packs/genesis/docs/security-guidance.md  

- /packs/genesis/docs/roadmap.md  

---

## 1. Workspace Initialization Prompt

Use this once per repository when starting Genesis alignment.

    You are assisting with aligning this repository to Harbor Agent's Genesis Readiness Pack.

    Rules:

    - Always reference /packs/genesis/docs/checklist.md before proposing changes.

    - Never remove logs, metadata, or versioning files.

    - Do not modify security or credential files.

    - When generating code, prefer creating new files or clearly marked blocks over silent edits.

    - Always produce a diff-style summary before suggesting changes.

    - Ask for clarification when encountering ambiguous requirements.

    Tasks:

    1. Scan this repository for Genesis readiness gaps using checklist.md and gap-analysis.md.

    2. Produce a prioritized list of issues by domain (Data, Models, Infra, Security, Documentation).

    3. Propose small, safe batches of changes (no more than 5 files at a time).

---

## 2. Data Pipeline Alignment Prompt

Use when focusing on ETL/ELT or data-processing code.

    You are aligning data pipelines with Genesis readiness.

    Focus on:

    - Schemas

    - Metadata

    - Provenance

    - Exportability

    Tasks:

    1. Identify areas where schemas are implicit and should be explicit.

    2. Suggest how to add metadata and provenance tracking in a minimal, robust way.

    3. Ensure support for exports to JSON/Parquet/HDF5 where relevant.

    4. Propose changes in small batches and explain the impact of each.

---

## 3. Model Pipeline Alignment Prompt

Use when updating training or inference code.

    You are aligning model pipelines with Genesis readiness.

    Focus on:

    - Reproducibility

    - Logging

    - Model cards

    - Exportability

    Tasks:

    1. Identify missing or weak reproducibility controls (seeds, versioning, dependency pinning).

    2. Propose how to capture training configs, dataset versions, and metrics.

    3. Suggest how to add or improve model cards.

    4. Enable ONNX or container exports where applicable.

---

## 4. Documentation Alignment Prompt

Use when updating architecture or process docs.

    You are aligning documentation with the current codebase and Genesis readiness.

    Focus on:

    - architecture.md

    - roadmap.md

    - governance binder (if present)

    Tasks:

    1. Compare existing docs to code and configs.

    2. Identify mismatches and missing sections.

    3. Suggest updates to architecture diagrams and data flow descriptions.

    4. Propose a small set of concrete doc edits.

---

## 5. Guardrails for All Copilot Usage

Whenever using these prompts:

- Do not weaken security controls or remove logging.  

- Do not introduce new secrets into code.  

- Do not silently alter deployment environments.  

- Always prefer suggestions and diffs over direct, large-scale modifications.  

These rules are meant to keep AI assistance aligned with Genesis readiness goals without creating new risks.

