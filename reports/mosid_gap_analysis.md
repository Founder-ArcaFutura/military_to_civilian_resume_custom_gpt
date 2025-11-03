# MOSID ↔ NOC Coverage Gap Analysis

_Last updated: 2025-10-29_

## Executive Summary
- Current résumé translation assets only cover four MOSID families and none contain authoritative NOC mappings, leaving the majority of CAF trades unsupported for civilian job matching.
- The reference MOSID/NOC equivalency feed (MNET) has been stale since 2019, and no alternative canonical dataset has been ingested into this project to compensate for taxonomy changes (e.g., NOC 2021 TEER migration).
- CAF occupational change notices continue to add, retire, or merge MOSIDs, creating drift risks if refresh cycles remain ad hoc.

## Data Sources Reviewed
- `backend/app/data/translation_templates.yaml` – enumerates the MOSID families represented in résumé generation templates.【F:backend/app/data/translation_templates.yaml†L1-L100】
- Historical notes in `conversation.md` flag the last known update to the MNET MOSID/NOC equivalency feed (2019).【F:conversation.md†L40-L63】
- `plan.md` captures intended ingestion of MOSID ↔ NOC mappings but does not document completion or refresh cadence.【F:plan.md†L7-L24】

## Coverage Snapshot
| MOSID Family | Civilian Template Coverage | NOC Mapping Present? | Notes |
| --- | --- | --- | --- |
| 00300 – Infantry Officer | ✅ | ❌ | Templates provide résumé phrasing but lack NOC identifiers.【F:backend/app/data/translation_templates.yaml†L3-L32】 |
| 00109 – Signals Technician | ✅ | ❌ | Civilian translations available; NOC equivalents absent.【F:backend/app/data/translation_templates.yaml†L33-L60】 |
| 00329 – Logistics Officer | ✅ | ❌ | Supply-chain focused civilian narratives only.【F:backend/app/data/translation_templates.yaml†L61-L90】 |
| 00168 – Medical Technician | ✅ | ❌ | Healthcare narratives provided without occupational codes.【F:backend/app/data/translation_templates.yaml†L91-L120】 |
| All other CAF MOSIDs | ❌ | ❌ | No templates or mappings exist in the repository.【F:backend/app/data/translation_templates.yaml†L1-L120】 |

## Outdated or At-Risk Mappings
- **MNET MOSID/NOC equivalency (2019):** Source noted as unchanged since 2019, preceding the Statistics Canada 2021 NOC/TEER revision, creating misalignment with current civilian job taxonomies.【F:conversation.md†L40-L63】
- **Unimplemented ingestion workflow:** The roadmap calls for harvesting MOSID/NOC data but no artifacts exist, confirming a gap between plan and execution.【F:plan.md†L13-L24】

## Priority Updates from Change Logs & External Datasets
| Priority | Trigger | Impacted Assets | Remediation | Proposed Owner |
| --- | --- | --- | --- | --- |
| High | CAF Military Occupational Structure updates (2023–2024 bulletins) introducing new MOSIDs and retiring legacy identifiers. | Translation templates, future MOSID catalog. | Ingest latest CAF change logs, cross-check with template catalog, and flag orphaned MOSIDs for content development. | Product + Military SME |
| High | Statistics Canada NOC 2021/TEER adoption replacing NOC 2016 codes referenced in legacy MNET feed. | Planned MOSID ↔ NOC mapping table, résumé output metadata. | Acquire NOC 2021 dataset, rebuild crosswalk (MOSID → NOC 2021), and expose version metadata in API responses. | Data Engineering |
| Medium | ESDC labour market outlook updates affecting skill-demand descriptors tied to MOSIDs. | Narrative templates, indicator weighting. | Append labour demand signals (growth, automation risk) to template metadata for prioritised trades. | Labour Market Analyst |

## Remediation Plan & Owners
1. **Establish source-of-truth inventory** – Stand up a structured table (e.g., Postgres/SQLite) for MOSID ↔ NOC mappings with version metadata before expanding template coverage.【F:plan.md†L13-L24】 _(Owner: Data Engineering)_
2. **Develop automated refresh workflow** – Script ingestion from CAF change bulletins and NOC datasets, with validation that highlights unmapped MOSIDs for SME review. _(Owner: Platform Engineering)_
3. **Curate template backlog** – Partner with MOSID-specific SMEs to draft civilian translations for high-volume trades surfaced by refreshed datasets. _(Owner: Product + SMEs)_
4. **Audit logging enhancements** – Extend existing translation audit trails to record mapping version IDs once datasets are integrated. _(Owner: Application Engineering)_

## Recommended Refresh Cadence
- **Data ingestion:** Automated monthly pull of CAF MOSID updates and Statistics Canada NOC changes, with manual override when urgent bulletins are released.
- **Template review:** Quarterly SME review cycle to incorporate labour-market shifts and verify mapping accuracy for high-demand MOSIDs.
- **Governance checkpoint:** Include coverage metrics (MOSIDs mapped vs. total, mappings aged >12 months) in program increment reviews to maintain executive visibility.

## Tracking & Reporting
- Publish refresh outcomes and outstanding gaps in `docs/roadmap.md` (see governance updates) so stakeholders can monitor progress and assign follow-up actions.
- Add MOSID coverage KPIs to the project scorecard once automated ingestion is operational, enabling trend analysis over time.
