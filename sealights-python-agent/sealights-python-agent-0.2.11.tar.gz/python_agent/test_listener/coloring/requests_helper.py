import functools
import os
from urlparse import urlparse

from python_agent import config
from python_agent.test_listener.state_tracker import StateTracker

try:
    import requests
except ImportError:
    from python_agent.packages import requests


def handle_requests(f):
    @functools.wraps(f)
    def inner_handle(*args, **kwargs):
        if StateTracker().current_test_identifier:
            headers = kwargs.get("headers", {})
            headers[config.TEST_IDENTIFIER] = StateTracker().current_test_identifier
            kwargs["headers"] = headers

        proxy = config.app["proxy"]
        if proxy:
            result = urlparse(proxy)
            if result.scheme == "https":
                os.environ["https_proxy"] = proxy
            else:
                os.environ["http_proxy"] = proxy
        return f(*args, **kwargs)
    return inner_handle

requests.post = handle_requests(requests.post)
requests.get = handle_requests(requests.get)
requests.put = handle_requests(requests.put)
requests.delete = handle_requests(requests.delete)
requests.patch = handle_requests(requests.patch)