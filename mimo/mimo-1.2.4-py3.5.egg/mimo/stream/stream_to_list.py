from .stream import Stream


class StreamToList(Stream):

    IN = ['item', 'size']
    OUT = ['items']

    async def run(self, ins, outs):
        async for size in ins.size:
            items = []
            while len(items) < size:
                items.append(await ins.item.pop())
            await outs.items.push(items)
        outs.items.close()
