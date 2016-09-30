from .stream import Stream


class StreamFromInput(Stream):

    OUT = ['item']

    def __init__(self, input):
        super().__init__()
        self.input = input

    async def run(self, ins, outs):
        async for item in self.input:
            await outs.item.push(item)
        outs.item.close()
