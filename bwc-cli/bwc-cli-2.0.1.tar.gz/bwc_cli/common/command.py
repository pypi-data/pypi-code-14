# Licensed to the Brocade, Inc. ('Brocade') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import abc
import ast
import json
import logging
import os
import sys
import time
from functools import wraps
from os.path import join as pjoin

import six
from cliff import command
from cliff import lister
from cliff import show

from st2client import models
from bwc_cli.common import resource

# A list of environment variables which are never inherited when using run
# --inherit-env flag
ENV_VARS_BLACKLIST = [
    'pwd',
    'mail',
    'username',
    'user',
    'path',
    'home',
    'ps1',
    'shell',
    'pythonpath',
    'ssh_tty',
    'ssh_connection',
    'lang',
    'ls_colors',
    'logname',
    'oldpwd',
    'term',
    'xdg_session_id'
]

LIVEACTION_STATUS_REQUESTED = 'requested'
LIVEACTION_STATUS_SCHEDULED = 'scheduled'
LIVEACTION_STATUS_DELAYED = 'delayed'
LIVEACTION_STATUS_RUNNING = 'running'
LIVEACTION_STATUS_SUCCEEDED = 'succeeded'
LIVEACTION_STATUS_FAILED = 'failed'
LIVEACTION_STATUS_TIMED_OUT = 'timeout'
LIVEACTION_STATUS_ABANDONED = 'abandoned'
LIVEACTION_STATUS_CANCELING = 'canceling'
LIVEACTION_STATUS_CANCELED = 'canceled'


LIVEACTION_COMPLETED_STATES = [
    LIVEACTION_STATUS_SUCCEEDED,
    LIVEACTION_STATUS_FAILED,
    LIVEACTION_STATUS_TIMED_OUT,
    LIVEACTION_STATUS_CANCELED,
    LIVEACTION_STATUS_ABANDONED
]

# Who parameters should be masked when displaying action execution output
PARAMETERS_TO_MASK = [
    'password',
    'private_key'
]


def format_parameters(value):
    # Mask sensitive parameters
    if not isinstance(value, dict):
        # No parameters, leave it as it is
        return value

    for param_name, _ in value.items():
        if param_name in PARAMETERS_TO_MASK:
            value[param_name] = '********'

    return value


def add_auth_token_to_kwargs_from_cli(func):
    @wraps(func)
    def decorate(*args, **kwargs):
        ns = args[1]
        if getattr(ns, 'token', None):
            kwargs['token'] = ns.token
        if getattr(ns, 'api_key', None):
            kwargs['api_key'] = ns.api_key
        return func(*args, **kwargs)
    return decorate


# This will be the base class for all the action runs (since all we do for the BWC cli is action
#  runs) All the pre-requisites needed to run the actions will be here.
class CommandMeta(abc.ABCMeta):

    def __new__(mcs, name, bases, cls_dict):
        if 'log' not in cls_dict:
            cls_dict['log'] = logging.getLogger(
                cls_dict['__module__'] + '.' + name)
        return super(CommandMeta, mcs).__new__(mcs, name, bases, cls_dict)


@six.add_metaclass(CommandMeta)
class Command(command.Command):
    # Every subclass will have to specify a ref_or_id which matches the action ref
    ref_or_id = None

    def __init__(self, app, app_args, cmd_name=None):
        super(Command, self).__init__(app, app_args, cmd_name)
        self.app = app
        self.app_args = app_args

    def run(self, parsed_args):
        parameters = []
        for arg in vars(parsed_args):
            if getattr(parsed_args, arg) is not None:
                value_str = str(getattr(parsed_args, arg))
                if '=' in value_str:
                    param = value_str
                else:
                    param = arg + '=' + str(getattr(parsed_args, arg))
                parameters.append(param)
        parsed_args.parameters = parameters
        parsed_args.ref_or_id = self.ref_or_id
        parsed_args.token = self.app.client.token
        parsed_args.json = True
        parsed_args.debug = False
        parsed_args.async = False
        parsed_args.user = None

        action_run = ActionRunCommand(
            models.Action, self.app, parsed_args)
        execution = action_run.run(self.app_args, parsed_args)
        # Tried adding this to the .pylintrc file but couldnt make it work. Hence adding it here.
        # pylint: disable=no-member
        setattr(parsed_args, 'execution_id', execution.id)
        setattr(parsed_args, 'execution_status', execution.status)

        if execution.status == 'failed':
            print('Operation failed:')
            self.print_error_for_failed_execution(execution=execution)
            self.print_failed_execution_details(execution.id)
            sys.exit(1)
        else:
            setattr(parsed_args, 'result', execution.result)
            return super(Command, self).run(parsed_args)

    @staticmethod
    def print_error_for_failed_execution(execution):
        # TODO: Improve error parsing in Python runner
        stdout = execution.result.get('stdout', None)
        stderr = execution.result.get('stderr', None)
        print('Failure Reason: %s' % (stdout or stderr))

    @staticmethod
    def print_failed_execution_details(executionId):
        print('Please run \'st2 execution get %s\' to get details of failure' % executionId)

    @staticmethod
    def print_get_details(executionId):
        print('Please run \'st2 execution get %s\' to get details of this command anytime' %
              executionId)

    @staticmethod
    def print_get_history():
        print('Please run \'st2 execution list\' to get history of all the past executions, '
              'then to get details about a specific execution run the command \'st2 execution '
              'get '
              '<execution_id>\'')


class Lister(Command, lister.Lister):
    pass


class ShowOne(Command, show.ShowOne):
    pass


class ActionRunCommandMixin(object):
    """
    Mixin class which contains utility functions related to action execution.
    """
    poll_interval = 2  # how often to poll for execution completion when using sync mode

    def get_resource(self, ref_or_id, **kwargs):
        return self.get_resource_by_ref_or_id(ref_or_id=ref_or_id, **kwargs)

    def _get_execution_result(self, execution, action_exec_mgr, args, **kwargs):
        pending_statuses = [
            LIVEACTION_STATUS_REQUESTED,
            LIVEACTION_STATUS_SCHEDULED,
            LIVEACTION_STATUS_RUNNING,
            LIVEACTION_STATUS_CANCELING
        ]

        if not args.async:
            while execution.status in pending_statuses:
                time.sleep(self.poll_interval)
                if not args.json and not args.yaml:
                    sys.stdout.write('.')
                    sys.stdout.flush()
                execution = action_exec_mgr.get_by_id(execution.id, **kwargs)

            sys.stdout.write('\n')

            if execution.status == LIVEACTION_STATUS_CANCELED:
                return execution

        return execution

    def _get_action_parameters_from_args(self, action, runner, args):
        """
        Build a dictionary with parameters which will be passed to the action by
        parsing parameters passed to the CLI.

        :param args: CLI argument.
        :type args: ``object``

        :rtype: ``dict``
        """
        action_ref_or_id = action.ref

        def read_file(file_path):
            if not os.path.exists(file_path):
                raise ValueError('File "%s" doesn\'t exist' % (file_path))

            if not os.path.isfile(file_path):
                raise ValueError('"%s" is not a file' % (file_path))

            with open(file_path, 'rb') as fp:
                content = fp.read()

            return content

        def transform_object(value):
            # Also support simple key1=val1,key2=val2 syntax
            if value.startswith('{'):
                # Assume it's JSON
                result = value = json.loads(value)
            else:
                pairs = value.split(',')

                result = {}
                for pair in pairs:
                    split = pair.split('=', 1)

                    if len(split) != 2:
                        continue

                    key, value = split
                    result[key] = value
            return result

        transformer = {
            'array': (lambda cs_x: [v.strip() for v in cs_x.split(',')]),
            'boolean': (lambda x: ast.literal_eval(x.capitalize())),
            'integer': int,
            'number': float,
            'object': transform_object,
            'string': str
        }

        def normalize(name, value):
            if name in runner.runner_parameters:
                param = runner.runner_parameters[name]
                if 'type' in param and param['type'] in transformer:
                    return transformer[param['type']](value)

            if name in action.parameters:
                param = action.parameters[name]
                if 'type' in param and param['type'] in transformer:
                    return transformer[param['type']](value)
            return None

        result = {}
        if not args.parameters:
            return result

        for idx in range(len(args.parameters)):
            arg = args.parameters[idx]
            if '=' in arg:
                k, v = arg.split('=', 1)

                # Attribute for files are prefixed with "@"
                if k.startswith('@'):
                    k = k[1:]
                    is_file = True
                else:
                    is_file = False

                try:
                    if is_file:
                        # Files are handled a bit differently since we ship the content
                        # over the wire
                        file_path = os.path.normpath(pjoin(os.getcwd(), v))
                        file_name = os.path.basename(file_path)
                        content = read_file(file_path=file_path)

                        if action_ref_or_id == 'core.http':
                            # Special case for http runner
                            result['_file_name'] = file_name
                            result['file_content'] = content
                        else:
                            result[k] = content
                    else:
                        normalized_value = normalize(k, v)
                        if normalized_value is not None:
                            result[k] = normalized_value
                except Exception as e:
                    # TODO: Move transformers in a separate module and handle
                    # exceptions there
                    if 'malformed string' in str(e):
                        message = ('Invalid value for boolean parameter. '
                                   'Valid values are: true, false')
                        raise ValueError(message)
                    else:
                        raise e
            else:
                result['cmd'] = ' '.join(args.parameters[idx:])
                break

        # Special case for http runner
        if 'file_content' in result:
            if 'method' not in result:
                # Default to POST if a method is not provided
                result['method'] = 'POST'

            if 'file_name' not in result:
                # File name not provided, use default file name
                result['file_name'] = result['_file_name']

            del result['_file_name']

        return result

    @staticmethod
    def _get_inherited_env_vars(self):
        env_vars = os.environ.copy()

        for var_name in ENV_VARS_BLACKLIST:
            if var_name.lower() in env_vars:
                del env_vars[var_name.lower()]
            if var_name.upper() in env_vars:
                del env_vars[var_name.upper()]

        return env_vars


class ActionRunCommand(ActionRunCommandMixin, resource.ResourceCommand):
    def __init__(self, resource, app, parsed_args, **kwargs):
        super(ActionRunCommand, self).__init__(
            resource, app,
            parsed_args, **kwargs)
        self.app = app

    @add_auth_token_to_kwargs_from_cli
    def run(self, app_args, parsed_args, **kwargs):
        if not parsed_args.ref_or_id:
            raise ValueError('Missing action reference or id')

        action = self.get_resource(parsed_args.ref_or_id, **kwargs)
        if not action:
            raise resource.ResourceNotFoundError('Action "%s" cannot be found.'
                                                 % (parsed_args.ref_or_id))
        runner_mgr = self.app.client.managers['RunnerType']
        runner = runner_mgr.get_by_name(action.runner_type, **kwargs)
        if not runner:
            raise resource.ResourceNotFoundError('Runner type "%s" for action "%s" cannot be found.'
                                                 % (action.runner_type, action.name))

        action_ref = '.'.join([action.pack, action.name])
        action_parameters = self._get_action_parameters_from_args(action=action, runner=runner,
                                                                  args=parsed_args)
        execution = models.LiveAction()
        execution.action = action_ref
        execution.parameters = action_parameters
        execution.user = parsed_args.user
        action_exec_mgr = self.app.client.managers['LiveAction']

        execution = action_exec_mgr.create(execution, **kwargs)

        execution = self._get_execution_result(execution=execution,
                                               action_exec_mgr=action_exec_mgr,
                                               args=parsed_args, **kwargs)
        return execution

    def take_action(self, parsed_args):
        pass
