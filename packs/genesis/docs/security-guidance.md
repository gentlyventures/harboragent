<!-- path: packs/genesis/docs/security-guidance.md -->

# Genesis Security and Governance Guidance (v0.1)

*This document provides engineering-focused security and governance readiness guidance for potential participation in the Genesis Mission. It is not legal advice and does not represent DOE requirements.*

The Genesis Mission builds on DOE's long-standing practices around secure scientific computing, data governance, and collaboration with external partners (industry, academia, and labs). This guidance translates those patterns into concrete readiness steps for engineering, security, and compliance teams.

---

## 1. Security Objectives (Readiness, Not Regulation)

For organizations aligning to Genesis, security and governance objectives typically include:

- Protecting sensitive scientific and operational data  

- Ensuring model and data integrity across pipelines  

- Maintaining strong access controls and auditability  

- Enabling secure collaboration with external systems (e.g., national labs, HPC centers)  

- Aligning with widely adopted frameworks such as the NIST AI Risk Management Framework (AI RMF) and DOE cyber-governance norms  

This document focuses on engineering-ready controls rather than legal or contractual obligations.

---

## 2. Data Classification and Handling

### 2.1 Classification

Define and document a simple, actionable classification scheme, for example:

- Public – safe for open publication  

- Internal – for internal use only, low risk if exposed  

- Confidential – sensitive business or technical information  

- Restricted – highly sensitive scientific, operational, or security-related data  

Readiness actions:

- Ensure all Genesis-related datasets are assigned a classification.  

- Maintain classification metadata alongside datasets (e.g., in a table, JSON, or YAML descriptor).  

### 2.2 Handling Rules

For each classification level, define:

- Storage locations allowed  

- Encryption requirements  

- Allowed transmission channels (e.g., VPN, TLS-only, private peering)  

- Access controls (who can view, modify, export)  

Engineering teams should be able to answer:

- Where does each dataset live?  

- Who can access it?  

- How is it protected at rest and in transit?  

---

## 3. Access Control and Identity

### 3.1 Identity and Roles

Readiness baseline:

- Centralized identity (SSO/IdP) for staff accessing data, models, and infrastructure  

- Role-based access control (RBAC) aligned to responsibilities (e.g., Data Engineer, ML Engineer, Security Engineer, Research Scientist)  

### 3.2 Access Policies

For Genesis-aligned systems:

- Document which roles can:  

  - Read, write, or export datasets  

  - Train or deploy models  

  - Modify pipelines or infrastructure  

- Ensure privileged accounts (admin, root, cluster operators) are strictly limited and audited.  

---

## 4. Secrets Management

All secrets (keys, tokens, passwords, certificates) should be:

- Stored in a dedicated secrets manager (e.g., Vault, KMS, cloud-native secrets)  

- Never committed to source control  

- Rotated regularly, with documented procedures  

Readiness checks:

- Review repositories for hard-coded secrets.  

- Confirm that all Genesis-related integration points (APIs, artifact stores, etc.) use centrally managed secrets.  

---

## 5. Data Protection: Encryption and Storage

### 5.1 Encryption in Transit

- Use TLS for all internal and external communications where Genesis-related data or models flow.  

- Ensure services reject plaintext connections or downgrade attempts.  

### 5.2 Encryption at Rest

- Enable encryption at rest for databases, object stores, and file systems that store Genesis-related data, logs, and artifacts.  

- Document key management responsibilities (who controls the keys, how they are rotated).  

---

## 6. Integrity, Provenance, and Audit Trails

Genesis-aligned workflows will typically require strong assurances that:

- Data has not been tampered with  

- Model artifacts correspond to known training pipelines and datasets  

- Changes over time are traceable  

### 6.1 Provenance and Lineage

Readiness actions:

- Maintain lineage metadata:  

  - Original data sources  

  - Transformations with timestamps  

  - Training jobs and configuration versions  

- Store this in a machine-readable format (e.g., JSON files, lineage tables, or a metadata store).  

### 6.2 Audit Trails

- Log access to datasets and models (who, what, when, where).  

- Log configuration changes to pipelines, deployments, and security settings.  

- Ensure logs are retained for an agreed duration and protected from tampering.  

---

## 7. Secure Artifact Submission Patterns

If your organization eventually submits data, models, or workflows to an external system (e.g., national lab infrastructure), recommended patterns include:

- Immutable bundles: Pack artifacts (data slices, models, configs) into immutable bundles with version IDs.  

- Hashing: Compute strong cryptographic hashes (e.g., SHA-256) for each bundle.  

- Signing: For higher assurance, sign bundles using organizational keys so recipients can verify origin and integrity.  

- Metadata: Attach descriptors including:  

  - Name and version  

  - Training or generation context  

  - Classification level  

  - Contact information  

Engineering teams should be able to reconstruct exactly what was submitted, when, and from which internal build or training pipeline.

---

## 8. Model Governance and NIST AI RMF Alignment

DOE and related bodies frequently reference NIST AI RMF principles around:

- Validity and reliability  

- Safety  

- Security and resilience  

- Accountability and transparency  

- Explainability and interpretability  

- Privacy enhancement  

- Fairness  

- Manageability  

Readiness steps:

- Maintain model cards describing:  

  - Intended use  

  - Known limitations  

  - Data sources  

  - Evaluation metrics  

- Document where models are deployed and how their outputs are used.  

- Include known risks or failure modes in model documentation.  

---

## 9. Environment Isolation and Segmentation

To limit blast radius and protect sensitive work:

- Segment Genesis-related workloads into isolated environments, such as:  

  - Separate VPCs or network segments  

  - Dedicated namespaces or clusters  

  - Restricted bastion or jump hosts for access  



- Prevent cross-environment data leakage by:  

  - Restricting egress from sensitive environments  

  - Using explicit allow-lists for external communication  

---

## 10. Incident Response and Monitoring

Readiness items:

- Defined incident response process for:  

  - Data exposure  

  - Model or artifact tampering  

  - Unauthorized access attempts  



- Monitoring for:  

  - Unusual data transfer patterns  

  - Suspicious authentication behavior  

  - Unexpected changes to models, configs, or code  



- Document escalation paths and points of contact.  

---

## 11. Documentation and Governance Binder

Create a concise "Genesis Governance Binder" that collects:

- Data classification policy  

- Access control model  

- Secrets management process  

- Encryption standards  

- Incident response plan  

- Model governance procedures  

- Links to architecture and data flow diagrams  

- Pointers to model cards and key datasets  

---

## 12. AI Copilot Usage for Security and Governance

When using AI coding assistants on Genesis-aligned systems, always provide:

- This security-guidance document  

- The gap analysis  

- The checklist  

Then use instructions similar to:

    You are updating this codebase to align with our Genesis Security & Governance Guidance.

    - Do not modify secrets or security policies without explicit review.

    - Do not weaken access controls, logging, or encryption.

    - When proposing changes, explain how they support data protection, integrity, or auditability.

    - Always reference docs/security-guidance.md and docs/gap-analysis.md before making changes.



This ensures AI tools strengthen rather than erode security and governance posture.

---

## 13. Summary

This guidance provides a practical, engineering-focused interpretation of security and governance
readiness for potential Genesis Mission participation. It is meant to be updated as internal systems
evolve and as DOE publishes additional details about collaboration models and security expectations.

