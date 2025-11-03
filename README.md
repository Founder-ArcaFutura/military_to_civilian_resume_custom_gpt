# Military to Civilian Resume Translator

## Overview

This repository contains the backend service for a custom GPT designed to translate Canadian Armed Forces (CAF) Military Personnel Record Résumés (MPRR) into civilian-friendly language. The service uses a simple, data-focused approach to provide accurate and relevant translations, helping veterans effectively communicate their skills and experience to civilian employers.

## Key Principles

*   **Data-Focused Backend:** This service is designed as a straightforward, data-centric backend. It avoids over-engineering to focus on its core mission: providing high-quality, relevant data to the custom GPT.

*   **Stateless and Private:** User privacy is a core principle. The service is **stateless** and does not log, store, or retain any personal information provided by the user. Every transaction is treated as a new, anonymous request.

*   **Augmentation, Not Replacement:** This tool is intended to be a powerful aid for transitioning service members, but it is not a replacement for the official counseling and resources provided by the CAF Transition Group.

## How It Works

The system uses a **Retrieval-Augmented Generation (RAG)** pattern. When the custom GPT receives a user's military experience, the backend service:
1.  **Retrieves** relevant data from its knowledge base, which contains mappings of military occupations (MOSIDs) to civilian equivalents (NOCs) and standardized descriptions of rank responsibilities.
2.  **Augments** the GPT's context with this factual data.
3.  The GPT then **Generates** a high-quality, civilian-friendly translation of the user's experience, grounded in the provided data.

## Getting Started

To run the server locally, follow these steps:

1.  **Install Dependencies:**
    Navigate to the `backend` directory and use Poetry to install the required packages.
    ```bash
    cd backend
    poetry install
    ```

2.  **Populate the Database:**
    The server uses a local SQLite database that needs to be populated with the project's data. Run the population script:
    ```bash
    poetry run python scripts/populate_db_from_json.py
    ```

3.  **Start the Server:**
    Run the server using `uvicorn`. The API will be available at `http://localhost:8100`.
    ```bash
    poetry run uvicorn app.mcp_server:app --host 0.0.0.0 --port 8100
    ```

## Data Pipeline

The project's data is managed through a set of scripts that handle scraping, verification, and database population.

*   **Data Sources:**
    *   **MNET Website:** The primary source for MOSID-to-NOC mappings is the official [MNET Website](https://caface-rfacace.forces.gc.ca/mnet-oesc/en/cafSearch).
    *   **`rank_responsibilities.yaml`:** This file contains a manually curated list of responsibilities for each CAF rank.

*   **Data Management Scripts:**
    *   **`update_mnet_data.py`:** This script scrapes the MNET website to update the local `mnet_data.json` file with the latest MOSID information.
    *   **`populate_db_from_json.py`:** This script populates the SQLite database from the `mnet_data.json` and `rank_responsibilities.yaml` files.
    *   **`verify_mosids.py`:** This script compares the MOSIDs in the local database against the live MNET website and reports any discrepancies.

## Testing

To run the test suite, navigate to the `backend` directory and run `pytest`:
```bash
cd backend
poetry run pytest
```

## Custom GPT Instructions

For guidance on how to configure your custom GPT to use this backend service, please refer to the instructions in `docs/gpt_instructions.md`.
