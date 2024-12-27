from enum import Enum

from src.core.config.base import BaseConfigSettings, config


class DBOption(Enum):
    MYSQL = "mysql"
    POSTGRES = "postgres"
    SQLITE = "sqlite"


class DatabaseSettings(BaseConfigSettings):
    DB_ENGINE: DBOption = config("DB_ENGINE", default=DBOption.SQLITE)


class SQLiteSettings(DatabaseSettings):
    SQLITE_URL: str = "sqlite+aiosqlite:///./db.sqlite"
    SQLITE_TEST_URL: str = "sqlite+aiosqlite:///./test.sqlite"

    @property
    def DATABASE_URL(self):
        return self.SQLITE_URL

    @property
    def TEST_URL(self):
        return self.SQLITE_TEST_URL


class PostgresSettings(DatabaseSettings):
    POSTGRES_USER: str = config("POSTGRES_USER", default="postgres")
    POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", default="postgres")
    POSTGRES_SERVER: str = config("POSTGRES_SERVER", default="localhost")
    POSTGRES_PORT: int = config("POSTGRES_PORT", default=5432)
    POSTGRES_DB: str = config("POSTGRES_DB", default="postgres")
    POSTGRES_URL: str = (
        f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    POSTGRES_TEST_URL: str = "postgresql+asyncpg://postgres:password123@127.0.0.1:5431/db-test"

    @property
    def DATABASE_URL(self):
        return self.POSTGRES_URL

    @property
    def TEST_URL(self):
        return self.POSTGRES_TEST_URL


class MySQLSettings(DatabaseSettings):
    MYSQL_USER: str = config("MYSQL_USER", default="mysql")
    MYSQL_PASSWORD: str = config("MYSQL_PASSWORD", default="mysql")
    MYSQL_SERVER: str = config("MYSQL_SERVER", default="localhost")
    MYSQL_PORT: int = config("MYSQL_PORT", default=3306)
    MYSQL_DB: str = config("MYSQL_DB", default="mysql")
    MYSQL_URL: str = (
        f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DB}"
    )
    MYSQL_TEST_URL: str = "mysql+aiomysql://mysql:password123@127.0.0.1:3307/db-test"

    @property
    def DATABASE_URL(self):
        return self.MYSQL_URL

    @property
    def TEST_URL(self):
        return self.MYSQL_TEST_URL
