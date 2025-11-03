# CAF Resume Helper MCP API Specification

## Overview
The Military to Civilian Resume backend runs as a [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server named **"CAF Resume Helper"**. It bootstraps a bundled SQLite database from the curated reference datasets under `backend/app/data/` and exposes a small set of read-only tools for converting Canadian Armed Forces records into civilian résumé context.【F:backend/app/mcp_server.py†L6-L153】

The server performs the following on start-up:
- Ensures tables for MOSID profiles, NOC equivalencies, task statements, ranks, and rank responsibilities exist in the local SQLite database.【F:backend/app/mcp_server.py†L9-L54】
- Loads MOSID↔NOC mappings from `mnet_data.json` and rank duty catalogues from `rank_responsibilities.yaml`, inserting any missing records into SQLite.【F:backend/app/mcp_server.py†L56-L88】
- Registers three MCP tools that clients can invoke to retrieve responsibilities and civilian-aligned equivalencies.【F:backend/app/mcp_server.py†L94-L153】

All tools return JSON-serializable dictionaries. Missing records are represented by an empty object (`{}`) to simplify downstream prompting logic.【F:backend/app/mcp_server.py†L103-L142】

## Tool Catalogue
| Tool name | Purpose | Input signature | Response shape |
|-----------|---------|-----------------|----------------|
| `get_rank_data` | Look up responsibilities for a specific CAF rank. | `rank_name: string` | `{ "responsibilities": string[] }` or `{}` when not found. |
| `get_mosid_data` | Retrieve NOC equivalencies and task statements for one MOSID code. | `mosid_code: string` | `{ "equivalencies": Equivalency[] }` or `{}` when not found. |
| `get_mosid_data_batch` | Resolve multiple MOSID codes in one call. | `mosid_codes: string[]` | `{ "<mosid_code>": MOSIDPayload }` mapping for each requested MOSID. |

`Equivalency` objects contain the `noc_code`, `civilian_title`, and a list of `task_statements`. `MOSIDPayload` is the same object returned by `get_mosid_data` for a single MOSID code.【F:backend/app/mcp_server.py†L127-L149】

## Tool Definitions

### `get_rank_data`
- **Description:** Returns the duty statements aligned to a Canadian Armed Forces rank.
- **Input:**
  - `rank_name` (string, required): Exact rank label as stored in the `rank_responsibilities.yaml` source (e.g., `"Captain"`).【F:backend/app/mcp_server.py†L76-L108】
- **Response:**
  - Success: `{ "responsibilities": [string, ...] }` where each string is a responsibility sentence associated with the rank.【F:backend/app/mcp_server.py†L107-L111】
  - Not found: `{}` (empty object).【F:backend/app/mcp_server.py†L101-L105】
- **Notes:** Responsibilities are ordered as they appear in the YAML source. Clients should treat the response as authoritative canonical phrasing.

### `get_mosid_data`
- **Description:** Provides the civilian labour market equivalencies for a CAF MOSID, including National Occupation Classification (NOC) codes and detailed task statements.
- **Input:**
  - `mosid_code` (string, required): Five-digit MOSID identifier (e.g., `"00005"`).【F:backend/app/mcp_server.py†L61-L140】
- **Response:**
  - Success: `{ "equivalencies": [ { "noc_code": string, "civilian_title": string, "task_statements": [string, ...] }, ... ] }`. The order matches the curated `mnet_data.json` entries for the MOSID.【F:backend/app/mcp_server.py†L124-L142】
  - Not found: `{}`.【F:backend/app/mcp_server.py†L118-L122】
- **Notes:** Each equivalency bundles a NOC code, the civilian job title, and the official task statements published for that NOC profile, enabling deterministic résumé bullet generation.

### `get_mosid_data_batch`
- **Description:** Convenience wrapper to query multiple MOSID codes in a single request.
- **Input:**
  - `mosid_codes` (array of strings, required): One or more MOSID identifiers.【F:backend/app/mcp_server.py†L144-L149】
- **Response:**
  - `{ "<mosid_code>": <payload>, ... }`, where `<payload>` is exactly the object returned by `get_mosid_data` for that MOSID. Missing MOSIDs map to `{}` to signal absence of curated data.【F:backend/app/mcp_server.py†L144-L149】
- **Notes:** Use this tool to hydrate prompt context for multiple service members without incurring repeated round-trips.

## Data Provenance
- **MOSID equivalencies** originate from `backend/app/data/mnet_data.json`, a curated mapping of MOSID codes to NOC descriptors and official task statements.【F:backend/app/mcp_server.py†L61-L75】
- **Rank responsibilities** come from `backend/app/data/rank_responsibilities.yaml`, capturing textual duty statements per rank.【F:backend/app/mcp_server.py†L76-L85】

Clients should refresh their cached knowledge only when these source files change, as the MCP server performs idempotent inserts and does not currently expose mutation endpoints.
