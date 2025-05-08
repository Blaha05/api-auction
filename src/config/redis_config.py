import redis
from dotenv import load_dotenv 
import os


r = redis.Redis(
    host=os.getenv('REDIS_HOST'),  
    port=os.getenv('REDIS_PORT'),
    password=os.getenv('REDIS_PASSWORD'),  
    decode_responses=True  
)

try:
    response = r.ping()
    if response:
        print("Подключение к Redis успешно!")
    else:
        print("Не удалось подключиться к Redis.")
except Exception as e:
    print(f"Произошла ошибка: {e}")