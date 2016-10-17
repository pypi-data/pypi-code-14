import os
import sys
import logging

from python_agent import config
from python_agent.utils import get_config_from_server, send_test_execution
from python_agent.utils.autoupgrade import AutoUpgrade
if sys.version_info < (2, 7):
    from python_agent.packages.dictconfig import dictConfig
else:
    from logging.config import dictConfig


log = logging.getLogger(__name__)


def get_server_args(cmd_line_args):
    log.info("Fetching Configuration From Server. Command Line Args: %s" % cmd_line_args)
    server_config = get_config_from_server(
        cmd_line_args["server"],
        cmd_line_args["customer_id"],
        cmd_line_args["app_name"],
        cmd_line_args["branch"],
        cmd_line_args["env"]
    )
    return server_config


def init_configuration(cmd_line_args):
    log.info("Initializing Configuration...")
    server_args = get_server_args(cmd_line_args)
    environ_args = dict((environment_variable_name, os.environ.get(environment_variable_name))
                        for environment_variable_name in config.app.keys())
    log.info("Environment Variables Configuration: %s" % environ_args)

    # Step 1, take command line args
    args = cmd_line_args

    # Step 2, complement with environment variables
    for env_variable_name, env_variable_value in environ_args.items():
        if env_variable_value and not args.get(env_variable_name):
            args[env_variable_name] = env_variable_value

    # Step 3, override with server args
    if server_args:
        args = server_args

    config.app.update(args)
    log.info("Final Configuration: %s" % config.app)
    return args


def upgrade_agent():
    log.info("Upgrading Agent")
    auto_upgrade = AutoUpgrade("sealights-python-agent", config.app["server"], config.app["customer_id"])
    auto_upgrade.upgrade()


def config_logging():
    dictConfig(config.LOG_CONF)
    try:
        log_conf = config.app.get("logging")
        if log_conf and isinstance(log_conf, dict):
            dictConfig(log_conf)
    except:
        log.warning("Failed Configuring Logging From Server. Wanted Config: %s. Default Config: %s"
                    % (config.app.get("logging"), config.LOG_CONF))


def init_coloring():
    from python_agent.test_listener.coloring import __all__
    for coloring_framework_name in __all__:
        __import__(
            "%s.%s.%s.%s" % ("python_agent", "test_listener", "coloring", coloring_framework_name),
            fromlist=[coloring_framework_name]
        )
        log.debug("Imported Coloring Framework: %s" % coloring_framework_name)
    log.info("Imported Coloring Frameworks: %s" % __all__)


def bootstrap():
    from python_agent.test_listener.web_frameworks import __all__
    for web_framework_name in __all__:
        web_framework = __import__(
            "%s.%s.%s.%s" % ("python_agent", "test_listener", "web_frameworks", web_framework_name),
            fromlist=[web_framework_name]
        )
        bootstrap_method = getattr(web_framework, "bootstrap", None)
        if bootstrap_method:
            bootstrap_method()
            log.debug("Bootstrapped Framework: %s" % web_framework_name)
    log.info("Bootstrapped Frameworks: %s" % __all__)


def init_test_execution():
    send_test_execution()
