<!-- path: packs/genesis/docs/gap-analysis.md -->

# Genesis Readiness Gap Analysis (v0.1)

*This worksheet is for internal engineering readiness assessment only. It does not represent DOE requirements.*

The analysis evaluates alignment across five readiness domains:

1. Data  

2. Models  

3. Infrastructure  

4. Security and Governance  

5. Documentation and Processes  

Scoring:  

- 0 = Not Present  

- 1 = Partial / In Progress  

- 2 = Complete  

Priority:  

- C = Critical  

- I = Important  

- O = Optional  

Each row includes a recommended owner (Eng/ML/Infra/Risk/etc.).

---

# 1. Data Readiness

| Area      | Item               | Description                                         | Score (0–2) | Priority | Owner          |

|-----------|--------------------|-----------------------------------------------------|-------------|----------|----------------|

| Schema    | Structured data    | Data sources have clear schemas                     |             | C        | Data Eng       |

| Metadata  | Consistent metadata| Metadata is consistent across datasets              |             | C        | Data Eng       |

| Provenance| Lineage tracking   | Provenance tracked (source, transforms, timestamps) |             | C        | Data Eng       |

| Versioning| Dataset versioning | Dataset versions maintained automatically           |             | I        | Data Eng       |

| Quality   | Quality scoring    | Datasets have quality metrics                       |             | I        | Data Eng       |

| Formats   | Exportability      | Supports JSON, CSV, Parquet, HDF5 exports           |             | C        | ML Eng         |

| Governance| Classification     | Data classification defined                         |             | C        | Sec/Compliance |

| Access    | Access control     | Policies for read/write/scoped access               |             | C        | Sec/IT         |

| Retention | Retention policy   | Retention/archival processes defined                |             | O        | Sec/IT         |

---

# 2. Model Readiness

| Area         | Item               | Description                                         | Score | Priority | Owner   |

|--------------|--------------------|-----------------------------------------------------|-------|----------|---------|

| Inventory    | Model catalog      | Inventory of all models with metadata               |       | C        | ML Eng  |

| Reproducibility | Deterministic inference | Ability to reproduce outputs deterministically |       | I        | ML Eng  |

| Logging      | Training logs      | Training pipeline logs stored and versioned         |       | C        | ML Eng  |

| Dependencies | Dependency pinning | Dependencies pinned across environments             |       | C        | ML Eng  |

| Documentation| Model cards        | Model cards exist for all models                    |       | C        | ML Eng  |

| Explainability | Feature attribution | Logic for feature attributions (if applicable)   |       | O        | ML Eng  |

| Export       | ONNX/container exports | Models exportable to ONNX or container bundles  |       | I        | ML Eng  |

| Benchmarking | Performance suite  | Benchmarks exist and are reproducible               |       | I        | ML Eng  |

---

# 3. Infrastructure Readiness

| Area          | Item                  | Description                                      | Score | Priority | Owner  |

|---------------|-----------------------|--------------------------------------------------|-------|----------|--------|

| Containers    | Pipeline containerization | All pipelines containerized                  |       | C        | Infra  |

| CI/CD         | CI/CD automation      | Pipelines tested and deployed automatically     |       | I        | DevOps |

| Isolation     | Isolated inference    | Inference workloads run in secure isolation     |       | C        | Infra/Sec |

| APIs          | API documentation     | REST/gRPC endpoints documented                  |       | I        | Eng    |

| Data Interop  | Schema mapping        | Internal schemas map to external formats        |       | I        | Eng    |

| HPC           | HPC interface         | Workflows can run on HPC-like systems           |       | O        | Infra  |

| Compatibility | Workflow portability  | Compatible with standard orchestrators          |       | I        | DevOps |

---

# 4. Security and Governance Readiness

| Area       | Item                | Description                                      | Score | Priority | Owner           |

|------------|---------------------|--------------------------------------------------|-------|----------|-----------------|

| Secrets    | Secrets management  | Vault/KMS used for secrets                       |       | C        | Sec             |

| Logging    | Audit trails        | Access and change logs maintained                |       | C        | Sec             |

| Encryption | Data protection     | Encryption in transit and at rest                |       | C        | Sec             |

| Network    | Segmentation        | Sensitive systems isolated via segmentation      |       | C        | Sec/IT          |

| Governance | NIST AI RMF alignment | Processes mirror NIST AI RMF principles       |       | I        | Risk/Compliance |

| Submission | Secure bundles      | Model/data submissions hashed and/or signed      |       | I        | ML/DevOps       |

| Monitoring | Drift detection     | Capability to detect model/data drift            |       | O        | ML Eng          |

---

# 5. Documentation and Process Readiness

| Area         | Item                 | Description                                      | Score | Priority | Owner          |

|--------------|----------------------|--------------------------------------------------|-------|----------|----------------|

| Architecture | Architecture diagram | Updated architecture diagram exists              |       | C        | Eng            |

| Data Flow    | Data documentation   | Documented upstream/downstream data flows        |       | C        | Data Eng       |

| Change Mgmt  | Change management    | Versioning and approvals defined                 |       | I        | Eng/PM         |

| Ops Docs     | SOPs                 | Standard operating procedures exist              |       | I        | PM/Ops         |

| Governance   | Governance binder    | Central governance documentation collection      |       | I        | Risk/Compliance|

| Readiness    | Readiness statement  | Internal Genesis readiness memo drafted          |       | O        | Exec/Ops       |

---

# Summary Table (Complete After Scoring)

Critical Coverage (%):  

Important Coverage (%):  

Optional Coverage (%):  

Overall Readiness Score (0–2):  

Top 5 Gaps:  

1.  

2.  

3.  

4.  

5.  

Recommended 90-Day Priorities:  

1.  

2.  

3.  

4.  

5.  

---

# AI Copilot / Cursor Usage

Use the following instruction inside your AI coding assistant to automate this gap analysis:

    Evaluate this repository against /packs/genesis/docs/gap-analysis.md.

    Output:

    - Score for each row in the tables

    - List of Critical (C) gaps only

    - Recommended file and documentation changes

    - Any missing schemas or metadata

    - A suggested 30/60/90-day plan to close the most important gaps

