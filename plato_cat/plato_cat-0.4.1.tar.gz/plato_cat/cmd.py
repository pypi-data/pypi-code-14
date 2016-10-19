from gevent import monkey
monkey.patch_all()  # noqa

import time
import sys
import traceback
import gevent
from gevent.pool import Pool
from gevent import Timeout
import functools

from sdk.actions import api as sdk_api

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

from cases.volume import BenchVolumes

from alerts.slack import SlackAlert
from alerts.console import ConsoleAlert

from oslo_config import cfg
COMMON_OPTS = [
    cfg.StrOpt('endpoint', help='api endpoint'),
    cfg.StrOpt('key', help='access key'),
    cfg.StrOpt('secret', help='access secret')
]

BENCH_OPTS = [
    cfg.IntOpt('total', help=''),
    cfg.IntOpt('concurrent', help=''),
    cfg.IntOpt('ratio', help=''),
    cfg.IntOpt('timeout', help=''),
]

CONF = cfg.CONF
CONF.register_cli_opts(COMMON_OPTS)
CONF.register_opts(COMMON_OPTS)
CONF.register_opts(BENCH_OPTS, group='benchmark')


def _get_api(conf):
    if not (conf.key and conf.secret and conf.endpoint):
        raise Exception('You have to specifiy --key, --secret, --endpoint '
                        'in the cli params, or use config file with '
                        '--config-file /your/config/file/path, '
                        'check cat.conf.sample for example')

    return sdk_api.setup(access_key=conf.key,
                         access_secret=conf.secret,
                         endpoint=conf.endpoint,
                         is_debug=True)


def _run_case(case, api):
    try:
        case.run(api, gevent.sleep)
    except Exception as ex:
        etype, value, tb = sys.exc_info()
        stack = ''.join(traceback.format_exception(etype,
                                                   value,
                                                   tb,
                                                   100))
        return {
            'message': str(ex),
            'traceback': stack,
            'case': case.__class__.__name__,
        }

    return None


def _alert_exceptions(exceptions):
    if not exceptions:
        return

    alerts = [
        SlackAlert(),
        ConsoleAlert()
    ]

    pool = Pool(len(alerts))
    pool.map(lambda x: x.call(exceptions), alerts)
    pool.join()


def _send_report(title, is_pass, stat):
    reports = [
        SlackAlert(),
        ConsoleAlert()
    ]

    pool = Pool(len(reports))
    pool.map(lambda x: x.report(title, is_pass, stat), reports)
    pool.join()


def cat():
    CONF()
    API = _get_api(CONF)

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

    exceptions = map(functools.partial(_run_case, api=API), cases)
    exceptions = filter(lambda x: x, exceptions)
    _alert_exceptions(exceptions)

    end = time.time()
    print ('cat finished in %d seconds' % (end - start))


def clean():
    CONF()
    API = _get_api(CONF)

    start = time.time()
    cases = [
        CleanEips(),
        CleanSnapshots(),
        CleanVolumes(),
        CleanInstances(),
        CleanNetworks(),
        CleanImages(),
        CleanKeyPairs(),
    ]

    exceptions = map(functools.partial(_run_case, api=API), cases)
    exceptions = filter(lambda x: x, exceptions)
    _alert_exceptions(exceptions)

    end = time.time()
    print ('clean finished in %d seconds' % (end - start))


def bench():
    CONF()
    API = _get_api(CONF)

    bmconf = getattr(CONF, 'benchmark')
    concurrent = bmconf.concurrent
    total = bmconf.total
    ratio = bmconf.ratio
    timeout = bmconf.timeout

    # begin all, clean them.
    clean()

    cases = [
        BenchVolumes(API, concurrent, gevent.sleep)
    ]

    for case in cases:
        threads = []

        start = time.time()
        t = Timeout(timeout)
        t.start()
        try:
            pool = Pool(concurrent)
            for i in xrange(0, total):
                threads.append(pool.spawn(case.run, API, gevent.sleep))
            pool.join()

        except Timeout:
            pass

        finally:
            t.cancel()

        end = time.time()
        succ = len([t1.value for t1 in threads if t1.value])
        fail = len([t2.value for t2 in threads if not t2.value])
        not_run = total - succ - fail

        title = ('Report: case: %s finished in : %d seconds. \n'
                 'Target: run %d total (with %d concurrent) must '
                 'finish in %d seconds with %d%% success rate.') % (
                  case.__class__.__name__,
                  end - start,
                  total,
                  concurrent,
                  timeout,
                  ratio)

        stat = {
            'total': total,
            'succ': succ,
            'fail': fail,
            'not_run': not_run,
            'time': int(end - start),
        }

        is_pass = int(succ * 100.0 / total) >= ratio

        _send_report(title, is_pass, stat)

    # after all, clean them.
    clean()
