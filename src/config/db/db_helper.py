from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base
from .db_config import settings

DB_URL = f'postgresql+asyncpg://{settings.PG_USER}:{settings.PG_PASSWORD}@{settings.PG_HOST}:{settings.PG_PORT}/{settings.PG_DB}'

async_engine = create_async_engine(DB_URL, echo=True)
async_session = sessionmaker(
	bind=async_engine,
	class_=AsyncSession
)

class Base(DeclarativeBase):
    pass


async def get_session():
    async with async_session() as session:
        yield session
