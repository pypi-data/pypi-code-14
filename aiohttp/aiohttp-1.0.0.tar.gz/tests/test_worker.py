"""Tests for aiohttp/worker.py"""
import asyncio
import logging
import pathlib
import ssl
from unittest import mock

import pytest

from aiohttp import helpers
from aiohttp.test_utils import make_mocked_coro

base_worker = pytest.importorskip('aiohttp.worker')


try:
    import uvloop
except ImportError:
    uvloop = None


WRONG_LOG_FORMAT = '%a "%{Referrer}i" %(h)s %(l)s %s'
ACCEPTABLE_LOG_FORMAT = '%a "%{Referrer}i" %s'


class BaseTestWorker:

    def __init__(self):
        self.servers = {}
        self.exit_code = 0
        self.cfg = mock.Mock()
        self.cfg.graceful_timeout = 100


class AsyncioWorker(BaseTestWorker, base_worker.GunicornWebWorker):
    pass


PARAMS = [AsyncioWorker]
if uvloop is not None:
    class UvloopWorker(BaseTestWorker, base_worker.GunicornUVLoopWebWorker):
        pass

    PARAMS.append(UvloopWorker)


@pytest.fixture(params=PARAMS)
def worker(request):
    ret = request.param()
    ret.notify = mock.Mock()
    return ret


def test_init_process(worker):
    with mock.patch('aiohttp.worker.asyncio') as m_asyncio:
        try:
            worker.init_process()
        except TypeError:
            pass

        assert m_asyncio.get_event_loop.return_value.close.called
        assert m_asyncio.new_event_loop.called
        assert m_asyncio.set_event_loop.called


def test_run(worker, loop):
    worker.wsgi = mock.Mock()

    worker.loop = loop
    worker._run = mock.Mock(
        wraps=asyncio.coroutine(lambda: None))
    worker.wsgi.startup = make_mocked_coro(None)
    with pytest.raises(SystemExit):
        worker.run()
    assert worker._run.called
    worker.wsgi.startup.assert_called_once_with()
    assert loop.is_closed()


def test_handle_quit(worker):
    worker.handle_quit(object(), object())
    assert not worker.alive
    assert worker.exit_code == 0


def test_handle_abort(worker):
    worker.handle_abort(object(), object())
    assert not worker.alive
    assert worker.exit_code == 1


def test_init_signals(worker):
    worker.loop = mock.Mock()
    worker.init_signals()
    assert worker.loop.add_signal_handler.called


def test_make_handler(worker, mocker):
    worker.wsgi = mock.Mock()
    worker.loop = mock.Mock()
    worker.log = mock.Mock()
    worker.cfg = mock.Mock()
    worker.cfg.access_log_format = ACCEPTABLE_LOG_FORMAT
    mocker.spy(worker, '_get_valid_log_format')

    f = worker.make_handler(worker.wsgi)
    assert f is worker.wsgi.make_handler.return_value
    assert worker._get_valid_log_format.called


def test_make_handler_debug_in_config(worker, mocker):
    app = mock.Mock()
    make_handler = app.make_handler = mock.Mock()
    worker.cfg.debug = True
    worker.cfg.access_log_format = worker.DEFAULT_GUNICORN_LOG_FORMAT
    worker.cfg.keepalive = 10
    worker.cfg.timeout = 15
    worker.log = mock.Mock()
    worker.make_handler(app)
    make_handler.assert_called_with(
        access_log=mock.ANY,
        access_log_format=worker.DEFAULT_AIOHTTP_LOG_FORMAT,
        debug=True,
        keepalive_timeout=10,
        logger=mock.ANY,
        slow_request_timeout=15)


def test_make_handler_no_debug_in_config(worker, mocker):
    app = mock.Mock()
    make_handler = app.make_handler = mock.Mock()
    del worker.cfg.debug
    worker.cfg.access_log_format = worker.DEFAULT_GUNICORN_LOG_FORMAT
    worker.cfg.keepalive = 10
    worker.cfg.timeout = 15
    worker.log = mock.Mock()
    worker.log.loglevel = logging.DEBUG
    worker.make_handler(app)
    make_handler.assert_called_with(
        access_log=mock.ANY,
        access_log_format=worker.DEFAULT_AIOHTTP_LOG_FORMAT,
        debug=True,
        keepalive_timeout=10,
        logger=mock.ANY,
        slow_request_timeout=15)


def test_make_handler_no_debug_in_config_not_debug_logger(worker, mocker):
    app = mock.Mock()
    make_handler = app.make_handler = mock.Mock()
    del worker.cfg.debug
    worker.cfg.access_log_format = worker.DEFAULT_GUNICORN_LOG_FORMAT
    worker.cfg.keepalive = 10
    worker.cfg.timeout = 15
    worker.log = mock.Mock()
    worker.log.loglevel = logging.INFO
    worker.make_handler(app)
    make_handler.assert_called_with(
        access_log=mock.ANY,
        access_log_format=worker.DEFAULT_AIOHTTP_LOG_FORMAT,
        debug=False,
        keepalive_timeout=10,
        logger=mock.ANY,
        slow_request_timeout=15)


@pytest.mark.parametrize('source,result', [
    (ACCEPTABLE_LOG_FORMAT, ACCEPTABLE_LOG_FORMAT),
    (AsyncioWorker.DEFAULT_GUNICORN_LOG_FORMAT,
     AsyncioWorker.DEFAULT_AIOHTTP_LOG_FORMAT),
])
def test__get_valid_log_format_ok(worker, source, result):
    assert result == worker._get_valid_log_format(source)


def test__get_valid_log_format_exc(worker):
    with pytest.raises(ValueError) as exc:
        worker._get_valid_log_format(WRONG_LOG_FORMAT)
    assert '%(name)s' in str(exc)


@asyncio.coroutine
def test__run_ok(worker, loop):
    worker.ppid = 1
    worker.alive = True
    worker.servers = {}
    sock = mock.Mock()
    sock.cfg_addr = ('localhost', 8080)
    worker.sockets = [sock]
    worker.wsgi = mock.Mock()
    worker.close = make_mocked_coro(None)
    worker.log = mock.Mock()
    worker.loop = loop
    loop.create_server = make_mocked_coro(sock)
    worker.wsgi.make_handler.return_value.requests_count = 1
    worker.cfg.max_requests = 100
    worker.cfg.is_ssl = True
    worker.cfg.access_log_format = ACCEPTABLE_LOG_FORMAT

    ssl_context = mock.Mock()
    with mock.patch('ssl.SSLContext', return_value=ssl_context):
        with mock.patch('aiohttp.worker.asyncio') as m_asyncio:
            m_asyncio.sleep = mock.Mock(
                wraps=asyncio.coroutine(lambda *a, **kw: None))
            yield from worker._run()

    worker.notify.assert_called_with()
    worker.log.info.assert_called_with("Parent changed, shutting down: %s",
                                       worker)

    args, kwargs = loop.create_server.call_args
    assert 'ssl' in kwargs
    ctx = kwargs['ssl']
    assert ctx is ssl_context


@asyncio.coroutine
def test__run_exc(worker, loop):
    with mock.patch('aiohttp.worker.os') as m_os:
        m_os.getpid.return_value = 1
        m_os.getppid.return_value = 1

        handler = mock.Mock()
        handler.requests_count = 0
        worker.servers = {mock.Mock(): handler}
        worker.ppid = 1
        worker.alive = True
        worker.sockets = []
        worker.log = mock.Mock()
        worker.loop = loop
        worker.cfg.is_ssl = False
        worker.cfg.max_redirects = 0
        worker.cfg.max_requests = 100

        with mock.patch('aiohttp.worker.asyncio.sleep') as m_sleep:
            slp = helpers.create_future(loop)
            slp.set_exception(KeyboardInterrupt)
            m_sleep.return_value = slp

            worker.close = make_mocked_coro(None)

            yield from worker._run()

        m_sleep.assert_called_with(1.0, loop=loop)
        worker.close.assert_called_with()


@asyncio.coroutine
def test_close(worker, loop):
    srv = mock.Mock()
    srv.wait_closed = make_mocked_coro(None)
    handler = mock.Mock()
    worker.servers = {srv: handler}
    worker.log = mock.Mock()
    worker.loop = loop
    app = worker.wsgi = mock.Mock()
    app.cleanup = make_mocked_coro(None)
    handler.connections = [object()]
    handler.finish_connections.return_value = helpers.create_future(loop)
    handler.finish_connections.return_value.set_result(1)

    app.shutdown.return_value = helpers.create_future(loop)
    app.shutdown.return_value.set_result(None)

    yield from worker.close()
    app.shutdown.assert_called_with()
    app.cleanup.assert_called_with()
    handler.finish_connections.assert_called_with(timeout=95.0)
    srv.close.assert_called_with()
    assert worker.servers is None

    yield from worker.close()


@asyncio.coroutine
def test__run_ok_no_max_requests(worker, loop):
    worker.ppid = 1
    worker.alive = True
    worker.servers = {}
    sock = mock.Mock()
    sock.cfg_addr = ('localhost', 8080)
    worker.sockets = [sock]
    worker.wsgi = mock.Mock()
    worker.close = make_mocked_coro(None)
    worker.log = mock.Mock()
    worker.loop = loop
    loop.create_server = make_mocked_coro(sock)
    worker.wsgi.make_handler.return_value.requests_count = 1
    worker.cfg.access_log_format = ACCEPTABLE_LOG_FORMAT
    worker.cfg.max_requests = 0
    worker.cfg.is_ssl = True

    ssl_context = mock.Mock()
    with mock.patch('ssl.SSLContext', return_value=ssl_context):
        with mock.patch('aiohttp.worker.asyncio') as m_asyncio:
            m_asyncio.sleep = mock.Mock(
                wraps=asyncio.coroutine(lambda *a, **kw: None))
            yield from worker._run()

    worker.notify.assert_called_with()
    worker.log.info.assert_called_with("Parent changed, shutting down: %s",
                                       worker)

    args, kwargs = loop.create_server.call_args
    assert 'ssl' in kwargs
    ctx = kwargs['ssl']
    assert ctx is ssl_context


@asyncio.coroutine
def test__run_ok_max_requests_exceeded(worker, loop):
    worker.ppid = 1
    worker.alive = True
    worker.servers = {}
    sock = mock.Mock()
    sock.cfg_addr = ('localhost', 8080)
    worker.sockets = [sock]
    worker.wsgi = mock.Mock()
    worker.close = make_mocked_coro(None)
    worker.log = mock.Mock()
    worker.loop = loop
    loop.create_server = make_mocked_coro(sock)
    worker.wsgi.make_handler.return_value.requests_count = 15
    worker.cfg.access_log_format = ACCEPTABLE_LOG_FORMAT
    worker.cfg.max_requests = 10
    worker.cfg.is_ssl = True

    ssl_context = mock.Mock()
    with mock.patch('ssl.SSLContext', return_value=ssl_context):
        with mock.patch('aiohttp.worker.asyncio') as m_asyncio:
            m_asyncio.sleep = mock.Mock(
                wraps=asyncio.coroutine(lambda *a, **kw: None))
            yield from worker._run()

    worker.notify.assert_called_with()
    worker.log.info.assert_called_with("Max requests, shutting down: %s",
                                       worker)

    args, kwargs = loop.create_server.call_args
    assert 'ssl' in kwargs
    ctx = kwargs['ssl']
    assert ctx is ssl_context


def test__create_ssl_context_without_certs_and_ciphers(worker):
    here = pathlib.Path(__file__).parent
    worker.cfg.ssl_version = ssl.PROTOCOL_SSLv23
    worker.cfg.cert_reqs = ssl.CERT_OPTIONAL
    worker.cfg.certfile = str(here / 'sample.crt')
    worker.cfg.keyfile = str(here / 'sample.key')
    worker.cfg.ca_certs = None
    worker.cfg.ciphers = None
    crt = worker._create_ssl_context(worker.cfg)
    assert isinstance(crt, ssl.SSLContext)
