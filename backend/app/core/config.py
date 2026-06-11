from functools import lru_cache
from typing import Literal

from pydantic import AnyHttpUrl, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    environment: Literal["development", "test", "production"] = "development"
    app_name: str = "Job Application Tracker"
    api_prefix: str = "/api"
    frontend_url: str = "http://localhost:5173"

    database_url: str = "sqlite+aiosqlite:///./job_tracker.db"
    test_database_url: str = "sqlite+aiosqlite:///:memory:"

    jwt_secret_key: str = Field(default="change-me-in-production-use-env", min_length=24)
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    email_verification_expire_minutes: int = 60
    reset_otp_expire_minutes: int = 10

    upstash_redis_url: str | None = None
    upstash_redis_token: str | None = None
    redis_url: str | None = None

    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_user: str | None = None
    smtp_password: str | None = None
    smtp_from_email: str = "noreply@example.com"
    smtp_from_name: str = "Job Tracker"

    supabase_url: AnyHttpUrl | None = None
    supabase_service_role_key: str | None = None
    supabase_storage_bucket: str = "resumes"

    login_rate_limit: str = "5/minute"
    login_lockout_failures: int = 5
    login_lockout_minutes: int = 15

    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    @field_validator("jwt_secret_key")
    @classmethod
    def validate_secret(cls, value: str) -> str:
        """Reject the development secret in production."""
        if value == "change-me-in-production-use-env":
            return value
        if len(value) < 24:
            raise ValueError("JWT_SECRET_KEY must be at least 24 characters")
        return value

    def validate_for_startup(self) -> None:
        """Crash early for missing production configuration."""
        if self.environment != "production":
            return

        missing: list[str] = []
        if self.jwt_secret_key == "change-me-in-production-use-env":
            missing.append("JWT_SECRET_KEY")
        if not self.database_url:
            missing.append("DATABASE_URL")
        if missing:
            joined = ", ".join(missing)
            raise RuntimeError(f"Missing required production environment variables: {joined}")


@lru_cache
def get_settings() -> Settings:
    """Return cached settings."""
    return Settings()


settings = get_settings()

