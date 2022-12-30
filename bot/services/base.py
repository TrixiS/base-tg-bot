from abc import ABC


class Service(ABC):
    async def setup(self):
        ...

    async def dispose(self):
        ...
