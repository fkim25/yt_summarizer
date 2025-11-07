"""
Configuration module for loading environment variables.
This ensures all files can access the .env file.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Get the project root directory (where this file is located)
PROJECT_ROOT = Path(__file__).parent

# Path to .env file
ENV_FILE = PROJECT_ROOT / '.env'

# Load environment variables from .env file
# This will not override existing environment variables
# Set override=True to allow .env to override system environment variables if needed
load_dotenv(dotenv_path=ENV_FILE, override=False)

# Verify .env file was loaded (for debugging)
if ENV_FILE.exists():
    _env_loaded = load_dotenv(dotenv_path=ENV_FILE, override=False)
else:
    _env_loaded = False


def get_env(key, default=None):
    """
    Get an environment variable.
    
    Args:
        key: Environment variable name
        default: Default value if not found
        
    Returns:
        Environment variable value or default
    """
    return os.getenv(key, default)


def ensure_env_loaded():
    """
    Ensure environment variables are loaded.
    This can be called from any module to guarantee .env is loaded.
    """
    load_dotenv(dotenv_path=ENV_FILE, override=False)

