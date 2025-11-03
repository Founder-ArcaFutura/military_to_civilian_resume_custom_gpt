# Military to Civilian Resume Backend

This backend is a Model Context Protocol (MCP) server that provides tools for translating Canadian Armed Forces (CAF) military experience into civilian resume content. It is designed to be used as a data source for a custom GPT.

## Getting Started

1. Install dependencies and launch the server:

   ```bash
   cd backend
   poetry install
   poetry run python app/mcp_server.py
   ```

2. The server will expose the following tools to an MCP client:

   - `get_rank_data`: Retrieves responsibilities for a given rank.
   - `get_mosid_data`: Retrieves NOC equivalencies and task statements for a given MOSID.
   - `get_mosid_data_batch`: Retrieves NOC equivalencies and task statements for a list of MOSIDs.

## Project Structure

- `app/data`: Static reference data, including MOSID to NOC mappings and rank responsibilities.
- `app/mcp_server.py`: The MCP server implementation, which exposes the tools for translating military experience.
- `tests/`: Automated tests for the MCP server.

## Testing

To run the tests:

```bash
cd backend
poetry run pytest
```
