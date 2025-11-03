# MNET MOSID ↔ NOC Source Data

This directory contains source tables published by the Canadian Armed Forces (CAF) Military Occupational Structure Identification (MOSID) to National Occupational Classification (NOC) crosswalk.

## Provenance

The file `mnet_mosid_noc_2023.csv` was manually transcribed on 2024-05-15 from the PDF table "Military to Civilian Occupation Translator" (version 2023-09-15) published on the CAF Military to Civilian Transition (MNET) site: <https://www.canada.ca/en/department-national-defence/services/benefits-military/transition/occupation-translator.html>.

The transcription preserves the canonical MOSID, CAF occupation title, paired NOC 2021 code and label, and the short role description provided in the table. Column order and header casing match the published table to facilitate reproducible parsing.

## Staleness

The CAF table is updated infrequently and the currently available publication is timestamped September 15, 2023. Users should validate with the CAF Transition Group for newer releases before relying on these mappings in production workflows.

If a more recent table is published, place the new file in this folder and update the transcription date above.
