from asyncio import sleep
from fastapi import FastAPI
from router import router
import redis.asyncio as redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from config.redis_config import r as redis_
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.on_event("startup")
async def startup():
    FastAPICache.init(RedisBackend(redis_), prefix="fastapi-cache")

@app.get("/ttt")
@cache(expire=60)
async def root():
    await sleep(5)  # Simulate a delay
    return {"message": "Hello World"}

app.include_router(router)

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)