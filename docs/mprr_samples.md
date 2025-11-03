# MPRR Sample Extract Summary

To support résumé translation, we reviewed sanitized Military Personnel Record Résumé (MPRR) extracts drawn from:

1. **Canadian Armed Forces (CAF) publicly available templates** – anonymized examples from CAF transition resources and career services.
2. **Stakeholder-provided sanitized excerpts** – portions of service records with personal identifiers removed per stakeholder NDAs.
3. **NATO standard personnel record formats** – open reference documents aligning with joint personnel reporting standards.

## Recurring Sections

| Section | Typical Contents | Notes |
| --- | --- | --- |
| Service Member Identification | Service number, rank, component, element, force | Personally identifiable; ensure masking of service number beyond last four digits. |
| Service History | Enlistment date, release date (if applicable), positions held, units | Requires date normalization to ISO-8601; verify gaps with SME. |
| Occupational Classification (MOSID/MOC) | MOSID code, trade description, qualification level | Map to civilian-friendly job titles using translation table. |
| Professional Qualifications | Courses, certifications, completion dates, status | Include accreditation body and civilian equivalencies. |
| Deployments & Operational Experience | Mission name, role, theatre, duration | Flag locations with security classification; redact mission specifics if restricted. |
| Awards & Decorations | Award name, date, citation | Some citations may contain sensitive operational details; include summary only. |
| Medical & Fitness Readiness | Medical category, fitness test scores | Considered protected health information; exclude from résumé exports. |
| Security Clearances | Level, issued date, expiry | Only report highest active clearance; redact issuance details. |
| Language & Cultural Competencies | Official language profile, additional languages, cultural training | May inform résumé skills section; ensure optional disclosure. |
| Education & Civilian Credentials | Degrees, diplomas, civilian certifications | Validate against external transcripts if available. |

## Data Sensitivity Considerations

* **Restricted Data** – Medical readiness details, detailed deployment narratives, intelligence-related awards, and full service numbers are restricted and must be masked or excluded.
* **Controlled Unclassified Information (CUI)** – Security clearance levels and mission names are treated as CUI; redact specifics when generating public résumés.
* **Open Data** – Course titles, general employment history, and awards without operational detail can be retained.

## Follow-up Actions

* Store sanitized examples in the secure shared drive under `/restricted/mprr_samples/` with hashed filenames.
* Update this document as additional sample formats are received.
* Confirm with security team before incorporating any new data elements into résumé exports.
