import asyncio

from concurrently import concurrently


async def amain(loop):
    data = 1, 2, 3
    i_data = iter(data)

    @concurrently(3)
    async def _parallel():
        for i in i_data:
            print(i)
            if i == 2:
                assert False
            await asyncio.sleep(3)
            print('awake', i)

    await _parallel()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(amain(loop))
