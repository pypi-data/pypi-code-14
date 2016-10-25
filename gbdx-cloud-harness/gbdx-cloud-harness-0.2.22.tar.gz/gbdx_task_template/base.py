"""
cloud-harness Task Template
"""
import json
import os

from gbdx_task_template.gbdx_task_interface import GbdxTaskInterface
from gbdx_task_template.port import LocalPortValidationError, RemotePortValidationError
from gbdx_task_template.log_settings import get_logger


class TaskTemplateError(Exception):
    pass


class TaskTemplate(GbdxTaskInterface):
    """ Base Class for custom tasks written for GBDX CLI.
    """
    task = None

    def __init__(self):
        self.__task_def_json = ''

        remote_work_path = os.environ.get('REMOTE_WORK_PATH', None)

        if remote_work_path is not None:
            self.__work_path = remote_work_path
            self.__remote_run = True
        else:
            self.__work_path = os.getcwd()
            self.__remote_run = False

        self.__src_path = None

        super(TaskTemplate, self).__init__(self.__work_path)
        self.logit = get_logger('{}'.format(__name__))
        self.logit.debug('Template Init')
        self.logit.debug("Remote Run: %s" % self.__remote_run)
        self.logit.debug("Work Path: %s" % self.__work_path)

    def finalize(self, success_or_fail, message=''):
        """
        :param success_or_fail: string that is 'success' or 'fail'
        :param message:
        """
        if not self.__remote_run:
            return json.dumps({'status': success_or_fail, 'reason': message}, indent=4)
        else:
            super(TaskTemplate, self).finalize(success_or_fail, message)

    def check_and_create_outputs(self):
        """
        Iterate through the task outputs.
        Two scenarios:
            - User is running locally, check that output folders exist.
            - User is running remotely, when docker container runs filesystem, check that output folders exist.
            - Else, do nothing.
        :return: None
        """
        if self.task is None:
            raise TaskTemplateError('A task must be initialized before running a TaskTemplate subclass.')

        for output_port in self.task.output_ports:
            # Make the dir
            if output_port.direction == 'Output' and output_port.type == 'directory':
                try:
                    is_file = output_port.is_valid_filesys(output_port.value)
                    is_remote = output_port.is_valid_s3_url(output_port.value)
                except LocalPortValidationError:
                    is_file = False
                except RemotePortValidationError:
                    is_remote = False

                if is_file and not is_remote:
                    try:
                        os.makedirs(output_port.value)
                    except OSError as e:
                        if 'File exists' not in e.strerror:
                            raise e

    def __enter__(self):

        if self.task is None:
            raise TaskTemplateError('A task must be initialized before running a TaskTemplate subclass.')

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.logit.debug('Failed, Exception: ')
            self.logit.debug(exc_type)
            self.logit.debug(exc_val)
            self.logit.debug(exc_tb)
            self.finalize('failed', str(exc_val))
        else:
            # Write output ports to ports.json
            input_ports, output_ports = self.task.ports
            for port in output_ports:
                if port.type == 'string':
                    self.set_output_string_port(port.name, port.value)

            self.logit.debug('Success: %s' % self._reason)
            self.finalize('success', self._reason)
