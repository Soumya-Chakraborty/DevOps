"""Application configuration settings."""
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Application
    app_name: str = Field(default="monitoring-system", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=False, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    # Database
    database_url: str = Field(env="DATABASE_URL")
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")

    # Monitoring
    collection_interval: int = Field(default=30, env="COLLECTION_INTERVAL")
    alert_threshold_cpu: float = Field(default=80.0, env="ALERT_THRESHOLD_CPU")
    alert_threshold_memory: float = Field(default=85.0, env="ALERT_THRESHOLD_MEMORY")
    alert_threshold_disk: float = Field(default=90.0, env="ALERT_THRESHOLD_DISK")

    # API
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
