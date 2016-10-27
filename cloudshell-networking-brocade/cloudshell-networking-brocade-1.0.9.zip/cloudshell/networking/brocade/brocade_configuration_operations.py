#!/usr/bin/python
# -*- coding: utf-8 -*-

import inject

from cloudshell.configuration.cloudshell_cli_binding_keys import CLI_SERVICE, SESSION
from cloudshell.configuration.cloudshell_shell_core_binding_keys import LOGGER, CONTEXT, API
from cloudshell.networking.brocade.brocade_state_operations import BrocadeStateOperations
from cloudshell.networking.operations.configuration_operations import ConfigurationOperations
from cloudshell.shell.core.config_utils import override_attributes_from_config
from cloudshell.shell.core.context_utils import get_resource_name


class BrocadeConfigurationOperations(ConfigurationOperations):
    DEFAULT_PROMPT = r'[>$#]\s*$'
    SESSION_WAIT_TIMEOUT = 600
    SAVE_RESPONSE_TIMEOUT = 3
    SAVE_RESPONSE_RETRIES = 10

    def __init__(self, context=None, api=None, cli_service=None, logger=None):
        self._context = context
        self._api = api
        self._cli_service = cli_service
        self._logger = logger
        overridden_config = override_attributes_from_config(BrocadeConfigurationOperations)
        self._default_prompt = overridden_config.DEFAULT_PROMPT
        self._session_wait_timeout = overridden_config.SESSION_WAIT_TIMEOUT
        self._save_response_timeout = overridden_config.SAVE_RESPONSE_TIMEOUT
        self._save_response_retries = overridden_config.SAVE_RESPONSE_RETRIES

    @property
    def api(self):
        return self._api or inject.instance(API)

    @property
    def cli_service(self):
        return self._cli_service or inject.instance(CLI_SERVICE)

    @property
    def logger(self):
        return self._logger or inject.instance(LOGGER)

    @property
    def context(self):
        return self._context or inject.instance(CONTEXT)

    @property
    def session(self):
        return inject.instance(SESSION)

    @property
    def state_operations(self):
        return BrocadeStateOperations()

    @property
    def resource_name(self):
        return get_resource_name().replace(" ", "_")

    def restore(self, path, configuration_type, restore_method, vrf_management_name=None):
        """ General method for restore configuration on Brocade devices """
        pass

    def save(self, folder_path, configuration_type, vrf_management_name=None):
        """ General method for save configuration on Brocade devices """
        pass
