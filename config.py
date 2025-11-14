"""Configuration module for loading environment variables."""
import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent
ENV_FILE = PROJECT_ROOT / '.env'
load_dotenv(dotenv_path=ENV_FILE, override=False)

def get_openai_api_key():
    """Get OpenAI API key from environment."""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        # Try to read from .env file directly
        try:
            env_file = PROJECT_ROOT / '.env'
            if env_file.exists():
                with open(env_file, 'r') as f:
                    for line in f:
                        if line.startswith('OPENAI_API_KEY='):
                            api_key = line.split('=', 1)[1].strip()
                            break
        except:
            pass
    return api_key

