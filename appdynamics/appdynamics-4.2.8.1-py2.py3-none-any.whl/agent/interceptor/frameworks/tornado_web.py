import contextlib
import functools
import sys

from ..base import BaseInterceptor
from appdynamics.agent.models.transactions import ENTRY_TORNADO
from appdynamics.lib import LazyWsgiRequest


class TornadoRequestHandlerInterceptor(BaseInterceptor):
    @contextlib.contextmanager
    def current_bt_manager(self, bt):
        self.agent.set_current_bt(bt)
        try:
            yield
        except:
            # untested code!!!
            if bt:
                bt.add_exception(*sys.exc_info())
            raise
        finally:
            self.agent.unset_current_bt()

    def __execute(self, _execute, handler, *args, **kwargs):
        import tornado.stack_context
        import tornado.wsgi
        bt = None
        with self.log_exceptions():
            bt = self.agent.start_transaction(
                ENTRY_TORNADO, request=LazyWsgiRequest(tornado.wsgi.WSGIContainer.environ(handler.request)))

        with tornado.stack_context.StackContext(functools.partial(self.current_bt_manager, bt)):
            return _execute(handler, *args, **kwargs)

    def __handle_request_exception(self, _handle_request_exception, handler, *args, **kwargs):
        # Catch errors in the handler function itself, `prepare`, and `on_finish`.
        if self.bt:
            self.bt.add_exception(*sys.exc_info())
        return _handle_request_exception(handler, *args, **kwargs)

    def _on_finish(self, on_finish, handler):
        self.agent.end_transaction(self.bt)
        return on_finish(handler)


def intercept_tornado_web(agent, mod):
    TornadoRequestHandlerInterceptor(agent, mod.RequestHandler).attach(
        ['_execute', '_handle_request_exception', 'on_finish'])
