from typing import Any, Awaitable, Callable, Dict, Protocol

from aiogram import BaseMiddleware, types


def _gen_snake_case(string: str):
    for i, c in enumerate(string):
        if c.islower():
            yield c
            continue

        if i != 0:
            yield "_"

        yield c.lower()


def _to_snake_case(string: str) -> str:
    return "".join(_gen_snake_case(string))


class Service(Protocol):
    async def setup(self) -> Any: ...
    async def dispose(self) -> Any: ...


class ServiceManager:
    def __init__(self):
        self._services: dict[str, Service] = {}

    def _register(self, service: Service):
        service_class_snake_name = _to_snake_case(service.__class__.__name__)
        self._services[service_class_snake_name] = service
        return self

    def register(self, *services: Service):
        for service in services:
            self._register(service)

        return self

    def unregister(self, service: Service):
        service_class_snake_name = _to_snake_case(service.__class__.__name__)
        del self._services[service_class_snake_name]

    async def setup_all(self):
        for service in self._services.values():
            await service.setup()

    async def dispose_all(self):
        for service in reversed(self._services.values()):
            await service.dispose()


class ServiceMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.manager = ServiceManager()

    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data.update(self.manager._services)
        return await handler(event, data)
