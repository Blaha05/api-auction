from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import PostgresDsn
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PG_USER:str = os.getenv("PG_USER")
    PG_PASSWORD:str = os.getenv("PG_PASSWORD")
    PG_HOST:str = os.getenv("PG_HOST")
    PG_PORT:str = os.getenv("PG_PORT")
    PG_DB:str = os.getenv("PG_DB")

    @property
    def database_url(self) -> Optional[PostgresDsn]:
        return (
            f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}@"
            f"{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"
        )

settings = Settings()

