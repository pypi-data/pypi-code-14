import logging
import os
import sys

import pip
import pkg_resources
from pip import status_codes
try:
    from pip import commands_dict
except ImportError:
    from pip import commands as commands_dict

from python_agent.packages import requests, semantic_version

log = logging.getLogger(__name__)


class AutoUpgrade(object):
    def __init__(self, pkg, server, customer_id):
        self.pkg = pkg
        self.server = server
        self.customer_id = customer_id

    def get_recommended_version(self):
        url = ""
        params = {}
        try:
            url = "/".join([self.server, "v1", "agents", self.pkg, "recommended"])
            params = {"customerId": self.customer_id}
            response = requests.get(url, params=params)
            response.raise_for_status()
            version = response.json().get("agent", {}).get("version")
            log.info("Recommended Agent Version: %s" % version)
            return semantic_version.Version(version)
        except Exception as e:
            log.warning("Failed Getting Recommended Version. URL: %s. Params: %s. Error: %s" % (url, params, str(e)))
        return self.get_current_version()

    def get_current_version(self):
        try:
            current_version = pkg_resources.get_distribution(self.pkg).version
            current_version = semantic_version.Version(current_version)
            return current_version
        except Exception as e:
            log.warning("Failed Getting Current Version. Pkg. %s" % self.pkg)
        return semantic_version.Version("0.0.0")

    def upgrade(self):
        status = status_codes.ERROR
        current_version = self.get_current_version()
        log.info("Current Agent Version: %s" % current_version)
        recommended_version = self.get_recommended_version()
        if recommended_version != current_version:
            try:
                status = self.install(recommended_version)
                if status == status_codes.SUCCESS:
                    log.info("Upgraded Agent Successfully. Restarting Agent With Version: %s" % recommended_version)
                    self.restart()
            except SystemExit as e:
                log.info("Failed Upgrading Or Restarting Agent. System Exit: %s" % str(e))
                return status_codes.ERROR
            except Exception as e:
                log.info("Failed Upgrading Or Restarting Agent. Error: %s" % str(e))
                return status_codes.ERROR
        return status

    def restart(self):
        os.execl(sys.executable, *([sys.executable] + sys.argv))

    def install(self, recommended_version):
        log.info("Installing Agent Version: %s" % recommended_version)
        cmd_name, cmd_args = pip.parseopts([
            "install",
            self.pkg + "==" + str(recommended_version),
            "--ignore-installed"
        ])
        command = commands_dict[cmd_name](isolated=pip.check_isolated(cmd_args))
        options, args = command.parse_args(cmd_args)
        status = command.run(options, args)
        return status
