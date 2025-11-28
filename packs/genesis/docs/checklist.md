<!-- path: packs/genesis/docs/checklist.md -->

# Genesis Readiness Checklist (v0.1)

This checklist covers **Data → Models → Infrastructure → Security & Governance → Documentation**.

For each item, mark:

- [ ] Not Started  

- [ ] In Progress  

- [ ] Complete  

You can also map each item to **Critical (C)**, **Important (I)**, or **Optional (O)** priorities.

---

## 1. Data Readiness

### Structure and Quality

- [ ] Data sources have explicit, documented schemas (C)  

- [ ] Metadata fields follow a consistent standard across datasets (C)  

- [ ] Data provenance is tracked (source, transformations, timestamps) (C)  

- [ ] Dataset versioning exists for major datasets (I)  

- [ ] Dataset quality metrics are defined and tracked (I)  

### Formats and Interoperability

- [ ] Data can be exported to JSON (C)  

- [ ] Data can be exported to CSV (C)  

- [ ] Data can be exported to Parquet or HDF5 where appropriate (C)  

### Governance

- [ ] A data classification framework is defined (C)  

- [ ] Access controls exist for read/write/scoped access (C)  

- [ ] Retention and archival policies exist (O)  

---

## 2. Model Readiness

### Inventory and Documentation

- [ ] All Genesis-relevant models are inventoried (C)  

- [ ] Basic metadata (owner, purpose, inputs/outputs) is documented (C)  

- [ ] Model cards exist or are planned (C)  

### Reproducibility

- [ ] Training scripts are version-controlled (C)  

- [ ] Training runs produce logs and saved configs (C)  

- [ ] Dependencies are pinned (C)  

- [ ] Deterministic inference mode is available, when feasible (I)  

### Exportability and Benchmarks

- [ ] Models can export to ONNX or equivalent portable formats (I)  

- [ ] Models can be packaged in containers for deployment (I)  

- [ ] Benchmark suites exist and are reproducible (I)  

- [ ] Explainability or feature attributions are available when applicable (O)  

---

## 3. Infrastructure Readiness

### Deployment and Containers

- [ ] All critical pipelines are containerized (Docker/Singularity) (C)  

- [ ] CI/CD exists for building, testing, and deploying pipelines (I)  

- [ ] Inference workloads can run in isolated environments (C)  

### APIs and Integration

- [ ] REST or gRPC APIs are documented (I)  

- [ ] Internal schemas can be mapped to external submission formats (I)  

### HPC and Workflow Portability

- [ ] Workflows can be adapted to or already run on HPC-like systems (O)  

- [ ] Pipelines are compatible with workflow engines (Airflow, Nextflow, Prefect, etc.) (I)  

---

## 4. Security and Governance

- [ ] Secrets are stored in a dedicated secrets manager (Vault/KMS, etc.) (C)  

- [ ] Data is encrypted in transit (C)  

- [ ] Data is encrypted at rest (C)  

- [ ] Access and change logs are maintained (C)  

- [ ] Sensitive workloads are isolated through network segmentation (C)  

- [ ] Model/data submission artifacts can be hashed and/or signed (I)  

- [ ] Internal processes are aligned with NIST AI RMF principles (I)  

- [ ] Basic drift detection exists for models and key datasets (O)  

---

## 5. Documentation and Process

- [ ] A current architecture diagram exists (C)  

- [ ] Data flow diagrams exist for major pipelines (C)  

- [ ] Change-management processes are documented (I)  

- [ ] Standard operating procedures (SOPs) exist for core workflows (I)  

- [ ] A Governance Binder collects key policies and links (I)  

- [ ] An internal "Genesis Readiness Statement" has been drafted (O)  

Use this checklist with the **Gap Analysis** and **Roadmap** documents to plan and track progress.

