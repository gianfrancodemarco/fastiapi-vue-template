from __future__ import annotations

from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "fastapi_vue_template",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.task_routes = {
    "app.infrastructure.messaging.tasks.*": {"queue": "default"}}
celery_app.conf.task_default_retry_delay = 5
celery_app.conf.task_default_queue = "default"


@celery_app.task(bind=True, ignore_result=False)
def heartbeat(self) -> str:  # type: ignore[override]
    return "alive"
