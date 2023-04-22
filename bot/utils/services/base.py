from typing import Protocol


class Service(Protocol):
    async def setup(self):
        ...

    async def dispose(self):
        ...
