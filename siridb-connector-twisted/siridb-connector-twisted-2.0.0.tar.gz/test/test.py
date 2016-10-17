import sys
from twisted.python import log
from twisted.internet import defer
from twisted.internet import task
from twisted.internet import reactor
import qpack
import time
import random

sys.path.append('..')
from siridb.twisted import SiriDBClientTwisted
from siridb.twisted.lib.exceptions import InsertError


def insertError(exc):
    print('!!!!: : {}'.format(exc))

@defer.inlineCallbacks
def test(_connection):
    data = {'series float': [
        [4.0, int(time.time()), random.random() * 10]
    ]}
    try:
        defr = siri.insert(data)
        defr.addErrback(insertError)
    except Exception as e:
        print('Exception: {}'.format(e))

    result = yield siri.query('select * from "series float"')
    print(result)

    siri.close()
    reactor.callLater(2, reactor.stop)




if __name__ == '__main__':
    siri = SiriDBClientTwisted(
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

    d = siri.connect(timeout=10)
    d.addCallback(test)
    reactor.run()