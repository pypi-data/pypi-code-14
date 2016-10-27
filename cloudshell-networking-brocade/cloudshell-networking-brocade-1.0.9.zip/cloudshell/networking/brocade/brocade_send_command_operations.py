#!/usr/bin/python
# -*- coding: utf-8 -*-

import inject

from cloudshell.configuration.cloudshell_cli_binding_keys import CLI_SERVICE
from cloudshell.configuration.cloudshell_shell_core_binding_keys import LOGGER, CONTEXT, API
from cloudshell.networking.operations.interfaces.run_command_interface import RunCommandInterface


class BrocadeSendCommandOperations(RunCommandInterface):
    def __init__(self, context=None, api=None, cli_service=None, logger=None):
        self._context = context
        self._api = api
        self._cli_service = cli_service
        self._logger = logger

    @property
    def logger(self):
        return self._logger or inject.instance(LOGGER)

    @property
    def cli_service(self):
        return self._cli_service or inject.instance(CLI_SERVICE)

    @property
    def context(self):
        return self._context or inject.instance(CONTEXT)

    @property
    def api(self):
        return self._api or inject.instance(API)

    def run_custom_command(self, command):
        return self.cli_service.send_command(command=command)

    def run_custom_config_command(self, command):
        return self.cli_service.send_config_command(command=command)
