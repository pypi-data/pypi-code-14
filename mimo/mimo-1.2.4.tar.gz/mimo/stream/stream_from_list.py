from .stream import Stream


class StreamFromList(Stream):

    IN = ['items']
    OUT = ['item', 'size']

    async def run(self, ins, outs):
        async for items in ins.items:
            await outs.size.push(len(items))
            for item in items:
                await outs.item.push(item)
        outs.size.close()
        outs.item.close()
