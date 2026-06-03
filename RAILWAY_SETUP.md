# Railway Setup

This repository is intended to be wired into Railway as three services:

- `cognee-api`
- `cognee-mcp`
- `postgres`

The easiest stable setup is:

- `cognee-api` sourced from this GitHub repo using `railway.api.toml`
- `cognee-mcp` sourced from this GitHub repo using `railway.mcp.toml`
- `postgres` as a Railway PostgreSQL plugin service

## Which Railway file does what?

- `railway-template.json`
  - Used for Railway template generation and template metadata
  - Describes which services should be provisioned and what variables/defaults they expose
  - Not the file Railway uses as the live build/deploy config for an individual service

- `railway.toml`
  - Generic backend deploy config in this repo
  - Can be used for a simple single-service backend deploy

- `railway.api.toml`
  - Service-specific deploy config for `cognee-api`
  - Railway reads this when you point the `cognee-api` service's Config-as-code setting to it

- `railway.mcp.toml`
  - Service-specific deploy config for `cognee-mcp`
  - Railway reads this when you point the `cognee-mcp` service's Config-as-code setting to it

In short:

- Template generation: `railway-template.json`
- Actual per-service deploy settings: `railway.api.toml` and `railway.mcp.toml`

## 1. Push this repository to GitHub

Railway template generation requires app services to have a reusable source.

Make sure this repository is pushed to GitHub and visible to Railway.

## 2. Create or verify the PostgreSQL service

In Railway:

1. Open your project
2. Click `New`
3. Add a `PostgreSQL` service
4. Keep the default service name or rename it to `postgres`

This service provides:

- `PGHOST`
- `PGPORT`
- `PGUSER`
- `PGPASSWORD`
- `PGDATABASE`

## 3. Configure `cognee-api`

In Railway:

1. Create a new service named `cognee-api`
2. Connect it to this GitHub repository
3. In `Build`, select `Dockerfile`
4. In `Config-as-code`, set the Railway config file to:

   `railway.api.toml`

5. In `Source`, leave root directory empty unless you intentionally move files into a subdirectory

### Required variables for `cognee-api`

Set these variables on the `cognee-api` service:

- `LLM_API_KEY`
- `LLM_ENDPOINT`
- `LLM_MODEL`
- `EMBEDDING_ENDPOINT`
- `EMBEDDING_MODEL`
- `EMBEDDING_DIMENSIONS`
- optional `EMBEDDING_API_KEY` if not reusing `LLM_API_KEY`

The template is designed for any OpenAI-compatible provider:

- `LLM_PROVIDER=custom`
- `LLM_ENDPOINT=<openai-compatible-base-url>`
- `LLM_MODEL=<chat-model-name>`
- `EMBEDDING_PROVIDER=litellm`
- `EMBEDDING_ENDPOINT=<openai-compatible-base-url>`
- `EMBEDDING_MODEL=<embedding-model-name>`
- `EMBEDDING_DIMENSIONS=<embedding-vector-size>`
- single-user mode
- Postgres graph persistence
- pgvector vector persistence

Example OpenAI official values:

- `LLM_ENDPOINT=https://api.openai.com/v1`
- `LLM_MODEL=gpt-4o-mini`
- `EMBEDDING_ENDPOINT=https://api.openai.com/v1`
- `EMBEDDING_MODEL=text-embedding-3-large`
- `EMBEDDING_DIMENSIONS=3072`

Example OpenRouter values:

- `LLM_ENDPOINT=https://openrouter.ai/api/v1`
- `LLM_MODEL=openrouter/openai/gpt-4o-mini`
- `EMBEDDING_ENDPOINT=https://openrouter.ai/api/v1`
- `EMBEDDING_MODEL=openrouter/google/gemini-embedding-2-preview`
- `EMBEDDING_DIMENSIONS=3072`

## 4. Configure `cognee-mcp`

In Railway:

1. Create a new service named `cognee-mcp`
2. Connect it to this GitHub repository
3. In `Build`, select `Dockerfile`
4. In `Config-as-code`, set the Railway config file to:

   `railway.mcp.toml`

5. In `Source`, leave root directory empty

The `Dockerfile.mcp` wrapper ensures the MCP service:

- honors Railway `PORT`
- runs in API/SSE mode
- can be exposed publicly at `/sse`

### Required variables for `cognee-mcp`

Set these variables on the `cognee-mcp` service:

- `API_URL=http://cognee-api.railway.internal:8080`
- `TRANSPORT_MODE=sse`
- `MCP_ALLOWED_HOSTS=<your-public-mcp-domain>,<your-public-mcp-domain>:*`

You can also reuse the same OpenAI-compatible model and database variables as the backend, if you want the MCP service to execute backend-facing operations consistently.

## 5. Generate the public MCP domain

After `cognee-mcp` is created:

1. Open the `cognee-mcp` service
2. Go to the domain section
3. Generate a Railway domain
4. Copy the domain value
5. Use that exact hostname in `MCP_ALLOWED_HOSTS`

Example:

- public domain: `cognee-mcp-production-9beb.up.railway.app`
- `MCP_ALLOWED_HOSTS=cognee-mcp-production-9beb.up.railway.app,cognee-mcp-production-9beb.up.railway.app:*`

## 6. Verify the deployment

### Backend API

- `https://<cognee-api-domain>/health` should return `200`

### MCP service

- `https://<cognee-mcp-domain>/health` should return `200`
- `https://<cognee-mcp-domain>/sse` should return `200`

Note:

- `/mcp` is not the correct endpoint for the production MCP service in this setup
- the correct public endpoint is `/sse`

## 7. Verify from OpenCode

Your OpenCode config should point to the MCP SSE endpoint:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "cognee": {
      "type": "remote",
      "url": "https://<cognee-mcp-domain>.up.railway.app/sse",
      "enabled": true,
      "oauth": false
    }
  }
}
```

Then verify:

- OpenCode shows `cognee` as connected
- a real Cognee MCP tool call succeeds
