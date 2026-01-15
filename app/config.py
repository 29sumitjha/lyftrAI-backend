# from pydantic import BaseModel, Field
# import os


# class Settings(BaseModel):
#     database_url: str = Field(..., alias="DATABASE_URL")
#     webhook_secret: str = Field(..., alias="WEBHOOK_SECRET")
#     log_level: str = Field("INFO", alias="LOG_LEVEL")


# def get_settings() -> Settings:
#     return Settings.model_validate(
#         {
#             "DATABASE_URL": os.getenv("DATABASE_URL"),
#             "WEBHOOK_SECRET": os.getenv("WEBHOOK_SECRET"),
#             "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
#         }
#     )

from pydantic import BaseModel, Field
from functools import lru_cache
import os


class Settings(BaseModel):
    # Defaults are provided so tests work without env vars
    database_url: str = Field(
        default="sqlite+aiosqlite:///./test.db", alias="DATABASE_URL"
    )
    webhook_secret: str = Field(
        default="testsecret", alias="WEBHOOK_SECRET"
    )
    log_level: str = Field(
        default="INFO", alias="LOG_LEVEL"
    )


@lru_cache
def get_settings() -> Settings:
    """
    Load settings once, preferring environment variables,
    but falling back to safe defaults for local testing.
    """
    return Settings.model_validate(
        {
            "DATABASE_URL": os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db"),
            "WEBHOOK_SECRET": os.getenv("WEBHOOK_SECRET", "testsecret"),
            "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
        }
    )


# single shared settings instance
settings = get_settings()
