#!/usr/bin/python
# -*- coding: utf-8 -*-

import inject
import time

from cloudshell.configuration.cloudshell_cli_binding_keys import CLI_SERVICE, SESSION
from cloudshell.configuration.cloudshell_shell_core_binding_keys import LOGGER, API
from cloudshell.networking.operations.state_operations import StateOperations
from cloudshell.shell.core.config_utils import override_attributes_from_config
from cloudshell.shell.core.context_utils import get_resource_name


class BrocadeStateOperations(StateOperations):
    DEFAULT_PROMPT = r'[>$#]\s*$'
    SESSION_WAIT_TIMEOUT = 600

    def __init__(self, cli_service=None, logger=None, api=None, resource_name=None):
        StateOperations.__init__(self)
        self._cli_service = cli_service
        self._logger = logger
        self._api = api
        self._resource_name = resource_name
        overridden_config = override_attributes_from_config(BrocadeStateOperations)
        self._default_prompt = overridden_config.DEFAULT_PROMPT
        self._session_wait_timeout = overridden_config.SESSION_WAIT_TIMEOUT

    @property
    def logger(self):
        return self._logger or inject.instance(LOGGER)

    @property
    def cli(self):
        return self._cli_service or inject.instance(CLI_SERVICE)

    @property
    def api(self):
        return self._api or inject.instance(API)

    @property
    def session(self):
        return inject.instance(SESSION)

    @property
    def resource_name(self):
        if self._resource_name is None:
            try:
                self._resource_name = get_resource_name()
            except:
                raise Exception(self.__class__.__name__, 'Failed to get api handler.')
        return self._resource_name

    def shutdown(self):
        """ Shutdown device """
        pass

    def reload(self):
        """ Reload device """

        expected_map = {"(enter 'y' or 'n')": lambda session: session.send_line('y')}
        try:
            self.logger.info("Send 'reload' to device...")
            self.cli.send_command(command='reload',
                                  expected_str="Halt and reboot",
                                  expected_map=expected_map,
                                  timeout=3)
        except Exception as e:
            self.logger.info('Session type is \'{}\', closing session...'.format(self.session.session_type))

        if self.session.session_type.lower() != 'console':
            self._wait_for_session_restore(self.session)

    def boot_from_secondary(self):
        expected_map = {"(enter 'y' or 'n')": lambda session: session.send_line('y')}
        try:
            self.logger.info("Send 'boot system flash secondary' to device...")
            self.cli.send_command(command='boot system flash secondary', expected_map=expected_map, timeout=3)
        except Exception as e:
            self.logger.info('Session type is \'{}\', closing session...'.format(self.session.session_type))

        if self.session.session_type.lower() != 'console':
            self._wait_for_session_restore(self.session)

    def _wait_for_session_restore(self, session):
        """ Wait for restore session connection """

        self.logger.debug('Waiting session restore')
        waiting_reboot_time = time.time()
        while True:
            try:
                if time.time() - waiting_reboot_time > self._session_wait_timeout:
                    raise Exception(self.__class__.__name__,
                                    "Session doesn't closed in {} sec as expected".format(
                                        self._session_wait_timeout))
                session.send_line('')
                time.sleep(1)
            except:
                self.logger.debug('Session disconnected')
                break
        reboot_time = time.time()
        while True:
            if time.time() - reboot_time > self._session_wait_timeout:
                self.cli.destroy_threaded_session(session=session)
                raise Exception(self.__class__.__name__,
                                'Session cannot connect after {} sec.'.format(self._session_wait_timeout))
            try:
                self.logger.debug('Reconnect retry')
                session.connect(re_string=self._default_prompt)
                self.logger.debug('Session connected')
                break
            except:
                time.sleep(5)
