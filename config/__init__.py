"""Configuration package."""

from .agents import (
    AGENT_TYPES,
    DEFAULT_CONFIG,
    MODELS,
    PROVIDERS,
    AgentConfig,
    get_model_info,
    get_provider_display_name,
)
from .settings import (
    APP_DIR,
    APP_NAME,
    APP_SUBTITLE,
    APP_VERSION,
    AUTO_SAVE_INTERVAL,
    DB_PATH,
    DB_SCHEMA_VERSION,
    DEFAULT_SAFE_MODE,
    LOGS_DIR,
    MAX_CONVERSATION_HISTORY,
)

__all__ = [
    # Agent config
    "AgentConfig",
    "DEFAULT_CONFIG",
    "PROVIDERS",
    "MODELS",
    "AGENT_TYPES",
    "get_provider_display_name",
    "get_model_info",
    # Settings
    "APP_NAME",
    "APP_SUBTITLE",
    "APP_VERSION",
    "APP_DIR",
    "DB_PATH",
    "LOGS_DIR",
    "DEFAULT_SAFE_MODE",
    "MAX_CONVERSATION_HISTORY",
    "AUTO_SAVE_INTERVAL",
    "DB_SCHEMA_VERSION",
]
