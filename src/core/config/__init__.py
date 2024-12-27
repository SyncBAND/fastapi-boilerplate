from src.core.config.base import AppSettings, CryptSettings, EnvironmentSettings, config
from src.core.config.database import (
    DBOption, DatabaseSettings, MySQLSettings, PostgresSettings, SQLiteSettings
)
from src.core.config.worker import (
    CelerySettings,
    ClientSideCacheSettings,
    RedisCacheSettings,
    RedisQueueSettings,
    RedisRateLimiterSettings
)


# Determine the correct database settings dynamically
def get_database_settings() -> DatabaseSettings:
    db_engine = DatabaseSettings().DB_ENGINE
    if db_engine == DBOption.SQLITE:
        return SQLiteSettings
    if db_engine == DBOption.MYSQL:
        return MySQLSettings
    return PostgresSettings


class Settings(
    AppSettings,
    CelerySettings,
    CryptSettings,
    ClientSideCacheSettings,
    EnvironmentSettings,
    RedisCacheSettings,
    RedisQueueSettings,
    RedisRateLimiterSettings,
    get_database_settings()
):
    ...


settings = Settings()
