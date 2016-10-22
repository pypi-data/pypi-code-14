import sys
import asyncio
import logging

logger = logging.getLogger()
logger.setLevel('DEBUG')

sys.path.append('..')
from siridb.connector import async_server_info
from siridb.connector import SiriDBClient

async def get_info():
    result = await async_server_info()
    print(result)

async def do_query(siri):
    await siri.connect(timeout=2)

    n = 120
    while n:
        try:
            result = await siri.query('select count(now) from "series float"')
        except Exception as e:
            print('Cannot run query:', e)
        else:
            print(result)
        finally:
            n -= 1
            await asyncio.sleep(1)

    siri.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(get_info())

    siri = SiriDBClient(
        username='iris',
        password='siri',
        dbname='dbtest',
        hostlist=[
            ('127.0.0.1', 9000, {'backup': False}),
            ('127.0.0.1', 9001, {'backup': False}),
            # ('127.0.0.1', 9002, {'backup': False}),
            # ('127.0.0.1', 9003, {'backup': False}),
            # ('127.0.0.1', 9004, {'backup': False}),
            # ('127.0.0.1', 9005, {'backup': False}),
    ])

    loop.run_until_complete(do_query(siri))
