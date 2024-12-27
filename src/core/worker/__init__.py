from celery import Celery

from src.core.config import settings

celery_app = Celery(
    "worker",
    backend=settings.REDIS_CACHE_URL,
    broker=settings.CELERY_BROKER_URL,
)

celery_app.conf.task_routes = {"worker.celery_worker.test_celery": "test-queue"}
celery_app.conf.update(task_track_started=True)
