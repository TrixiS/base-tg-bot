from typing import Type

from aiogram.dispatcher.filters import BaseFilter
from aiogram.dispatcher.router import Router as AiogramRouter


class Router(AiogramRouter):
    def bind_filter(self, bound_filter: Type[BaseFilter]) -> None:
        for observer in self.observers.values():
            observer.bind_filter(bound_filter)
