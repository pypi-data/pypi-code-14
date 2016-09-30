from .stream import Stream


class StreamFromIterator(Stream):

    OUT = ['item']

    def __init__(self, iterator):
        super().__init__()
        self.iterator = iterator

    async def run(self, ins, outs):
        for item in self.iterator:
            await outs.item.push(item)
        outs.item.close()
