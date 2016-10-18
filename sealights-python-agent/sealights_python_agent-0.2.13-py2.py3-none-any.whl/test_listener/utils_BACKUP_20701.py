import os
import logging
import logging.config
import functools
import threading
import urllib
import urllib2
from urlparse import urlparse

from selenium.webdriver.remote.webdriver import WebDriver

try:
    import requests
except ImportError:
    from python_agent.packages import requests

from python_agent import config, VERSION

log = logging.getLogger(__name__)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


<<<<<<< Updated upstream
class StateTracker(object):
    __metaclass__ = Singleton

    def __init__(self):
        self._lock = threading.Lock()
        self._current_test_identifier = None

    def __str__(self):
        if self._current_test_identifier:
            return "State: %s" % self._current_test_identifier
        return "Not in test"

    @property
    def current_test_identifier(self):
        return self._current_test_identifier

    @current_test_identifier.setter
    def current_test_identifier(self, test_id):
        self._lock.acquire()
        if self._current_test_identifier != test_id:
            self._current_test_identifier = test_id
        self._lock.release()


def identify_framework(frames):
    for frame in frames:
        if "pytest" in frame[1]:
            return "pytest"
        if "unittest" in frame[1]:
            return "unittest"


def is_test_equal_to_frame(framework, frame):
    current_test_identifier = StateTracker().current_test_identifier
    if not current_test_identifier:
        return False
    if framework == "pytest":
        test_id = urllib.url2pathname(current_test_identifier.split("/")[-1])
        file_name = frame[1].split("/")[-1] if frame[1] else ""
        test_name = frame[3] if frame[3] else ""
        return file_name + "::" + test_name == test_id
    if framework == "unittest":
        test_id = urllib.url2pathname(current_test_identifier.split("/")[-1])
        file_name_test = frame[0].f_locals["self"].id() if frame[0] else ""
        return file_name_test == test_id


def new_execute(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            import inspect
            self = args[0]
            frames = inspect.stack()
            for index, frame in enumerate(frames):
                framework = identify_framework(frames)
                if is_test_equal_to_frame(framework, frame):
                    params = {
                        "sessionId": self.session_id,
                        "cookie": {
                            "name": config.TEST_IDENTIFIER,
                            "value": StateTracker().current_test_identifier
                        }
                    }
                    self.command_executor.execute("addCookie", params)
        except Exception as e:
            log.exception("failed to set cookie. cookie: %s. error: %s"
                          % (StateTracker().current_test_identifier, str(e)))
            print str(e)
        return f(*args, **kwargs)
    return wrapper

WebDriver.execute = new_execute(WebDriver.execute)


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


def handle_urllib2(f):
    @functools.wraps(f)
    def inner_handle(*args, **kwargs):
        request = f(*args, **kwargs)
        if StateTracker().current_test_identifier:
            request.headers[config.TEST_IDENTIFIER] = StateTracker().current_test_identifier
        return request
    return inner_handle

urllib2.Request.__init__ = handle_urllib2(urllib2.Request.__init__)
=======
def create_environment():
    try:
        return {
            "agentType": "python",
            "agentVersion": VERSION,
            "environmentName": config.app["env"],
            "machineName": socket.gethostname(),
            "platform": platform.platform(),
            "os": platform.system(),
            "osVersion": platform.release(),
            "arch": platform.machine(),
            "processId": os.getpid(),
            "dependencies": dict((package_name, pkg_resources.require(package_name)[0].version)
                                 for package_name, class_name in pkg_resources.working_set.by_key.items()),
            "compiler": platform.python_compiler(),
            "interpreter": platform.python_implementation(),
            "runtime": platform.python_version(),
            "configuration": config.app
        }
    except Exception as e:
        log.exception("failed to create environment. error: %s" % str(e))
    return {
        "agentType": "python",
        "agentVersion": "",
        "environmentName": config.app["env"],
        "configuration": config.app
    }


def get_test_name_from_identifier(test_identifier):
    if not test_identifier:
        return ""
    if "/" not in test_identifier:
        return test_identifier
    test_name_parts = test_identifier.split("/")[1:]
    return "/".join(test_name_parts)


def get_execution_id_from_identifier(test_identifier):
    if not test_identifier:
        return ""
    return test_identifier.split("/")[0]
>>>>>>> Stashed changes
