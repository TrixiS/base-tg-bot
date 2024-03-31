import asyncio
import functools
from dataclasses import dataclass
from typing import Any, Callable, Coroutine

from ..utils import dateutils
from ..utils.services import Service

_JobFunc = Callable[..., Coroutine[Any, Any, Any]]


@dataclass(frozen=True)
class _Job:
    func: _JobFunc
    args: tuple[Any, ...]
    kwargs: dict[str, Any]
    interval_seconds: float

    async def run(self):
        while True:
            await asyncio.sleep(self.interval_seconds)

            partial_func = functools.partial(
                self.func, *self.args, **self.kwargs, now=dateutils.utc_now()
            )

            asyncio.create_task(partial_func())


@dataclass
class _Schedule:
    job: _Job
    task: asyncio.Task | None = None


class ScheduleService(Service):
    def __init__(self):
        self._schedules: list[_Schedule] = []

    async def setup(self):
        for schedule in self._schedules:
            schedule.task = asyncio.create_task(schedule.job.run())

    async def dispose(self):
        for schedule in self._schedules:
            if schedule.task is not None:
                schedule.task.cancel()

    def schedule(self, func: _JobFunc, *args, interval_seconds: float, **kwargs):
        self._schedules.append(
            _Schedule(_Job(func, args, kwargs, interval_seconds=interval_seconds))
        )

        return self
