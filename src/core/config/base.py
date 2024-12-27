import os

from enum import Enum
from typing import ClassVar

from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from starlette.config import Config


current_file_dir = os.path.dirname(os.path.realpath(__file__))
env_path = os.path.join(current_file_dir, "..", "..", "..", ".env")
config = Config(env_path)


class BaseConfigSettings(BaseSettings):
    model_config: ClassVar[ConfigDict] = ConfigDict(case_sensitive=True)


class AppSettings(BaseConfigSettings):
    APP_NAME: str = config("APP_NAME", default="FastAPI app")
    APP_DESCRIPTION: str | None = config("APP_DESCRIPTION", default=None)
    APP_VERSION: str | None = config("APP_VERSION", default="0.0.1")
    LICENSE_NAME: str | None = config("LICENSE", default=None)
    CONTACT_NAME: str | None = config("CONTACT_NAME", default=None)
    CONTACT_EMAIL: str | None = config("CONTACT_EMAIL", default=None)


class CryptSettings(BaseConfigSettings):
    SECRET_KEY: str = config("SECRET_KEY")
    ALGORITHM: str = config("ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)
    REFRESH_TOKEN_EXPIRE_DAYS: int = config("REFRESH_TOKEN_EXPIRE_DAYS", default=7)


class EnvironmentOption(Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    LOCAL = "local"
    STAGING = "staging"
    TEST = "test"


class EnvironmentSettings(BaseConfigSettings):
    ENVIRONMENT: EnvironmentOption = config("ENVIRONMENT", default="local")
    DEFAULT_LOCALE: str = "en_US"
    DEBUG: int = 0
