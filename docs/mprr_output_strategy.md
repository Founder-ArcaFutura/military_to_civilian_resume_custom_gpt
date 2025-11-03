# MPRR Field Output Strategy

This document summarizes how the MPRR data dictionary fields are represented in civilian résumé outputs.

## Narrative vs. Tabular Outputs

| Field Key | Label | Output Type | Rationale |
|-----------|-------|-------------|-----------|
| `service_history` | Service History Entry | Narrative bullet(s) | Contains mission context, leadership scope, and outcomes that translate best into résumé achievements. |
| `qualifications` | Qualifications | Tabular facts | Course names and completion dates are typically listed as factual credentials. |
| `awards` | Honours and Awards | Tabular facts (with optional short narrative) | Award titles and citations are primarily factual; short descriptors may be added as needed. |

## Narrative Coverage

Narrative outputs are currently focused on the `service_history` field and use template patterns defined in `docs/templates/service_history_narratives.md`.

## Validation Plan

1. Review narrative templates with a CAF career counselor and a civilian hiring manager to confirm language, required inputs, and tone.
2. Collect feedback on clarity, measurability, and civilian readability.
3. Iterate on template language and metadata based on stakeholder feedback.
4. Log approvals and changes in a revision history appended to each template file.

> **Status:** External validation is pending. Schedule stakeholder sessions once draft templates are internally approved.
