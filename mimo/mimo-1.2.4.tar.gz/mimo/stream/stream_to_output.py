from .stream import Stream


class StreamToOutput(Stream):

    IN = ['item']

    def __init__(self, output):
        super().__init__()
        self.output = output

    async def run(self, ins, out):
        async for item in ins.item:
            await self.output.push(item)
        ins.item.close()
