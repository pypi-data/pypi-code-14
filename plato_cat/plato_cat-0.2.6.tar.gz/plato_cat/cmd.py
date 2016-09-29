from gevent import monkey
monkey.patch_all()  # noqa

import time
import sys
import traceback
import gevent
from gevent.pool import Pool

from sdk.actions import api

from cases.instance import InstanceCase
from cases.key_pair import KeyPairCase
from cases.eip import EIPCase
from cases.image import ImageCase
from cases.instance_type import InstanceTypeCase
from cases.job import JobCase
from cases.monitor import MonitorCase
from cases.network import NetworkCase
from cases.operation import OperationCase
from cases.quota import QuotaCase
from cases.snapshot import SnapshotCase
from cases.volume import VolumeCase

from cases.instance import CleanInstances
from cases.key_pair import CleanKeyPairs
from cases.image import CleanImages
from cases.network import CleanNetworks
from cases.volume import CleanVolumes
from cases.eip import CleanEips
from cases.snapshot import CleanSnapshots

from alerts.slack import SlackAlert
from alerts.console import ConsoleAlert

exceptions = []
API = None


def run_case(case):
    try:
        case.run(API, gevent.sleep)
    except Exception as ex:
        etype, value, tb = sys.exc_info()
        stack = ''.join(traceback.format_exception(etype,
                                                   value,
                                                   tb,
                                                   100))
        exceptions.append({
            'message': str(ex),
            'traceback': stack,
            'case': case.__class__.__name__,
        })


def alert_exceptions():
    alerts = [
        SlackAlert(),
        ConsoleAlert()
    ]

    if exceptions:
        pool = Pool(2)
        pool.map(lambda alert: alert.call(exceptions), alerts)
        pool.join()


def cat():
    if len(sys.argv) != 4:
        print """execute this with
%s ENDPOINT ACCESS_KEY ACCESS_SECRET""" % sys.argv[0]
        return

    start = time.time()

    global API
    API = api.setup(access_key=sys.argv[2],
                    access_secret=sys.argv[3],
                    endpoint=sys.argv[1],
                    is_debug=True)
    start = time.time()
    cases = [
        InstanceCase(),
        KeyPairCase(),
        ImageCase(),
        InstanceTypeCase(),
        JobCase(),
        MonitorCase(),
        NetworkCase(),
        EIPCase(),
        OperationCase(),
        QuotaCase(),
        VolumeCase(),
        SnapshotCase(),
    ]

    for case in cases:
        run_case(case)

    if exceptions:
        alert_exceptions()

    end = time.time()
    print ('cat finished in %d seconds' % (end - start))


def clean():
    if len(sys.argv) != 4:
        print """execute this with
%s ENDPOINT ACCESS_KEY ACCESS_SECRET""" % sys.argv[0]
        return

    start = time.time()

    global API
    API = api.setup(access_key=sys.argv[2],
                    access_secret=sys.argv[3],
                    endpoint=sys.argv[1],
                    is_debug=True)

    cases = [
        CleanEips(),
        CleanSnapshots(),
        CleanVolumes(),
        CleanInstances(),
        CleanNetworks(),
        CleanImages(),
        CleanKeyPairs(),
    ]

    for case in cases:
        run_case(case)

    if exceptions:
        alert_exceptions()

    end = time.time()
    print ('clean finished in %d seconds' % (end - start))
