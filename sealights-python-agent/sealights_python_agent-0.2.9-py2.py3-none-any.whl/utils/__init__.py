import logging
import os
import argparse
import json
import subprocess
import urllib
from urlparse import urlparse
import functools
import pkg_resources
import time

import python_agent.packages.requests
from python_agent.packages.giturlparse import parse
from python_agent import config
from python_agent.test_listener import utils


log = logging.getLogger(__name__)


def retries(logger, tries=3):
    def inner(f):
        @functools.wraps(f)
        def inner_args(*args, **kwargs):
            for i in range(tries):
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    logger.warn("failed try #%s running function %s. args: %s exception: %s"
                                % (str(i + 1), f.func_name, str(args), unicode(e)),  exc_info=True)
                    time.sleep(2 * i)
            raise
        return inner_args
    return inner


def exception_handler(log, quiet=True, message=None):
    def f_exception_handler(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log.exception("%s. Error: %s. Args: %s. Kwargs: %s" % (message, str(e), args, kwargs))
                if not quiet:
                    raise
        return wrapper
    return f_exception_handler


def get_top_relative_path(filepath):
    return os.path.relpath(filepath, os.getcwd())


def validate_server_api(server, is_validate_api=False):
    error_msg = "Must be of the form: http[s]://<server>/api"
    try:
        result = urlparse(server)
        if result.scheme not in ["http", "https"]:
            raise argparse.ArgumentTypeError(error_msg)
        if is_validate_api and "/api" not in result.path:
            raise argparse.ArgumentTypeError(error_msg)
    except Exception:
        raise argparse.ArgumentTypeError(error_msg)
    return server


def validate_server(server):
    return validate_server_api(server, is_validate_api=True)


def get_config_from_server(server, customer_id, app_name, branch, env):
    server_config = {}
    url = None
    try:
        url = "/".join([server, "v1", "config", customer_id, "null", app_name, branch, env, config.app["technology"],
                        pkg_resources.get_distribution("sealights-python-agent").version])
        url = urllib.quote(url, safe="/:")
        response = python_agent.packages.requests.get(url)
        config_data = response.json()
        config_data = config_data.get("config", "{}")
        server_config = json.loads(config_data)
        response.raise_for_status()
        log.info("Fetched Configuration From Server. Configuration: %s" % server_config)
    except Exception as e:
        log.warning("Failed Fetching Configuration From Server. URL: %s. Error: %s" % (url, str(e)))
    return server_config


def get_repo_url():
    raw_url = subprocess.Popen(['git', 'config', '--get', 'remote.origin.url'], stdout=subprocess.PIPE).communicate()[0].replace("\n", "")
    result = parse(raw_url)
    return result.url2https


def get_commit_history():
    commits = subprocess.Popen(['git', 'log', '--format=%H', '-n', '100'], stdout=subprocess.PIPE).communicate()[0].split("\n")
    commits = commits[:-1]
    return commits


def send_test_execution():
    data = {
        "customerId": config.app.get("customer_id"),
        "appName": config.app.get("app_name"),
        "environment": config.app.get("env"),
        "newEnvironment": config.app.get("test_phase")
    }
    url = config.app["server"] + config.TEST_EXECUTION_ROUTE
    try:
        log.info("Sending Test Execution. URL: %s. Data: %s" % (url, data))
        response = python_agent.packages.requests.post(url, json=data)
        response.raise_for_status()
        log.info("Sent Test Execution. Response: %s" % response.content)
    except Exception as e:
        log.exception("Failed Sending Test Execution To Server. URL: %s. Params: %s. Error: %s" % (url, data, str(e)))


def upload_report(metadata_path, report_path, source):
    if not os.path.isfile(report_path):
        log.exception("XML Report Doesn't Exist. Path Checked: %s" % report_path)
        return
    with open(metadata_path, 'w') as f:
        f.write(json.dumps({
            "source": source,
            "type": "JUnitReport",
            "customerId": config.app["customer_id"],
            "appName": config.app["app_name"],
            "environment": utils.create_environment()
        }))
    data = (("metadata", open(metadata_path, "r")), ("report", open(report_path, "r")))
    url = config.app["server"] + config.EXTERNAL_DATA_ROUTE
    try:
        log.info("Uploading JUnit Report. URL: %s." % url)
        response = python_agent.packages.requests.post(url, files=data)
        response.raise_for_status()
    except Exception as e:
        log.exception("Failed Sending XML Report To Server. URL: %s. Data: %s. Error: %s" % (url, data, str(e)))
