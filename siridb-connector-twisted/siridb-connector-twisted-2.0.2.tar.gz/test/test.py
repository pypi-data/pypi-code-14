import sys
from twisted.python import log
from twisted.internet import defer
from twisted.internet import task
from twisted.internet import reactor
import time
import random
import logging

log.startLogging(sys.stdout)
logger = logging.getLogger()
logger.setLevel('INFO')

sys.path.append('..')
from siridb.twisted import SiriDBClientTwisted
from siridb.twisted.lib.exceptions import InsertError
from siridb.twisted.lib.exceptions import PoolError
from twisted.internet import task
from twisted.internet import reactor


@defer.inlineCallbacks
def test(_connection, n):
    data = {'series float': [
        [int(time.time()), random.random() * 10]
    ]}
    try:
        result = yield siri.insert(data)
    except InsertError as e:
        print('Insert error: {}'.format(e))
    except PoolError as e:
        print('Pool error: {}'.format(e))
    except Exception as e:
        print('Other exception: {}'.format(e))
    else:
        print(result)

    try:
        result = yield siri.query('select * from "series float"')
    except PoolError as e:
        print('Pool error: {}'.format(e))
    except Exception as e:
        print('Other exception: {}'.format(e))
    else:
        print('Serien float len:', len(result['series float']))

    if n == 220:
        reactor.callLater(2, reactor.stop)
    else:
        n += 1
        reactor.callLater(2, test, _connection, n)


def failed(exc):
    log.err('Exception: {}'.format(exc.value))
    reactor.callLater(1, reactor.stop)

if __name__ == '__main__':
    siri = SiriDBClientTwisted(
        username='iris',
        password='siri',
        dbname='dbtest',
        hostlist=[
            ('127.0.0.1', 9000, {'backup': False}),
            ('127.0.0.1', 9001, {'backup': False}),
            # ('127.0.0.1', 9001, {'backup': False}),
            # ('127.0.0.1', 9002, {'backup': False}),
            # ('127.0.0.1', 9003, {'backup': False}),
            # ('127.0.0.1', 9004, {'backup': False}),
            # ('127.0.0.1', 9005, {'backup': False}),
    ])

    n = 0
    d = siri.connect(timeout=10)
    d.addCallback(test, n)
    d.addErrback(failed)
    reactor.run()