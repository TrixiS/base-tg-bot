from abc import ABC, abstractmethod


class BaseService(ABC):
    @abstractmethod
    async def setup(self):
        return NotImplemented

    @abstractmethod
    async def dispose(self):
        return NotImplemented
