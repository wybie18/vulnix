"""Application settings and configuration."""

from pathlib import Path


# Application Paths
APP_DIR = Path.home() / ".vulnix"
DB_PATH = APP_DIR / "vulnix.db"
LOGS_DIR = APP_DIR / "logs"

# Ensure directories exist
APP_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Application Settings
APP_NAME = "VULNIX"
APP_SUBTITLE = "QA/VA Swarm"
APP_VERSION = "0.1.0"

# UI Settings
DEFAULT_SAFE_MODE = True
MAX_CONVERSATION_HISTORY = 1000
AUTO_SAVE_INTERVAL = 10  # seconds

# Database Settings
DB_SCHEMA_VERSION = 1
