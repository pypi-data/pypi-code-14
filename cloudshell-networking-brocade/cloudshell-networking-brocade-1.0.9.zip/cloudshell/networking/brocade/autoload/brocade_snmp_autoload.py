#!/usr/bin/python
# -*- coding: utf-8 -*-

import inject
import re
import os

from cloudshell.configuration.cloudshell_cli_binding_keys import CLI_SERVICE
from cloudshell.configuration.cloudshell_shell_core_binding_keys import LOGGER, CONFIG
from cloudshell.configuration.cloudshell_snmp_binding_keys import SNMP_HANDLER
from cloudshell.networking.operations.interfaces.autoload_operations_interface import AutoloadOperationsInterface
from cloudshell.shell.core.context_utils import get_attribute_by_name


class BrocadeSnmpAutoload(AutoloadOperationsInterface):
    def __init__(self, snmp_handler=None, logger=None, config=None, cli_service=None, snmp_community=None):
        """Basic init with injected snmp handler and logger

        :param snmp_handler:
        :param logger:
        :param config:
        :return:
        """
        self._config = config
        self._snmp = snmp_handler
        self._logger = logger
        self._enable_snmp = True
        self._disable_snmp = False
        self.snmp_community = snmp_community
        if not self.snmp_community:
            self.snmp_community = get_attribute_by_name("SNMP Read Community")
        self._cli_service = cli_service

    @property
    def logger(self):
        return self._logger or inject.instance(LOGGER)

    @property
    def config(self):
        return self._config or inject.instance(CONFIG)

    @property
    def snmp(self):
        if not self._snmp:
            self._snmp = inject.instance(SNMP_HANDLER)
        return self._snmp

    @property
    def cli_service(self):
        return self._cli_service or inject.instance(CLI_SERVICE)

    def load_additional_mibs(self):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mibs"))
        self.snmp.update_mib_sources(path)

    def enable_snmp(self):
        """ Enable SNMP server and configure community """

        self.cli_service.send_config_command("enable password-display")
        snmp_data = self.cli_service.send_config_command("show snmp server")

        snmp_status = re.search(r"Status:\s*(?P<status>\w+)\n", snmp_data)
        if snmp_status:
            snmp_status = snmp_status.group("status")

        snmp_ro_community = re.search(r"Community\(ro\):\s*(?P<snmp_ro_community>.+)\n", snmp_data)
        if snmp_ro_community:
            snmp_ro_community = snmp_ro_community.group("snmp_ro_community")
        else:
            snmp_ro_community = ""

        if "disabled" in snmp_status.lower():
            self.cli_service.send_config_command("snmp-server")

        if self.snmp_community not in snmp_ro_community:
            self.cli_service.send_config_command("snmp-server community {} ro".format(self.snmp_community))

    def disable_snmp(self):
        """ Disable SNMP server and remove community from configuration """
        self.cli_service.send_config_command("no snmp-server community {} ro".format(self.snmp_community))
        self.cli_service.send_config_command("no snmp-server")

    def discover(self):
        """
        General entry point for autoload

        :return: AutoLoadDetails object or Exception
        """

        if not self.snmp_community:
            raise Exception(self.__class__.__name__, "SNMP Read Community shouldn't be empty")

        try:
            self._enable_snmp = (get_attribute_by_name('Enable SNMP') or 'true').lower() == 'true'
            self._disable_snmp = (get_attribute_by_name('Disable SNMP') or 'false').lower() == 'true'
        except:
            pass

        if self._enable_snmp:
            self.enable_snmp()

        try:
            return self._get_autoload_details()
        except Exception as e:
            self.logger.error('Autoload failed: {0}'.format(e))
            raise Exception(self.__class__.__name__, e)
        finally:
            if self._disable_snmp:
                self.disable_snmp()

    def _get_autoload_details(self):
        """
        Read device structure and attributes:
        chassis, modules, submodules, ports, port-channels and power supplies

        :return: AutoLoadDetails object or Exception
        """

        pass
