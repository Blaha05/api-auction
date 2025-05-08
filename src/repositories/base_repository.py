from abc import ABC, abstractmethod


class BaseRepository(ABC):
    
    @abstractmethod
    async def create(self, obj):
        pass

    @abstractmethod
    async def get_one(self, id):
        pass

    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def update(self, obj):
        pass

    @abstractmethod
    async def delete(self, obj):
        pass

    