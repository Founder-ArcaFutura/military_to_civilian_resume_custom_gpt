# MPRR Field Map (Living Data Dictionary)

This dictionary maps MPRR data elements to their résumé equivalents. Update as new fields are introduced or definitions change.

| Field Name | Description | Source Section | Data Type | Sensitivity | Transformation / Handling |
| --- | --- | --- | --- | --- | --- |
| service_number_truncated | Last four digits of the member's service number for record linkage. | Service Member Identification | string | Restricted (PII) | Store separately from résumé outputs; never display in résumé. |
| rank_current | Current rank at time of extract. | Service Member Identification | string | Controlled | Translate to civilian-friendly leadership level (e.g., "Captain" → "Mid-level Manager"). |
| component | Component/element (Regular, Reserve, etc.). | Service Member Identification | string | Controlled | Normalize to standardized list. |
| force_element | Navy, Army, Air Force, Special Operations indicator. | Service Member Identification | string | Controlled | Map to résumé summary keywords. |
| enrolment_date | Date member joined service. | Service History | date | Controlled | Convert to ISO-8601 (`YYYY-MM-DD`). |
| release_date | Date member released (if applicable). | Service History | date/null | Controlled | ISO-8601; can be null for active members. |
| positions | Array of role records (unit, position title, start/end dates). | Service History | array<object> | Controlled | Normalize titles; derive civilian equivalents via translation matrix. |
| mosid | Military Occupation Specification Identifier. | Occupational Classification | string | Controlled | Map to civilian occupation taxonomy (NOC/SOC). |
| mosid_description | Human-readable description of MOSID. | Occupational Classification | string | Open | Use as résumé skills summary input. |
| qualification_level | Operational qualification level within trade. | Occupational Classification | string | Controlled | Translate to proficiency scale (Foundational/Intermediate/Advanced). |
| courses_completed | List of courses with completion status. | Professional Qualifications | array<object> | Controlled | Normalize provider names; filter to relevant civilian certifications. |
| certifications_active | Civilian-recognized certifications. | Professional Qualifications | array<object> | Open | Include in résumé certification section. |
| deployments | Deployment records (mission, theatre, role, start/end). | Deployments & Operational Experience | array<object> | Controlled | Mask mission codes flagged as restricted; generalize location if classified. |
| operational_impacts | Summary of mission outcomes or metrics. | Deployments & Operational Experience | string | Controlled | Redact sensitive figures; convert to quantifiable achievements. |
| awards | Honors and awards received. | Awards & Decorations | array<object> | Controlled | Display award name and year only; omit citation text if classified. |
| languages | Official language profile scores and additional languages. | Language & Cultural Competencies | array<object> | Open | Convert CAF language profile to CEFR equivalents. |
| education | Formal education credentials. | Education & Civilian Credentials | array<object> | Open | Ensure institution names match official transcripts. |
| security_clearance_level | Highest current clearance level. | Security Clearances | string | Controlled | Display only highest level; omit issuance/expiry dates in résumé. |
| security_clearance_expiry | Expiry date for clearance. | Security Clearances | date | Restricted | Retain internally; not shown on résumé. |
| medical_category | Current medical category. | Medical & Fitness Readiness | string | Restricted (PHI) | Exclude from résumé exports; store in secure enclave. |
| fitness_scores | Annual fitness evaluation scores. | Medical & Fitness Readiness | array<object> | Restricted (PHI) | Exclude from résumé exports. |
| contact_email | Member's preferred contact email. | Service Member Identification | string | Restricted (PII) | Separate consent required before use in résumé. |
| contact_phone | Member's phone number. | Service Member Identification | string | Restricted (PII) | Store encrypted; not published without consent. |
| emergency_contact | Name and phone for emergency contact. | Service Member Identification | object | Restricted (PII) | Exclude entirely from résumé system. |
| remarks | Free-text remarks field. | General | string | Controlled | Scan for sensitive keywords; redact before résumé use. |

## Sensitivity Levels

* **Open** – Safe for résumé export.
* **Controlled** – Requires review; only export derived, non-sensitive values.
* **Restricted (PII/PHI)** – Must be masked or excluded from résumé outputs.

## Review Log

| Date | Reviewer | Notes |
| --- | --- | --- |
| 2024-05-07 | Data Governance SME | Confirmed exclusion of medical & fitness data. |
| 2024-05-08 | Security Officer | Flagged mission-specific deployment codes as restricted; masking required. |
| 2024-05-09 | Privacy Officer | Approved handling of contact data with consent workflow. |

> **Next Review:** Schedule quarterly reviews or upon introduction of new data sources.
