"""Configuration for AI models and providers."""

from dataclasses import dataclass
from typing import List


@dataclass
class AgentConfig:
    """Configuration for an AI agent."""
    
    name: str
    provider: str
    model: str
    description: str
    enabled: bool = True


# Available AI Providers
PROVIDERS = {
    "github_copilot": "GitHub Copilot",
    "openai": "OpenAI",
    "anthropic": "Anthropic",
    "local": "Local Model",
}

# Available Models
MODELS = {
    "gpt-5.3-codex": {
        "name": "GPT-5.3-Codex",
        "provider": "github_copilot",
        "description": "Advanced code analysis model",
    },
    "gpt-4": {
        "name": "GPT-4",
        "provider": "openai",
        "description": "General purpose model",
    },
    "claude-3-opus": {
        "name": "Claude 3 Opus",
        "provider": "anthropic",
        "description": "Advanced reasoning model",
    },
}

# Agent Types
AGENT_TYPES = {
    "SYSTEM": {"name": "System", "description": "System messages and notifications"},
    "AGENT": {"name": "Agent", "description": "Main agent coordinator"},
    "TRACE": {"name": "Trace", "description": "Execution trace logs"},
    "DAST": {"name": "DAST", "description": "Dynamic Application Security Testing"},
    "SAST": {"name": "SAST", "description": "Static Application Security Testing"},
    "SECRETS": {"name": "Secrets", "description": "Secret scanning and detection"},
    "FUZZ": {"name": "Fuzzing", "description": "Fuzz testing agent"},
    "NET": {"name": "Network", "description": "Network security analysis"},
    "FIX": {"name": "Fix", "description": "Automated fix suggestions"},
    "REPORT": {"name": "Report", "description": "Report generation"},
}

# Default Configuration
DEFAULT_CONFIG = AgentConfig(
    name="Vulnix Default",
    provider="github_copilot",
    model="gpt-5.3-codex",
    description="Default vulnerability assessment agent",
    enabled=True,
)


def get_provider_display_name(provider_key: str) -> str:
    """Get display name for a provider."""
    return PROVIDERS.get(provider_key, provider_key)


def get_model_info(model_key: str) -> dict:
    """Get model information."""
    return MODELS.get(model_key, {
        "name": model_key,
        "provider": "unknown",
        "description": "Unknown model",
    })
