from aiogram.dispatcher.event.handler import CallbackType
from aiogram.dispatcher.router import Router as AiogramRouter


class Router(AiogramRouter):
    def filter(self, *filters: CallbackType) -> None:
        for observer in self.observers.values():
            observer.filter(*filters)
