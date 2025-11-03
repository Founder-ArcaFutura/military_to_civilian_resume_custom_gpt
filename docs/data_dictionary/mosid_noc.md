# MOSID ↔ NOC Crosswalk

The MOSID ↔ NOC dataset normalizes the CAF Military to Civilian Occupation Translator into a machine-readable format for resume generation pipelines.

## Raw inputs

* **Location:** `data/raw/`
* **Source:** CAF Military to Civilian Transition (MNET) MOSID ↔ NOC table (2023-09-15 publication).
* **File format:** CSV (UTF-8). Column names mirror the published table to simplify audits.

## ETL process

Run `python backend/scripts/ingest_mosid_noc.py` to parse all CSV/TSV files in `data/raw/` and emit normalized artifacts under `data/processed/`.

The loader trims whitespace, standardizes column headers, removes duplicate MOSID+NOC pairs, and captures lightweight metadata about the source file.

## Output artifacts

### `data/processed/mosid_noc.csv`
Tabular representation with one record per MOSID+NOC mapping.

### `data/processed/mosid_noc.json`
JSON array mirroring the CSV content for ingestion in JavaScript pipelines.

## Field definitions

| Field | Type | Description |
| --- | --- | --- |
| `mosid` | string | Four-digit Military Occupation Structure Identification (MOSID) code from the CAF translator. |
| `caf_title` | string | Official CAF occupation name associated with the MOSID. |
| `noc_code` | string | National Occupational Classification (NOC 2021) code paired to the MOSID in the CAF translator. |
| `civilian_title` | string | Civilian occupation title provided for the referenced NOC. |
| `role_description` | string | Narrative role description summarizing the CAF occupation in civilian terminology. |
| `source_file` | string | Filename of the raw source table from which the record was parsed. |
| `source_publication_date` | string\|null | Date or year parsed from the source filename when available. |
| `transcription_date` | string\|null | ISO date the ETL ran, populated automatically during ingestion. |

## Refresh cadence

To update the dataset, replace or add new raw files in `data/raw/` and re-run the ETL script. Commit both the raw source and regenerated processed artifacts along with an updated provenance note in `data/raw/README.md`.
