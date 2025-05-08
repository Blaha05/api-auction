import asyncio
import smtplib
from config.celery_config import celery_app
from config.sendemail_config import EmailConfig
import eventlet
from services.ORMservice import service_factory
from config.db.db_helper import async_session
from models.messege import Folow

eventlet.monkey_patch()

service_follow = service_factory(async_session, Folow)

config_email = EmailConfig()

@celery_app.task
def sendemail(massage, user):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(config_email.email, config_email.password)
    server.sendmail('viktorblaha2005@gmail.com',user, massage)
    server.quit()
    return 

# celery -A auctionCursova.src.tasks.sendemail worker -l info -P eventlet
# celery -A auctionCursova.src.tasks.sendemail beat --loglevel=info
# celery -A tasks.sendemail worker -l info -P eventlet
# celery -A config.celery_config worker -l info -P eventlet


@celery_app.task
def check_email(users, user_bit):

    if users:
        for user in users:
            sendemail.apply_async(args=[f"Now do bit {user_bit}", user])