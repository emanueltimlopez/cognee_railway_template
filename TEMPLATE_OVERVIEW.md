# Deploy and Host Cognee AI Memory Platform with MCP on Railway

Cognee AI Memory Platform with MCP combines a private Cognee backend, durable Postgres + pgvector storage, and a public MCP service so AI tools can store, structure, and retrieve memory across sessions. This template is set up for a production-style Railway deployment with OpenAI-compatible model endpoints and an MCP SSE endpoint for client integrations.

## About Hosting Cognee AI Memory Platform with MCP

Hosting this template deploys three connected services: `cognee-api` as the private backend, `cognee-mcp` as the public MCP layer, and PostgreSQL as the shared relational, graph, and vector store. Railway handles service provisioning, networking, and runtime configuration, while the template wires the backend and MCP service together over internal networking. The result is a single-user-ready memory stack that supports ingestion, Cognify processing, search, and MCP-based tool access from clients like OpenCode. You only need to provide your OpenAI-compatible endpoint, model names, LLM credentials, and optionally a separate embedding key.

## Common Use Cases

- Give AI coding assistants persistent project memory across sessions through MCP
- Build a private knowledge graph and vector memory backend for internal AI workflows
- Store, structure, and retrieve context from documents, notes, and development artifacts

## Dependencies for Cognee AI Memory Platform with MCP Hosting

- An API key and base URL for an OpenAI-compatible LLM endpoint, such as OpenAI, OpenRouter, LiteLLM proxy, or vLLM
- PostgreSQL with pgvector support

### Deployment Dependencies

- Cognee docs: https://docs.cognee.ai/
- Cognee MCP quickstart: https://docs.cognee.ai/cognee-mcp/mcp-quickstart
- Railway template docs: https://docs.railway.com/templates/create
- OpenCode config schema: https://opencode.ai/config.json

### Implementation Details

The template deploys:
- `cognee-api` with Dockerfile-based build and `/health` healthcheck
- `cognee-mcp` in API/SSE mode, exposed publicly at `/sse`
- `postgres` as the shared persistence layer for relational, graph, and vector data

Example OpenCode MCP configuration:

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

## Why Deploy Cognee AI Memory Platform with MCP on Railway?

Railway is a singular platform to deploy your infrastructure stack. Railway will host your infrastructure so you don't have to deal with configuration, while allowing you to vertically and horizontally scale it.

By deploying Cognee AI Memory Platform with MCP on Railway, you are one step closer to supporting a complete full-stack application with minimal burden. Host your servers, databases, AI agents, and more on Railway.
