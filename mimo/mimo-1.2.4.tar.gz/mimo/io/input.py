import asyncio


class InputClosed(Exception):
    pass


class Input(asyncio.Queue):
    def __init__(self, name, maxsize=0, loop=None, *, stream=None):
        super().__init__(maxsize, loop=loop)
        self.name = name
        self.stream = stream
        self._closed = False

    async def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return await self.pop()
        except InputClosed:
            raise StopAsyncIteration

    async def push(self, item):
        try:
            if self._closed:
                raise InputClosed
            return await self.put(item)
        except RuntimeError:
            raise RuntimeError('Event loop closed while waiting for push to {} input: {}'.format(self.stream, self.name))

    async def peek(self):
        while self.empty():
            if self.is_closed():
                raise InputClosed

            getter = self._loop.create_future()
            self._getters.append(getter)
            try:
                await getter
            except:
                getter.cancel()
                if not self.empty() and not getter.cancelled():
                    self._wakeup_next(self._getters)
                raise
        return self._queue[0]

    async def pop(self):
        try:
            while self.empty():
                if self._closed and len(self._putters) == 0:
                    raise InputClosed

                getter = self._loop.create_future()
                self._getters.append(getter)
                try:
                    await getter
                except:
                    getter.cancel()
                    if not self.empty() and not getter.cancelled():
                        self._wakeup_next(self._getters)
                    raise
            return self.get_nowait()
        except RuntimeError:
            raise RuntimeError('Event loop closed while waiting for pop from {} input: {}'.format(self.stream, self.name))

    def open(self):
        self._closed = False

    def close(self):
        self._closed = True
        self._maxsize = 0
        while self._putters:
            putter = self._putters.popleft()
            if not putter.done():
                putter.set_result(None)
        while self._getters:
            getter = self._getters.popleft()
            if not getter.done():
                if self.empty():
                    getter.set_exception(InputClosed)
                else:
                    getter.set_result(None)

    def is_closed(self):
        return self._closed and len(self._queue) == 0 and len(self._putters) == 0

    def is_open(self):
        return not self.is_closed()
