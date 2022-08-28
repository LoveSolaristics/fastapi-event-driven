from os import environ

from pydantic import BaseSettings


class DefaultSettings(BaseSettings):
    """
    Default configs for application.

    Usually, we have three environments: for development, testing and production.
    But in this situation, we only have standard settings for local development.
    """

    ENV: str = environ.get("ENV", "local")
    APP_HOST: str = environ.get("APP_HOST", "http://127.0.0.1")
    APP_PORT: int = int(environ.get("APP_PORT", 8080))

    REDIS_PORT: int = int(environ.get("REDIS_PORT", 6379))
    REDIS_PASSWORD: str | None = environ.get("REDIS_PASSWORD", None)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
