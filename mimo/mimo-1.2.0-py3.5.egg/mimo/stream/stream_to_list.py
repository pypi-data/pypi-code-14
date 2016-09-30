from .stream import Stream


class StreamToList(Stream):

    IN = ['item']

    def __init__(self,):
        super().__init__()
        self.collection = []

    async def run(self, ins, outs):
        collection = self.collection
        async for item in ins.item:
            collection.append(item)
