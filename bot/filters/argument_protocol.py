from typing import Optional, Protocol

from aiogram import types


class BoundFilterArgumentProtocol(Protocol):
    from_user: Optional[types.User]
