from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings with environment variable support"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # ============ APPLICATION SETTINGS ============
    PROJECT_NAME: str = "Template Project"
    VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=True)

    class Config:
        env_file = ".env"
        case_sensitive = True


def get_settings() -> Settings:
    return Settings()


# Export the configured settings
settings = get_settings()
