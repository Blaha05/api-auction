from celery import Celery
from dotenv import load_dotenv
import os
import eventlet

load_dotenv()

redis_url = str(os.getenv('CELERY_BROKER_URL'))

celery_app = Celery("celery_worker", broker=redis_url, backend=redis_url)


celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    enable_utc=True,
    timezone='Europe/Moscow',
    broker_connection_retry_on_startup=True,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)

#celery_app.autodiscover_tasks(['tasks'])


