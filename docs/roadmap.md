# Project Roadmap & Governance

## Vision & Milestones
| Quarter | Milestone | Notes |
| --- | --- | --- |
| 2024 Q2 | Stand up MOSID ↔ NOC source-of-truth dataset and expose via internal API. | Depends on ingestion workflow outlined in the MOSID gap analysis.【F:reports/mosid_gap_analysis.md†L31-L57】 |
| 2024 Q3 | Expand résumé templates to cover top 20 CAF MOSIDs by population. | Requires SME backlog prioritisation and refreshed mappings to avoid stale civilian translations.【F:reports/mosid_gap_analysis.md†L59-L86】 |
| 2024 Q4 | Automate quarterly governance review with coverage KPIs and audit logging of mapping versions. | Builds on audit recommendations and refresh cadence established in the gap analysis.【F:reports/mosid_gap_analysis.md†L88-L112】 |

## Governance Rituals
- **Monthly data ingestion sync:** Confirm CAF change notices and Statistics Canada NOC updates have run; log any failures and create remediation tickets.【F:reports/mosid_gap_analysis.md†L88-L100】
- **Quarterly SME review:** Validate civilian translations, retire superseded MOSIDs, and approve new mappings before production deployment.【F:reports/mosid_gap_analysis.md†L88-L100】
- **Program increment checkpoint:** Present coverage metrics (MOSIDs mapped vs. total, mappings aged >12 months) and outstanding remediation actions to leadership.【F:reports/mosid_gap_analysis.md†L101-L112】

## Tracking & Accountability
| Workstream | Description | RACI |
| --- | --- | --- |
| Data ingestion & refresh | Automate MOSID/NOC pulls, maintain source-of-truth tables, and version metadata. | **R:** Platform Engineering / Data Engineering<br>**A:** Product Lead<br>**C:** Military SME<br>**I:** Compliance |
| Template expansion | Build and validate civilian résumé narratives for prioritised MOSIDs. | **R:** Product + Military SMEs<br>**A:** Product Lead<br>**C:** Labour Market Analyst<br>**I:** Engineering |
| Audit & reporting | Instrument API responses and dashboards with mapping versions and coverage KPIs. | **R:** Application Engineering<br>**A:** Engineering Lead<br>**C:** Compliance<br>**I:** Product |

## Artifact Register
| Artifact | Purpose | Refresh Cadence | Owner |
| --- | --- | --- | --- |
| `reports/mosid_gap_analysis.md` | Central coverage status, remediation priorities, and cadence guidance. | Update monthly or when major CAF/NOC changes occur.【F:reports/mosid_gap_analysis.md†L88-L112】 | Product Ops |
| MOSID/NOC Source Table | Structured mapping repository powering résumé translations. | Automated monthly refresh with manual hotfix support.【F:reports/mosid_gap_analysis.md†L82-L100】 | Data Engineering |
| SME Template Backlog | Prioritised list of MOSIDs needing civilian narratives. | Reviewed quarterly during SME governance session.【F:reports/mosid_gap_analysis.md†L74-L95】 | Product |

## Open Risks & Mitigations
1. **Stale occupational taxonomies** – Mitigated by enforcing automated ingestion checks and dashboard alerts for mappings older than 12 months.【F:reports/mosid_gap_analysis.md†L31-L112】
2. **Insufficient SME capacity** – Track staffing in governance sessions; escalate gaps to leadership two quarters ahead of planned template expansions.【F:reports/mosid_gap_analysis.md†L59-L95】
3. **Audit blind spots** – Integrate mapping version IDs into application logs and expose in reporting dashboards per remediation plan.【F:reports/mosid_gap_analysis.md†L74-L86】
