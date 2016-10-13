import asyncio


class AsynchronousZip:
    def __init__(self, *iterables):
        self._iterables = iterables

    def __aiter__(self):
        return self

    async def __anext__(self):
        result = await asyncio.gather(*[iterator.__anext__() for iterator in self._iterables])
        return tuple(result)
