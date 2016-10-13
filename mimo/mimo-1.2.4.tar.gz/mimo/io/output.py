import asyncio


class Output:
    def __init__(self, name, *, stream=None):
        self.name = name
        self.stream = stream
        self._connections = []

    async def push(self, item):
        try:
            await asyncio.gather(*[connection.push(item) for connection in self._connections])
        except RuntimeError:
            raise RuntimeError('Event loop closed while waiting for push to {} output: {}'.format(self.stream, self.name))

    def pipe(self, connection):
        self._connections.append(connection)

    def close(self):
        for connection in self._connections:
            connection.close()
