import asyncio
from concurrent.futures import ProcessPoolExecutor
from functools import lru_cache
from typing import Callable, List

from . import AbstractEngine, AbstractWaiter, UnhandledExceptions


class AsyncIOWaiter(AbstractWaiter):

    def __init__(self, fs: List[asyncio.Future], loop: asyncio.BaseEventLoop):
        self.fs = fs
        self.loop = loop

    async def __call__(self, *, suppress_exceptions=False):
        await asyncio.wait(self.fs, loop=self.loop)

        if not suppress_exceptions and self.exceptions():
            raise UnhandledExceptions(self.exceptions())

    async def stop(self):
        for f in self.fs:
            f.cancel()
        await self(suppress_exceptions=True)

    @lru_cache()
    def exceptions(self) -> List[Exception]:
        exc_list = []
        for f in self.fs:
            if f.cancelled():
                continue

            exc = f.exception()
            if exc:
                exc_list.append(exc)

        return exc_list


class AsyncIOEngine(AbstractEngine):

    def __init__(self, *, loop: asyncio.BaseEventLoop=None):
        super().__init__()
        self.loop = loop or asyncio.get_event_loop()

    def create_task(self, fn: asyncio.coroutine) -> asyncio.Future:
        return self.loop.create_task(fn())

    def waiter_factory(self, fs: List[asyncio.Future]):
        return AsyncIOWaiter(fs=fs, loop=self.loop)


class AsyncIOExecutorEngine(AsyncIOEngine):

    def __init__(self, *, loop=None, executor=None):
        assert not isinstance(executor, ProcessPoolExecutor), \
            'ProcessPoolExecutor is not supported'

        super().__init__(loop=loop)
        self.pool = executor

    def create_task(self, fn: Callable[[], None]) -> asyncio.Future:
        return self.loop.run_in_executor(self.pool, fn)
