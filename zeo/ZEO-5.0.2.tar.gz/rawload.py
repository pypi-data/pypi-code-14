import argparse
import logging
import time

from ZODB.utils import z64, maxtid

import ZEO
from ZEO.asyncio.client import Promise

#logging.basicConfig(level=logging.DEBUG)

def main():
    a, s = ZEO.server()
    db = ZEO.DB(a)
    with db.transaction() as conn:
        conn.root.x = 'x'*999

    storage = db.storage
    expect = storage.loadBefore(z64, maxtid)
    repetitions = 1000
    protocol = storage._server.client.protocol
    n = [repetitions]

    def load_test(future):

        def load(result):
            if result != expect:
                raise AssertionError(result, expect)
            if n[0]:
                n[0] -= 1
                protocol.promise('loadBefore', z64, maxtid)(load)
            else:
                future.set_result(None)

        load(expect)

    start = time.time()
    storage._server._ClientRunner__call(load_test)
    print(round((time.time()-start)*1000000/repetitions))


if __name__ == '__main__':
    main()
