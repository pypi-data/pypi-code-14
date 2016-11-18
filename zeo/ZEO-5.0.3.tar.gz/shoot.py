import logging
import ZEO
from zodbshootout.speedtest import SpeedTest

fmt = ('add %d, update %d, warm %d, cold %d, hot %d, steamin %d'
       ' (microseconds)')

#logging.basicConfig(level=logging.ERROR)

addr, stop = ZEO.server()

speedtest = SpeedTest(concurrency=1, objects_per_txn=3, object_size=555)
for i in range(3):
    times = speedtest.run((lambda : ZEO.DB(addr)), 'zeo', i)
    print(fmt % tuple(round(t*1000000) for t in times), file=sys.stderr)
