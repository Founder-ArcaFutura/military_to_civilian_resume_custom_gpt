# ChatGPT Custom Action Configuration

The CAF Resume Helper backend can be exposed to a Custom GPT through ChatGPT Actions.
This folder contains the manifest and OpenAPI specification required by OpenAI to
register the action.

## Files

- `chatgpt_actions_manifest.json` – Action manifest served from
  `https://resume-helper.example.com/.well-known/ai-plugin.json`.
- `chatgpt_actions_openapi.yaml` – OpenAPI 3.1 definition of the read-only endpoints.

## Deployment Checklist

1. **Host the API.** Run the FastAPI deployment (or HTTP gateway around the MCP server)
   at `https://resume-helper.example.com` and ensure it implements the three paths
   declared in the OpenAPI document.
2. **Serve the manifest.** Make the manifest available from
   `https://resume-helper.example.com/.well-known/ai-plugin.json` and update the
   placeholder domains, contact details, and logo URL to match your environment.
3. **Protect with API keys.** Issue API keys to trusted ChatGPT users and verify that
   each request includes the `X-API-Key` header.
4. **Upload to Custom GPT.** In the ChatGPT builder, select "Actions" → "Import from URL"
   and supply the manifest URL.

Once configured, the GPT can call the following operations:

- `GET /v1/ranks/{rankName}` – returns responsibilities associated with a CAF rank.
- `GET /v1/mosids/{mosidCode}` – returns civilian NOC equivalencies for a MOSID.
- `POST /v1/mosids:batchLookup` – resolves multiple MOSIDs in a single request.

These responses mirror the deterministic datasets stored under `backend/app/data/` and
are suitable for prompting workflows that translate Canadian Armed Forces experience
into civilian résumé language.
