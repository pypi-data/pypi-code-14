import functools
import urllib2

from python_agent import config
from python_agent.test_listener.state_tracker import StateTracker


def handle_urllib2(f):
    @functools.wraps(f)
    def inner_handle(self, *args, **kwargs):
        f(self, *args, **kwargs)
        if StateTracker().current_test_identifier:
            self.headers[config.TEST_IDENTIFIER] = StateTracker().current_test_identifier
    return inner_handle

urllib2.Request.__init__ = handle_urllib2(urllib2.Request.__init__)