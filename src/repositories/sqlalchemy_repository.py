from sqlalchemy import select, delete, update
from .base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession

class SqlAlchemyRepository(BaseRepository):
    
    def __init__(self, session: AsyncSession, model):
        self.session = session
        self.model = model

    async def create(self, obj):
        async with self.session() as session:
            if not isinstance(obj, dict):
                obj = obj.dict()
            stmt = self.model(**obj)
            session.add(stmt)
            await session.commit()
            await session.refresh(stmt)
            return stmt
    
    async def get_one(self, filter):
        async with self.session() as session:
            if not isinstance(filter, dict):
                filter = filter.dict()
            stmt = select(self.model).filter_by(**{k: v for k, v in filter.items() if v is not None})
            result = await session.execute(stmt)
            return result.scalars().all()
        
    async def get_all(self):
        async with self.session() as session:
            stmt = select(self.model)
            result = await session.execute(stmt)
            return result.scalars().all()
    
    async def update(self, obj, filter):
        async with self.session() as session:
            if not isinstance(obj, dict):
                obj = obj.dict()
            if not isinstance(filter, dict):
                filter = filter.dict()
            stmt = update(self.model).values(
                **{k: v for k, v in obj.items() if v is not None}
                ).filter_by(
                    **{k: v for k, v in filter.items() if v is not None}
                )
            result = await session.execute(stmt)    
            await session.commit()
            return stmt
    
    async def delete(self, filter):
        async with self.session() as session:
            if not isinstance(filter, dict):
                filter = filter.dict()
            stmt = delete(self.model).where(
                *[getattr(self.model, key) == value for key, value in filter.items() if value is not None]
            )
            await session.execute(stmt)
            await session.commit()
            return {"message": "Deleted successfully"}  # ✅ ПОВЕРТАЄМО JSON
