import json
from pathlib import Path


def load_template() -> dict:
    template_path = Path(__file__).resolve().parents[1] / "railway-template.json"
    return json.loads(template_path.read_text())


def test_railway_template_includes_cognee_mcp_service() -> None:
    template = load_template()

    services = {service["name"]: service for service in template["services"]}

    assert "cognee-mcp" in services
    assert "cognee-api" in services


def test_cognee_mcp_service_targets_api_mode() -> None:
    template = load_template()

    services = {service["name"]: service for service in template["services"]}
    mcp_service = services["cognee-mcp"]

    assert mcp_service["build"]["dockerfilePath"] == "Dockerfile.mcp"
    assert mcp_service["deploy"]["healthcheckPath"] == "/health"
    assert mcp_service["variables"]["TRANSPORT_MODE"]["value"] == "sse"
    assert (
        mcp_service["variables"]["API_URL"]["value"]
        == "http://${{cognee-api.RAILWAY_PRIVATE_DOMAIN}}:8080"
    )
    assert (
        mcp_service["variables"]["MCP_ALLOWED_HOSTS"]["value"]
        == "${{cognee-mcp.RAILWAY_PUBLIC_DOMAIN}},${{cognee-mcp.RAILWAY_PUBLIC_DOMAIN}}:*"
    )


def test_cognee_api_uses_openai_compatible_provider_contract() -> None:
    template = load_template()

    services = {service["name"]: service for service in template["services"]}
    api_variables = services["cognee-api"]["variables"]

    required_model_variables = {
        "LLM_ENDPOINT",
        "LLM_MODEL",
        "LLM_API_KEY",
        "EMBEDDING_ENDPOINT",
        "EMBEDDING_MODEL",
        "EMBEDDING_DIMENSIONS",
    }

    assert required_model_variables.issubset(api_variables)
    assert api_variables["LLM_PROVIDER"]["value"] == "custom"
    assert api_variables["EMBEDDING_PROVIDER"]["value"] == "litellm"


def test_cognee_api_template_does_not_force_openrouter_defaults() -> None:
    template = load_template()

    services = {service["name"]: service for service in template["services"]}
    api_variables = services["cognee-api"]["variables"]

    configurable_values = {
        api_variables["LLM_ENDPOINT"]["value"],
        api_variables["LLM_MODEL"]["value"],
        api_variables["EMBEDDING_ENDPOINT"]["value"],
        api_variables["EMBEDDING_MODEL"]["value"],
    }
    descriptions = " ".join(
        variable["description"] for variable in api_variables.values() if "description" in variable
    )

    assert "https://openrouter.ai/api/v1" not in configurable_values
    assert not any(value.startswith("openrouter/") for value in configurable_values)
    assert "OpenRouter" not in descriptions
