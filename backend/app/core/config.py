from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "PlanPilot API"
    ENV: str = "dev"

    DATABASE_URL: str = Field(default="sqlite+aiosqlite:///./planpilot.db")

    # Comma-separated origins, e.g. "http://localhost:5173"
    CORS_ORIGINS: str = Field(default="http://localhost:5173")

    OPENAI_API_KEY: str = Field(default="")
    OPENAI_MODEL: str = Field(default="gpt-4o-mini")  # good default for MVP
    OPENAI_TIMEOUT_SECONDS: int = Field(default=30)

    AI_MAX_PHASES: int = Field(default=8)
    AI_MAX_TASKS_PER_PHASE: int = Field(default=10)


settings = Settings()
