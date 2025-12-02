<!-- path: packs/tax-assist/docs/security-guidance.md -->

# Tax Preparation Security and Data Protection Guidance (v0.1)

*This document provides practice-focused security and data protection guidance for tax preparation professionals preparing for the 2025 tax filing season. It is not legal advice and does not represent IRS requirements.*

Tax preparation practices handle highly sensitive client data including Social Security Numbers, financial information, and tax return data. This guidance translates industry best practices and regulatory requirements into concrete security steps for tax preparers, practice managers, and IT staff.

---

## 1. Security Objectives

For tax preparation practices, security and data protection objectives include:

- Protecting client PII (Personally Identifiable Information) and financial data

- Ensuring data integrity across tax preparation workflows

- Maintaining strong access controls and auditability

- Complying with IRS requirements and professional standards

- Enabling secure client communication and file transfer

- Protecting against data breaches and identity theft

This document focuses on practical, implementable controls rather than legal or regulatory obligations.

---

## 2. Data Classification and Handling

### 2.1 Classification

Define and document a simple classification scheme:

- **Public** – Safe for general communication (e.g., tax law summaries)

- **Internal** – For internal use only (e.g., workflow documentation)

- **Confidential** – Client data, tax returns, financial information

- **Restricted** – Highly sensitive data (SSNs, bank accounts, identity documents)

**Readiness actions:**

- Ensure all client data is classified as Confidential or Restricted

- Maintain classification metadata alongside client files

- Train staff on data classification and handling

### 2.2 Handling Rules

For each classification level, define:

- Storage locations allowed (encrypted drives, secure servers)

- Encryption requirements (at rest and in transit)

- Allowed transmission channels (secure portals, encrypted email)

- Access controls (who can view, modify, export)

- Retention and disposal requirements

**Engineering teams should be able to answer:**

- Where does each client's data live?

- Who can access it?

- How is it protected at rest and in transit?

- When is it disposed of?

---

## 3. Access Control and Identity

### 3.1 Identity and Roles

**Readiness baseline:**

- Unique user accounts for all staff accessing client data

- Role-based access control (RBAC) aligned to responsibilities:
  - Tax Preparer (read/write client data)
  - Reviewer (read-only, can approve)
  - Administrator (full access)
  - Support Staff (limited access)

- Strong password policies (complexity, expiration, MFA)

### 3.2 Access Policies

For tax preparation systems:

- Document which roles can:
  - View client tax returns
  - Modify return data
  - E-file returns
  - Access client financial information
  - Export client data

- Ensure privileged accounts (admin, system) are strictly limited and audited

- Implement principle of least privilege (minimum access necessary)

---

## 4. Secrets Management

All secrets (passwords, API keys, encryption keys) should be:

- Stored in a dedicated secrets manager (password manager, KMS)

- Never committed to source control or shared via email

- Rotated regularly with documented procedures

- Protected with MFA where possible

**Readiness checks:**

- Review systems for hard-coded passwords or keys

- Confirm all tax software and e-filing credentials use secure storage

- Verify staff use password managers for client portal access

---

## 5. Data Protection: Encryption and Storage

### 5.1 Encryption in Transit

- Use TLS/SSL for all client data transmission:
  - Client portals (HTTPS)
  - Email (encrypted email or secure portals)
  - File transfers (SFTP, secure cloud storage)
  - Remote access (VPN)

- Ensure services reject plaintext connections

### 5.2 Encryption at Rest

- Enable encryption at rest for:
  - Client data files
  - Tax return databases
  - Backup storage
  - Cloud storage

- Document key management (who controls keys, rotation procedures)

- Use full-disk encryption on laptops and workstations

---

## 6. Integrity, Provenance, and Audit Trails

Tax preparation workflows require strong assurances that:

- Client data has not been tampered with

- Tax returns correspond to source documents

- Changes over time are traceable

- E-filed returns are accurately transmitted

### 6.1 Data Provenance

**Readiness actions:**

- Maintain source document tracking:
  - Original client documents (W-2s, 1099s, receipts)
  - Data entry timestamps
  - Modification history
  - E-file transmission records

- Store this in a machine-readable format (metadata, logs)

### 6.2 Audit Trails

- Log access to client data (who, what, when, where)

- Log changes to tax returns (preparer, reviewer, timestamps)

- Log e-file submissions and acknowledgments

- Ensure logs are retained for required duration and protected from tampering

---

## 7. Secure Client Communication

### 7.1 Secure File Transfer

- Use secure client portals for document exchange

- Avoid unencrypted email for sensitive data

- Implement secure file sharing (encrypted cloud storage, secure portals)

### 7.2 Identity Verification

- Verify client identity before sharing sensitive information

- Use secure authentication for client portal access

- Implement procedures for phone/email verification

---

## 8. E-Filing Security

### 8.1 E-File Transmission

- Use IRS-approved e-file providers and software

- Verify e-file transmission uses encryption (TLS/SSL)

- Maintain records of e-file submissions and acknowledgments

### 8.2 E-File Authentication

- Protect e-file credentials (EFIN, passwords)

- Use MFA for e-file provider accounts where available

- Rotate e-file credentials regularly

---

## 9. Incident Response and Monitoring

**Readiness items:**

- Defined incident response process for:
  - Data breaches
  - Unauthorized access
  - Lost or stolen devices
  - Phishing attacks

- Monitoring for:
  - Unusual access patterns
  - Suspicious authentication attempts
  - Unexpected data exports
  - Failed login attempts

- Document escalation paths and points of contact:
  - Internal IT/Security
  - Legal counsel
  - Cyber insurance
  - IRS (if required)

---

## 10. Physical Security

### 10.1 Office Security

- Secure physical access to offices and workstations

- Lock filing cabinets containing client data

- Secure disposal of paper documents (shredding)

### 10.2 Device Security

- Full-disk encryption on laptops and workstations

- Automatic screen locks after inactivity

- Secure disposal of old devices (data wiping)

- Prohibit use of personal devices for client data (BYOD policies)

---

## 11. Backup and Disaster Recovery

### 11.1 Backup Procedures

- Regular automated backups of client data

- Encrypted backup storage

- Tested backup restoration procedures

- Off-site backup storage

### 11.2 Disaster Recovery

- Documented disaster recovery plan

- Regular testing of recovery procedures

- Business continuity planning

---

## 12. Compliance and Professional Standards

### 12.1 IRS Requirements

- Comply with IRS e-filing security requirements

- Maintain PTIN and professional credentials

- Follow Circular 230 professional standards

### 12.2 State Requirements

- Comply with state data protection laws

- Maintain state professional licenses

- Follow state-specific security requirements

### 12.3 Professional Liability

- Maintain professional liability insurance

- Document security practices for insurance purposes

---

## 13. Staff Training and Awareness

### 13.1 Security Training

- Regular security awareness training for all staff

- Phishing awareness and prevention

- Password security best practices

- Data handling procedures

### 13.2 Incident Response Training

- Staff training on incident response procedures

- Reporting procedures for security incidents

- Client notification procedures (if required)

---

## 14. Documentation and Governance

Create a concise "Security Governance Binder" that collects:

- Data classification policy

- Access control model

- Encryption standards

- Incident response plan

- Backup and disaster recovery procedures

- Staff training records

- Security audit logs

---

## 15. AI Copilot Usage for Security

When using AI coding assistants on tax preparation systems, always provide:

- This security-guidance document

- The gap analysis

- The checklist

Then use instructions similar to:

    You are updating this tax preparation system to align with our Security & Data Protection Guidance.

    - Do not modify security or encryption settings without explicit review.

    - Do not weaken access controls, logging, or encryption.

    - When proposing changes, explain how they support data protection, integrity, or auditability.

    - Always reference docs/security-guidance.md and docs/gap-analysis.md before making changes.

This ensures AI tools strengthen rather than erode security posture.

---

## 16. Summary

This guidance provides practical, practice-focused security and data protection readiness for the 2025 tax filing season. It should be updated as systems evolve and as IRS publishes additional security requirements or guidance.

**Key Priorities:**

1. Encrypt client data at rest and in transit
2. Implement strong access controls and audit logging
3. Secure e-filing credentials and transmissions
4. Train staff on security best practices
5. Maintain incident response procedures

