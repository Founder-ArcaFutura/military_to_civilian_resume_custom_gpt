# Privacy Guardrails & Deployment Postures for the Military-to-Civilian Resume Platform

## Current deployment posture (default)

The live design assumes a **no-retention, public-data-only workflow**:

- Members interact with the service through a Custom GPT front-end. Prompts and responses remain transient inside the ChatGPT session; the platform does not ingest, store, or index member-uploaded résumés or MPRRs.
- The backend exposes retrieval-augmented generation (RAG) actions that reference a curated knowledge base derived exclusively from publicly available MNET material (e.g., MOSID descriptions, historical job summaries) plus internally written civilian-language translations.
- Custom actions supply only the relevant MOSID snippets to ChatGPT at inference time. No member-specific text is persisted in platform storage, analytics tooling, or logs beyond ephemeral processing required to fulfill the request.
- Operators regularly review the curated MOSID content to ensure it remains free of personal identifiers and reflects the latest publicly released information.

Document this posture in architecture diagrams, runbooks, and procurement files so reviewers understand that the platform functions purely as a knowledge bridge rather than a system of record for MPRRs.

### Guardrails that still apply in the public-data posture

- **Source validation and provenance** – Track when MNET artifacts were harvested, maintain citations, and schedule periodic refreshes so outdated summaries can be flagged for review.
- **Content integrity** – Protect the curated MOSID dataset with access controls, change management, and backup/restore procedures to prevent tampering or unauthorized edits.
- **User guidance** – Provide UI notices instructing members not to paste full résumés, SINs, or health details into chat prompts. Reinforce that the tool offers language support only and does not store submissions.
- **Third-party assurances** – Confirm the selected OpenAI plan enforces enterprise retention controls (no training on prompts, limited log retention) and capture those assurances in supplier management files.
- **Breach and incident response** – Maintain security contacts and runbooks in case the curated knowledge base or API credentials are compromised.

## Alternate posture: full MPRR ingestion (legacy design)

The remainder of this document captures the high-assurance controls required **only if the platform ever ingests, stores, or processes actual MPRRs**. Treat this section as an appendix for a future deployment scenario and keep it separate from the default public-data implementation dossier.

### Regulatory context

Canadian Armed Forces (CAF) Military Personnel Record Résumés (MPRRs) contain personal information that is subject to multiple federal privacy obligations:

- **Privacy Act (R.S.C., 1985, c. P-21)** – Establishes baseline duties for federal institutions collecting, retaining, and disclosing personal information, including the need for lawful authority, purpose specification, accuracy, safeguards, retention schedules, and data subject rights (Sections 4–8, 6(2), 7, 8(1)).
- **Department of National Defence (DND) and CAF Policy (DAOD 1002-0/1002-1)** – Requires compliance with the Privacy Act, assignment of privacy responsibility to commanding officers, maintenance of Personal Information Banks (PIBs), privacy impact assessments (PIAs), and implementation of risk-based safeguards for personal information held by DND/CAF.
- **DAOD 6002-2 (Management of Personal Information)** – Provides operational direction on consent management, access controls, recordkeeping, and breach reporting for personal information, including MPRRs.
- **Directive on Privacy Practices (Treasury Board Secretariat)** – Requires privacy protocols, retention/disposition aligned with Library and Archives Canada (LAC) schedules, and reporting/mitigation of privacy breaches.
- **Library and Archives of Canada Act** – Governs retention and disposition authorizations for federal records, requiring adherence to approved retention schedules for personnel records.
- **Security of Information Act & DND Security Orders** – Mandate safeguards proportional to the sensitivity of information, including IT security controls for Protected B information (which typically covers MPRR data).

These obligations apply when the platform stores, processes, or transmits MPRRs, whether in production systems, staging environments, support tooling, or analytical datasets.

### Key obligations for the platform

1. **Lawful authority & purpose specification**  
   - Collect and use MPRRs only with documented authority from DND/CAF and for the explicit purpose of assisting members with civilian resumes.  
   - Maintain a Personal Information Bank (PIB) entry describing purpose, categories, and retention.

2. **Consent & notice**  
   - Obtain informed, written consent from the member before ingesting their MPRR, citing the lawful authority, intended uses, retention period, and potential disclosures.  
   - Provide a privacy notice that meets TBS Directive requirements (purpose, legal authority, uses, rights, contact info).  
   - Allow members to withdraw consent and outline implications (e.g., deletion of their data and service termination).

3. **Collection minimization & accuracy**  
   - Ingest only MPRR fields necessary for resume translation.  
   - Validate data against the authoritative MPRR to ensure accuracy before use.  
   - Document rationale for each data element retained.

4. **Access controls**  
   - Restrict access to authorized personnel with a demonstrated need-to-know (Protected B handling).  
   - Enforce role-based access control (RBAC) with least privilege, MFA, session logging, and quarterly access reviews.

5. **Safeguards & security controls**  
   - Encrypt MPRRs at rest using AES-256 (or equivalent) and in transit using TLS 1.2+.  
   - Apply file-level encryption for backups and ensure keys are managed via a FIPS 140-2 compliant HSM/KMS.  
   - Maintain audit logs for all read/write/export operations and protect logs from tampering.  
   - Conduct Privacy Impact Assessments (PIAs) and Threat Risk Assessments (TRAs) prior to production release; update after material changes.

6. **Retention & disposition**  
   - Align retention with LAC-approved schedules (e.g., destroy MPRRs within 2 years after last active use unless a longer period is authorized).  
   - Implement automated deletion workflows and documented destruction certificates (digital shredding standards).  
   - Retain consent records for at least two years after data deletion to evidence compliance.

7. **Redaction & disclosure**  
   - Redact SINs, medical data, and other sensitive fields from any exports or reports not strictly required for resume generation.  
   - Ensure disclosures to third parties comply with section 8(2) of the Privacy Act (e.g., consent, legal authority).  
   - Provide members access to their data upon request (section 12) and correct inaccuracies promptly.

8. **Breach response**  
   - Follow TBS privacy breach protocol: detect, contain, assess, notify affected members, notify the Office of the Privacy Commissioner (OPC) and TBS if material.  
   - Maintain incident response runbooks and post-incident review documentation.

### Consent requirements & workflow

#### Consent prerequisites

- Identify lawful authority (e.g., National Defence Act, DAOD 1002) and cite within consent form.
- Provide clear explanation of purposes, uses, retention, safeguards, and potential disclosures.
- Explain rights to withdraw consent, access records, and file complaints with the OPC.
- Obtain positive action (e-signature or written) and capture timestamp, member service number, and contact details.
- Store consent record separately from operational datasets but link via unique identifier.

#### Sample consent workflow

1. **Pre-ingestion briefing:** Display privacy notice and consent form on secure portal; offer downloadable PDF.  
2. **Member review:** Member reviews the notice, acknowledges understanding, and can request clarification via contact info.  
3. **Affirmative consent capture:** Member signs (digital signature) and submits; system records metadata (timestamp, IP, version of notice).  
4. **Verification:** Platform verifies member identity (CAC card or CAF identity provider).  
5. **Confirmation:** Email confirmation with reference number, consent summary, and withdrawal instructions.  
6. **Ingestion unlock:** System accepts MPRR upload/API ingest only after consent record exists and identity verified.  
7. **Withdrawal handling:** Provide dashboard workflow for withdrawal; on request, trigger deletion job and send completion certificate.

#### Sample consent text (excerpt)

> **Purpose and Authority**  
> Your Military Personnel Record Résumé (MPRR) is collected under the authority of the National Defence Act and DAOD 1002-0/1002-1 to provide translation of your service history into a civilian résumé.  
> 
> **Uses and Disclosures**  
> Your information will be used solely to generate tailored résumé content and will not be disclosed outside the Department of National Defence without your written consent, unless required by law.  
> 
> **Safeguards**  
> Your MPRR will be stored in encrypted systems located in Canada. Access is limited to authorized personnel supporting the résumé translation process.  
> 
> **Retention**  
> Your MPRR will be retained for up to two years after your last active use of the service, after which it will be securely destroyed unless you renew your consent.  
> 
> **Your Rights**  
> You may access or correct your information, withdraw consent, or file a complaint with the Office of the Privacy Commissioner of Canada. Contact privacy@mil2civ.gc.ca or 1-800-000-0000 for assistance.

### Handling rules & technical implications

| Area | Guardrail | Tooling Implications |
| --- | --- | --- |
| **Encryption at rest** | AES-256 encryption for databases, object storage, backups; key rotation annually or after personnel changes. | Use cloud KMS with Hardware Security Module (HSM) backing; integrate with secrets manager; enforce envelope encryption for files. |
| **Encryption in transit** | TLS 1.2+ for all services; mutual TLS for internal microservices. | Configure ingress controllers/load balancers with approved ciphers; automate certificate issuance via PKI. |
| **Access control** | RBAC, MFA, Just-In-Time admin access, quarterly access reviews. | Integrate with CAF IdP (SAML/OAuth); automate provisioning/deprovisioning via IAM; deploy privileged access management (PAM) tooling. |
| **Logging & monitoring** | Immutable audit logs, retention 2 years, anomaly detection. | Implement centralized log service (e.g., SIEM) with WORM storage; define log schema capturing user, action, record IDs. |
| **Redaction** | Remove SIN/medical data before generating exports; mask PII in lower environments. | Build data transformation pipeline with configurable redaction rules; leverage DLP scanners for QA. |
| **Data minimization** | Only required MPRR fields accessible; pseudonymize identifiers in analytics. | Configure ETL to exclude optional fields; use tokenization for member IDs when training models. |
| **Retention & deletion** | Automated deletion 2 years post-use or upon withdrawal; evidence of destruction. | Implement scheduled deletion jobs with attestations; integrate with ticketing system for approval/audit. |
| **Backups & DR** | Encrypted, access restricted, tested annually; ensure deletion propagates. | Use backup solution supporting object-level delete/crypto shredding; document restoration testing. |
| **Breach response** | 24h detection/containment, notifications per TBS protocol. | Maintain incident response tooling (SOAR), run tabletop exercises, automate breach assessment templates. |

### Next steps

1. **Legal review:** Submit guardrails to DND/CAF legal counsel and Privacy Office for validation of authority, consent language, and retention schedules.  
2. **Security assessment:** Engage Departmental Security Officer (DSO) to ensure controls meet Protected B requirements and integrate with departmental IT security standards.  
3. **PIPEDA/third-party considerations:** If external vendors are involved, ensure contracts include privacy clauses, data residency in Canada, and audit rights.  
4. **Documentation:** Incorporate guardrails into the System Security Plan (SSP), Privacy Impact Assessment (PIA), and onboarding runbooks.  
5. **Training:** Develop mandatory privacy and security training for all platform operators handling MPRRs.

