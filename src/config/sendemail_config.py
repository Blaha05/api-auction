import smtplib
from dotenv import load_dotenv
import os

email = os.getenv('EMAIL')
password = os.getenv('TOKEN_EMAIL')

class EmailConfig:
    email = os.getenv('EMAIL')
    password = os.getenv('TOKEN_EMAIL')


def get_email_config():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    return server
