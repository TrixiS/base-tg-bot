import asyncio
import sys
from typing import Any, Coroutine, TypeVar

import uvloop

_T = TypeVar("_T")


def run(coro: Coroutine[Any, Any, _T]) -> _T:
    if sys.version_info < (3, 11):
        uvloop.install()
        return asyncio.run(coro)

    with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
        return runner.run(coro)
