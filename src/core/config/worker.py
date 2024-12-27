from src.core.config.base import BaseConfigSettings, config


DEFAULT_HOST = "localhost"
DEFAULT_PORT = 6379


class CelerySettings(BaseConfigSettings):
    CELERY_BROKER_USER: str = config("CELERY_BROKER_USER", default="rabbit")
    CELERY_BROKER_PASSWORD: str = config("CELERY_BROKER_PASSWORD", default="password")
    CELERY_BROKER_HOST: str = config("CELERY_BROKER_HOST", default=DEFAULT_HOST)
    CELERY_BROKER_PORT: int = config("CELERY_BROKER_PORT", default=5672)
    CELERY_BROKER_URL: str = (
        f"amqp://{CELERY_BROKER_USER}:{CELERY_BROKER_PASSWORD}"
        f"@{CELERY_BROKER_HOST}:{CELERY_BROKER_PORT}/"
    )


class ClientSideCacheSettings(BaseConfigSettings):
    CLIENT_CACHE_MAX_AGE: int = config("CLIENT_CACHE_MAX_AGE", default=60)


class RedisCacheSettings(BaseConfigSettings):
    REDIS_CACHE_HOST: str = config("REDIS_CACHE_HOST", default=DEFAULT_HOST)
    REDIS_CACHE_PORT: int = config("REDIS_CACHE_PORT", default=DEFAULT_PORT)
    REDIS_CACHE_PATH: int = config("REDIS_CACHE_PATH", default=7)
    REDIS_CACHE_URL: str = f"redis://{REDIS_CACHE_HOST}:{REDIS_CACHE_PORT}/{REDIS_CACHE_PATH}"
    CELERY_BACKEND_PATH: int = config("CELERY_BACKEND_PATH", default=0)
    CELERY_BACKEND_URL: str = f"redis://{REDIS_CACHE_HOST}:{REDIS_CACHE_PORT}/{CELERY_BACKEND_PATH}"


class RedisQueueSettings(BaseConfigSettings):
    REDIS_QUEUE_HOST: str = config("REDIS_QUEUE_HOST", default=DEFAULT_HOST)
    REDIS_QUEUE_PORT: int = config("REDIS_QUEUE_PORT", default=DEFAULT_PORT)


class RedisRateLimiterSettings(BaseConfigSettings):
    REDIS_RATE_LIMIT_HOST: str = config("REDIS_RATE_LIMIT_HOST", default=DEFAULT_HOST)
    REDIS_RATE_LIMIT_PORT: int = config("REDIS_RATE_LIMIT_PORT", default=DEFAULT_PORT)
    REDIS_RATE_LIMIT_URL: str = f"redis://{REDIS_RATE_LIMIT_HOST}:{REDIS_RATE_LIMIT_PORT}/"
