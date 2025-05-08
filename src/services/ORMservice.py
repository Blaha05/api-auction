from repositories.sqlalchemy_repository import SqlAlchemyRepository

class ORMService:

    def __init__(self, session, model):
        self.service = SqlAlchemyRepository(session, model)

    async def create(self, obj):
        return await self.service.create(obj)
    
    async def get_one(self, filter):
        return await self.service.get_one(filter)
    
    async def get_all(self):
        return await self.service.get_all()
    
    async def update(self, obj, filter):
        return await self.service.update(obj, filter)
    
    async def delete(self, obj):
        return await self.service.delete(obj)
    

def service_factory(session, model):
    return ORMService(session, model)