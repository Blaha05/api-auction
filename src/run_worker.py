from config.celery_config import celery_app

# Це потрібно лише для імпорту, щоб Celery знав про таски
import tasks.sendemail

# worker запускається з CLI:
# celery -A config.celery_config.celery_app worker --loglevel=info
