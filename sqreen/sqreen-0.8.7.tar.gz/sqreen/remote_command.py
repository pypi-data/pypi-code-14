# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Execute and sanitize remote commands
"""

import logging

from .rules_callbacks import cb_from_rule


LOGGER = logging.getLogger(__name__)


class Command(object):
    """ Abstract command
    """
    pass


class InvalidCommand(Exception):
    """ An exception raised if a command is invalid.
    It can either doesn't contains a name attribute or no callback
    has been registered for this command.
    """
    pass


class RemoteCommand(object):
    """ Class responsible for dispatching and executing remote commands
    """

    def __init__(self):
        self.commands = {}

    def process_list(self, commands, *args, **kwargs):
        """ Process a list of command and assemble the result
        """
        res = {}

        if commands is None:
            return res

        if isinstance(commands, dict):
            LOGGER.debug("Wrong commands type %s: %r", type(commands), commands)
            return res

        for command in commands:
            try:
                command_uuid = command['uuid']
            except KeyError:
                LOGGER.debug("Command without uuid: %s", command)
                continue

            res[command_uuid] = self.process(command, *args, **kwargs)
        return res

    def process(self, command, *args, **kwargs):
        """ Process a single command

        Check that the command is registered first then try
        to call it with *args and **kwargs parameters
        """
        # Validate the command
        try:
            self._validate_command(command)
        except InvalidCommand as exception:
            return {'status': False, 'msg': str(exception)}

        LOGGER.debug("Processing command %s", command['name'])

        # Then execute the command
        result = self.commands[command['name']](*args, **kwargs)
        return self._format_result(result)

    def _validate_command(self, command):
        """ Check if the command name has been registered
        """
        command_name = command.get('name')
        if command_name not in self.commands:
            msg = "unknown command name '{}'".format(command_name)
            raise InvalidCommand(msg)

    @staticmethod
    def _format_result(result):
        """ Format the command result for the backend
        """
        if result is None:
            return {'status': False, 'output': 'None returned'}
        elif result is True:
            return {'status': True}
        else:
            return {'status': True, 'output': result}

    def register_command(self, command_name, command):
        """ Register a command callback for command name
        """
        self.commands[command_name] = command

    @classmethod
    def with_production_commands(cls):
        """ Returns a RemoteCommand with all production commands
        already registered
        """
        remote_command = cls()

        for command_name, command in ALL_COMMANDS.items():
            remote_command.register_command(command_name, command)

        return remote_command


###
# COMMANDS DEFINITION
###

def _load_rules(runner):
    """ Retrieve the rulespack and instantiate the callbacks, returns
    a list of callbacks
    """
    rules = runner.session.get_rulespack()

    if len(rules['rules']) == 0 or rules['pack_id'] is None:
        return None, []

    LOGGER.info("Retrieved rulespack id: %s", rules['pack_id'])
    rules_name = ", ".join(rule['name'] for rule in rules['rules'])
    LOGGER.debug("Retrieved %d rules: %s", len(rules['rules']), rules_name)

    # Create the callbacks
    callbacks = []
    for rule_dict in rules['rules']:
        # Set the pack_id on each rule
        rule_dict['rulespack_id'] = rules['pack_id']

        # Instantiate the rule callback
        callback = cb_from_rule(rule_dict, runner)

        if callback:
            LOGGER.debug('Rule "%s" will hook on "%s %s" with callback %s with strategy %s',
                         callback.rule_name, callback.hook_module,
                         callback.hook_name, callback, callback.strategy)

            callbacks.append(callback)

            # Check if the rule has some metrics to register
            for metric in rule_dict.get('metrics', []):
                runner.metrics_store.register_metric(**metric)

    return rules['pack_id'], callbacks


def _instrument_callbacks(runner, callbacks):
    """ For a given list of callbacks, hook them
    """
    LOGGER.info("Setup instrumentation")
    for callback in callbacks:
        runner.instrumentation.add_callback(callback)


def instrumentation_enable(runner):
    """ Retrieve a rulespack, instantiate RuleCallback from the rules
    and instrument them.
    """
    # Load rules
    pack_id, rules = _load_rules(runner)

    LOGGER.debug("Start instrumentation with rulespack_id %s", pack_id)

    # Clean existing callbacks to avoid double-instrumentation
    instrumentation_remove(runner)

    # Instrument retrieved rules
    _instrument_callbacks(runner, rules)

    return pack_id


def instrumentation_remove(runner):
    """ Remove all callbacks from instrumentation, return True
    """
    LOGGER.debug("Remove instrumentation")
    runner.instrumentation.deinstrument_all()
    return True


def rules_reload(runner):
    """ Load the rules, deinstrument the old ones and instrument
    the new loaded rules. Returns the new rulespack_id
    """
    LOGGER.debug("Reloading rules")
    pack_id, rules = _load_rules(runner)

    # Deinstrument
    instrumentation_remove(runner)

    # Reinstrument new ones
    _instrument_callbacks(runner, rules)

    LOGGER.debug('Rules reloaded')
    return pack_id


def features_get(runner):
    print("COMMAND: Features_get")


def features_change(runner):
    print("COMMAND: Features change")

ALL_COMMANDS = {
    "instrumentation_enable": instrumentation_enable,
    "instrumentation_remove": instrumentation_remove,
    "rules_reload": rules_reload,
    "features_get": features_get,
    "features_change": features_change
}
