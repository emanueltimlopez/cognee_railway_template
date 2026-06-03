# Cognee Railway Deployment Template

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/deploy/SKKN1Y?referralCode=YqmMB-&utm_medium=integration&utm_source=template&utm_campaign=generic)

This repository is a deployment-focused fork of [topoteretes/cognee](https://github.com/topoteretes/cognee) for Railway.

It is intentionally trimmed to the files needed to:

- deploy a private `cognee-api` backend
- deploy a public `cognee-mcp` service in API/SSE mode
- provision managed PostgreSQL with pgvector
- generate a Railway template from a working project

## What this template deploys

- `cognee-api` as the private Cognee backend
- `cognee-mcp` as the public MCP service in API/SSE mode
- `postgres` for relational, graph, and vector persistence

## Railway MCP endpoint

After deployment, point OpenCode or another MCP client at the public `cognee-mcp` domain with the `/sse` suffix:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "cognee": {
      "type": "remote",
      "url": "https://<cognee-mcp-service>.up.railway.app/sse",
      "enabled": true,
      "oauth": false
    }
  }
}
```

The `cognee-mcp` service talks to the private `cognee-api` service over Railway internal networking using `API_URL=http://cognee-api.railway.internal:8080`.

## Safe Railway environment policy

Use private Railway networking for all service-to-service communication inside the same Railway project and environment.

Use internal/private values for:

- `DB_HOST`
- `GRAPH_DATABASE_HOST`
- `VECTOR_DB_HOST`
- `GRAPH_DATABASE_URL`
- `VECTOR_DB_URL`
- `API_URL` from `cognee-mcp` to `cognee-api`

Preferred internal hosts:

- `postgres.railway.internal`
- `cognee-api.railway.internal`
- `cognee-mcp.railway.internal`

Use public values only for:

- end-user and client connections
- OpenCode / Claude Code / MCP client configuration
- local debugging from outside Railway
- direct laptop access to Postgres via Railway TCP proxy

Public-only examples:

- `RAILWAY_PUBLIC_DOMAIN`
- `RAILWAY_STATIC_URL`
- `RAILWAY_SERVICE_COGNEE_API_URL`
- `RAILWAY_SERVICE_COGNEE_MCP_URL`
- `SERVE_URL`
- `DATABASE_PUBLIC_URL`
- `RAILWAY_TCP_PROXY_DOMAIN`
- `RAILWAY_TCP_PROXY_PORT`

Do not use public proxy/database URLs for internal runtime traffic between Railway services. They are slower and may incur egress/network charges.

## OpenAI-compatible model configuration

This template is configured for a single-user deployment with any OpenAI-compatible API.
Use OpenAI, OpenRouter, a LiteLLM proxy, vLLM, or another endpoint that accepts
OpenAI-style chat/completions and embeddings requests.

Required LLM variables:

- `LLM_PROVIDER=custom`
- `LLM_ENDPOINT=<openai-compatible-base-url>`
- `LLM_MODEL=<chat-model-name>`
- `LLM_API_KEY=<api-key>`

Required embedding variables:

- `EMBEDDING_PROVIDER=litellm`
- `EMBEDDING_ENDPOINT=<openai-compatible-base-url>`
- `EMBEDDING_MODEL=<embedding-model-name>`
- `EMBEDDING_DIMENSIONS=<embedding-vector-size>`
- optionally `EMBEDDING_API_KEY=<embedding-api-key>` if you do not want to reuse `LLM_API_KEY`

Example OpenAI official configuration:

- `LLM_ENDPOINT=https://api.openai.com/v1`
- `LLM_MODEL=gpt-4o-mini`
- `EMBEDDING_ENDPOINT=https://api.openai.com/v1`
- `EMBEDDING_MODEL=text-embedding-3-large`
- `EMBEDDING_DIMENSIONS=3072`

Example OpenRouter configuration:

- `LLM_ENDPOINT=https://openrouter.ai/api/v1`
- `LLM_MODEL=openrouter/openai/gpt-4o-mini`
- `EMBEDDING_ENDPOINT=https://openrouter.ai/api/v1`
- `EMBEDDING_MODEL=openrouter/google/gemini-embedding-2-preview`
- `EMBEDDING_DIMENSIONS=3072`

## Required user-provided variables

- `LLM_API_KEY`
- `LLM_ENDPOINT`
- `LLM_MODEL`
- `EMBEDDING_ENDPOINT`
- `EMBEDDING_MODEL`
- `EMBEDDING_DIMENSIONS`
- optionally `EMBEDDING_API_KEY` if you do not want to reuse `LLM_API_KEY`

## Publish checklist

- `cognee-api /health` returns `200`
- `cognee-mcp /health` returns `200`
- `cognee-mcp /sse` returns `200`
- login works on the backend
- `add -> cognify -> search` works on a fresh dataset
- Postgres shows dataset persistence and nonzero graph data
- OpenCode connects to the MCP server successfully
- OpenCode can execute a real Cognee tool call successfully

## Current verified live references

- Backend API: `https://cognee-api-production-81bb.up.railway.app`
- MCP SSE: `https://cognee-mcp-production-9beb.up.railway.app/sse`

## Related files

- `railway-template.json` — production Railway template
- `railway.toml` — backend deployment config for direct CLI deploys
- `Dockerfile` — backend image
- `Dockerfile.mcp` — MCP wrapper image that honors Railway `PORT`
- `distributed/deploy/README.md` — upstream-style deployment notes
