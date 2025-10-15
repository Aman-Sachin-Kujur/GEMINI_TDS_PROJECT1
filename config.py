# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from dotenv import load_dotenv
from typing import Optional
from pathlib import Path

# Load .env early so environment variables are available to Pydantic Settings.
project_root = Path(__file__).resolve().parent
load_dotenv(dotenv_path=project_root / '.env')


# Define the structure for all required secrets/config
class Settings(BaseSettings):
    # API Keys/Tokens — optional at construction time; validated explicitly.
    GEMINI_API_KEY: Optional[str] = None
    GITHUB_TOKEN: Optional[str] = None

    # Project-specific variables
    STUDENT_SECRET: Optional[str] = None
    GITHUB_USERNAME: Optional[str] = None

    # Define which file to load settings from (keeps behavior explicit)
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    def validate_required(self) -> None:
        """Perform explicit validation and raise a clear error if any required
        environment variable is missing or empty.
        """
        missing = []
        for name in ("GEMINI_API_KEY", "GITHUB_TOKEN", "STUDENT_SECRET", "GITHUB_USERNAME"):
            val = getattr(self, name, None)
            if val is None or (isinstance(val, str) and val.strip() == ""):
                missing.append(name)

        if missing:
            raise RuntimeError(
                "Missing required environment variables: " + ", ".join(missing) +
                ".\nPlease create a .env file (see .env.example) or set these in your environment."
            )


# Use lru_cache to load the settings only once, improving performance
@lru_cache()
def get_settings():
    """Returns the cached settings object and validates required vars."""
    settings = Settings()
    settings.validate_required()
    return settings