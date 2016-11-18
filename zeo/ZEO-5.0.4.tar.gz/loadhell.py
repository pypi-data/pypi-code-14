# Measure load performance at the network level by beating the crap
# out of a ZEO server.

import logging
import time
import multiprocessing
import sys

from ZODB.utils import maxtid, z64

import ZEO.tests.testssl

logger = logging.getLogger(__name__)

#logging.basicConfig(level='DEBUG')

def fworker(client_storage, queue, nloads):
    expect = client_storage.loadBefore(z64, maxtid)
    callf = client_storage._server.callf
    start = time.time()
    futures = [callf('loadBefore', z64, maxtid) for i in range(nloads)]
    for future in futures:
        assert future.result(999) == expect
    queue.put(int((time.time()-start) * 1000000 / nloads))

def worker(client_storage, queue, nloads):
    expect = client_storage.loadBefore(z64, maxtid)
    call = client_storage._server.call
    start = time.time()
    for i in range(nloads):
        assert call('loadBefore', z64, maxtid) == expect
    queue.put(int((time.time()-start) * 1000000 / nloads))

def worker_process(addr, queue, nloads, ssl):
    try:
        if ssl:
            ssl = ZEO.tests.testssl.client_ssl()
        client = ZEO.client(addr, ssl=ssl)
        worker(client, queue, nloads)
    except:
        logger.exception('worker process')
        raise

def main():
    nprocs, nloads, ssl = map(int, sys.argv[1:])
    if ssl:
        zeo_conf = ZEO.tests.testssl.server_config
    else:
        ssl = None
        zeo_conf = None

    addr, stop = ZEO.server(threaded=False, path='t.fs', zeo_conf=zeo_conf)
    try:
        db = ZEO.DB(addr, ssl=ZEO.tests.testssl.client_ssl() if ssl else None)
        with db.transaction() as conn:
            conn.root.x = 'x'*999
        queue = multiprocessing.Queue()
        processes = [
            multiprocessing.Process(target=worker_process,
                                    args=(addr, queue, nloads, ssl),
                                    daemon=True)
            for i in range(nprocs)
            ]
        for process in processes:
            process.start()
        for process in processes:
            process.join(999)
            assert not process.is_alive()
        times = sorted(queue.get() for process in processes)
        print(times[0],
              times[len(times)*1//4],
              times[len(times)*2//4],
              times[len(times)*3//4],
              times[-1],
              sum(times)/len(times),
              )
    finally:
        stop()

if __name__ == '__main__':
    main()
