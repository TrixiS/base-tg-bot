from typing import Any, Optional

from aiogram import Dispatcher as AiogramDispatcher
from aiogram.fsm.storage.base import BaseEventIsolation, BaseStorage
from aiogram.fsm.strategy import FSMStrategy

from .service_manager import ServiceManager


class Dispatcher(AiogramDispatcher):
    def __init__(
        self,
        storage: Optional[BaseStorage] = None,
        fsm_strategy: FSMStrategy = ...,
        events_isolation: Optional[BaseEventIsolation] = None,
        disable_fsm: bool = False,
        **kwargs: Any
    ) -> None:
        super().__init__(storage, fsm_strategy, events_isolation, disable_fsm, **kwargs)
        self.services = ServiceManager()
