import os
import logging
import logging.config
import platform
import socket
import pkg_resources

from python_agent import config

log = logging.getLogger(__name__)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def create_environment():
    try:
        return {
            "agentType": "python",
            "agentVersion": pkg_resources.get_distribution("sealights-python-agent").version,
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
