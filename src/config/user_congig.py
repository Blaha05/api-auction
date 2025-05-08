from services.ORMservice import ORMService
from services.hashservice import HashedPassword
from services.tokenservice import Token
import os
from dotenv import load_dotenv

load_dotenv()


token = Token(
    key = os.getenv('SECRET_KEY'),
    time = int(os.getenv('ACCESS_KEY_MiNUTES')),
    algorithm = os.getenv('ALGORITHM')
)

hashed_password = HashedPassword()

def services_users():
    return {
        'token': token,
        'hashed_password': hashed_password, 
    }