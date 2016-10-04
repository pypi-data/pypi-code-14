import sys
import asyncio

# sys.path.append('..')
from siridb.connector import async_server_info
from siridb.connector import SiriDBClient

async def get_info():
    result = await async_server_info()
    print(result)

async def do_query(siri):
    await siri.connect()
    result = await siri.query('select * from "series float"')
    print(result)
    siri.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_info())

    siri = SiriDBClient(
        username='iris',
        password='siri',
        dbname='dbtest',
        hostlist=[
            ('127.0.0.1', 9000, {'backup': False}),
            # ('127.0.0.1', 9001, {'backup': False}),
            # ('127.0.0.1', 9002, {'backup': False}),
            # ('127.0.0.1', 9003, {'backup': False}),
            # ('127.0.0.1', 9004, {'backup': False}),
            # ('127.0.0.1', 9005, {'backup': False}),
    ])

    loop.run_until_complete(do_query(siri))
