import os
import sys
import logging

from coverage.cmdline import Opts, unshell_list

from python_agent import config
from python_agent.utils import get_config_from_server, validate_server, validate_server_api
from python_agent.utils.autoupgrade import AutoUpgrade
if sys.version_info < (2, 7):
    from python_agent.packages.dictconfig import dictConfig
else:
    from logging.config import dictConfig


log = logging.getLogger(__name__)


def add_options(parser, add_option_method):
    for args, kwargs in OPTIONS.items():
        getattr(parser, add_option_method)(*[args], **kwargs)


def parse_cmd_line_args(parser):
    args, unknown_args = parser.parse_known_args()
    return args, unknown_args


def get_server_args(cmd_line_args):
    server_config = get_config_from_server(
        cmd_line_args["server"],
        cmd_line_args["customer_id"],
        cmd_line_args["app_name"],
        cmd_line_args["branch"],
        cmd_line_args["env"]
    )
    return server_config


def init_configuration(cmd_line_args):
    server_args = get_server_args(cmd_line_args)
    environ_args = dict((environment_variable_name, os.environ.get(environment_variable_name))
                        for environment_variable_name in config.app.keys())

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

    return args


def upgrade_agent():
    auto_upgrade = AutoUpgrade("sealights-python-agent", config.app["server"], config.app["customer_id"])
    auto_upgrade.upgrade()


def config_logging():
    dictConfig(config.LOG_CONF)
    try:
        log_conf = config.app.get("logging")
        if log_conf and isinstance(log_conf, dict):
            dictConfig(log_conf)
    except:
        log.warning("failed configuring logging for python agent. wanted config: %s. default config: %s"
                    % (config.app.get("logging"), config.LOG_CONF))


config_logging()
OPTIONS = {
    "--customer_id": {"required": True, "help": "An id representing the client"},
    "--app_name": {"required": True, "help": "The name of the application"},
    "--server": {"type": validate_server, "required": True, "help": "Sealights Server. Must be of the form: http[s]://<server>/api"},
    "--build": {"default": config.DEFAULT_BUILD, "help": "The build number of the application"},
    "--branch": {"default": config.DEFAULT_BRANCH, "help": "The branch of the current build"},
    "--env": {"default": config.DEFAULT_ENV, "help": "The environment of the current build"},
    "--proxy": {"type": validate_server_api, "help": "Go through proxy server. Must be of the form: http[s]://<server>"},
    Opts.source.get_opt_string(): {
        "action": Opts.source.action,
        "metavar": Opts.source.metavar,
        "help": Opts.source.help,
        "type": unshell_list
    },
    Opts.include.get_opt_string(): {
        "action": Opts.include.action,
        "metavar": Opts.include.metavar,
        "help": Opts.include.help,
        "type": unshell_list
    },
    Opts.omit.get_opt_string(): {
        "action": Opts.omit.action,
        "metavar": Opts.omit.metavar,
        "help": Opts.omit.help,
        "type": unshell_list
    }
}
