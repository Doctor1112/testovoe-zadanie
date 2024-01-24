from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_DIR: Path
    REGISTRY: str
    DOMAIN: str
    DEBUG: bool = False

    BOT_TOKEN: str

    SERVICE_CHAT_ID: int

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str


settings = Settings()
