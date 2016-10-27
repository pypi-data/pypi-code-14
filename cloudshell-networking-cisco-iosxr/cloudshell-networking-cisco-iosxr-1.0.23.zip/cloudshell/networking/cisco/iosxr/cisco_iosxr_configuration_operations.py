from collections import OrderedDict
import traceback
import inject
import re
import time

from cloudshell.networking.networking_utils import validateIP
from cloudshell.networking.cisco.firmware_data.cisco_firmware_data import CiscoFirmwareData
from cloudshell.networking.operations.interfaces.configuration_operations_interface import \
    ConfigurationOperationsInterface
from cloudshell.networking.operations.interfaces.firmware_operations_interface import FirmwareOperationsInterface
from cloudshell.shell.core.context_utils import get_resource_name
from cloudshell.networking.cisco.cisco_configuration_operations import CiscoConfigurationOperations


def _get_time_stamp():
    return time.strftime("%d%m%y-%H%M%S", time.localtime())

# def _is_valid_copy_filesystem(filesystem):
#     return not re.match('bootflash$|tftp$|ftp$|harddisk$|nvram$|pram$|flash$|localhost$', filesystem) is None


class CiscoIOSXRConfigurationOperations(CiscoConfigurationOperations):
    def __init__(self):
        CiscoConfigurationOperations.__init__(self)


    def save_configuration(self, destination_host, source_filename, vrf=None):
        """Backup 'running-config' from device to provided file_system [ftp|tftp]
    	Also possible to backup config to localhost
    	:param destination_host:  tftp/ftp server where file be saved
    	:param source_filename: what file to backup - we ignore the input form the user for
    	    this param because we support only running-config.
    	:return: status message / exception
    	"""

        #source_filename = 'running-config'

        if source_filename == '':
            source_filename = 'running-config'
        if '-config' not in source_filename:
            source_filename = source_filename.lower() + '-config'

        match_data = re.search('running-config', source_filename)
        if not match_data:
            raise Exception('Cisco IOS XR', "Configuration type is empty or wrong - should be running-config ")

        if destination_host == '':
            raise Exception('Cisco IOS XR', "Destination host is empty")

        system_name = re.sub('\s+', '_', get_resource_name())
        if len(system_name) > 23:
            system_name = system_name[:23]

        destination_filename = '{0}-{1}-{2}'.format(system_name, source_filename.replace('-config', ''),
                                                            _get_time_stamp())
        self.logger.info('destination filename is {0}'.format(destination_filename))

        if len(destination_host) <= 0:
            destination_host = self._get_resource_attribute(self.resource_name, 'Backup Location')
            if len(destination_host) <= 0:
                raise Exception('Folder path and Backup Location are empty')
        if destination_host.endswith('/'):
            destination_file = destination_host + destination_filename
        else:
            destination_file = destination_host + '/' + destination_filename

            # destination_file = destination_file.replace('127.0.0.1/', 'localhost/')
        is_uploaded = self.copy(destination_file=destination_file, source_file=source_filename, vrf=vrf)
        if is_uploaded[0] is True:
            self.logger.info('Save complete')
            return '{0},'.format(destination_filename)
        else:
            self.logger.info('Save failed with an error: {0}'.format(is_uploaded[1]))
            raise Exception(is_uploaded[1])

    def restore_configuration(self, source_file, config_type , restore_method='override', vrf=None):
        """Restore configuration on device from provided configuration file
    	Restore configuration from local file system or ftp/tftp server into 'running-config'.
    	:param source_file: relative path to the file on the remote host tftp://server/sourcefile
    	:param restore_method: override current config or not
    	:param config_type: 'running' we ignore the input form the user for
    	    this param because we support only running-config.
    	:return:
    	"""

        if not re.search('append|override', restore_method.lower()):
            raise Exception('Cisco IOS XR', "Restore method is wrong! Should be Append or Override")

        #config_type = 'running-config'
        if '-config' not in config_type:
            config_type = config_type.lower() + '-config'

        self.logger.info('Start restoring device configuration from {}'.format(source_file))

        match_data = re.search('running-config', config_type)
        if not match_data:
            raise Exception('Cisco IOS XR', "Configuration type is empty or wrong - should be running-config ")

        destination_filename = match_data.group()

        if source_file == '':
            raise Exception('Cisco IOS XR', "Path is empty")

        # source_file = source_file.replace('127.0.0.1/', 'localhost/')

        # incase of override - load the configuration file over running configuration
        if restore_method.lower() == 'override':
            self.load(source_file=source_file, vrf=vrf)
            is_uploaded = (True, '')

        # incase of append - add the configuration file to the existing one using copy command.
        elif restore_method.lower() == 'append':
            is_uploaded = self.copy(source_file=source_file, destination_file=destination_filename, vrf=vrf)

        if is_uploaded[0] is False:
            raise Exception('Cisco IOS XR', is_uploaded[1])

        is_downloaded = (True, '')
        if is_downloaded[0] is True:
            return 'Finished restore configuration!'
        else:
            raise Exception('Cisco IOS XR', is_downloaded[1])


    def load(self, source_file='', vrf=None, timeout=600, retries=5):
        """load configurationon running mode on device from provided configuration file
	    :param source_file: relative path to the file on the remote host tftp://server/sourcefile
		"""

        if not source_file:
            raise Exception('Cisco IOS XR', "No source filename provided for load method!")

        expected_map = OrderedDict()

        expected_map = {
            '[\[\(][Yy]es/[Nn]o[\)\]]|\[confirm\]': lambda session: session.send_line('yes'),
            '\(y\/n\)': lambda session: session.send_line('y'),
            '[\[\(][Yy]/[Nn][\)\]]': lambda session: session.send_line('y'),
            'overwritte': lambda session: session.send_line('yes'),
            'Do you wish to proceed':lambda session: session.send_line('yes')
        }

        load_command_str = 'load {0}'.format(source_file)
        if vrf:
            load_command_str += ' vrf {0}'.format(vrf)

        # we sand the config command and the command itself
        output=self.cli.send_config_command(command=load_command_str, expected_map=expected_map,timeout = 60)

        commit = 'commit replace'

        outcommit = self.cli.send_config_command(command=commit, expected_map=expected_map,timeout =60)
        # to exit the configuration mode
        self.cli.send_command(command='')

        match_error = re.search(r" Can't assign requested address|[Ee]rror:", output)

        error_match_commit = re.search(r'(ERROR|[Ee]rror).*', outcommit)


        if match_error is not None or error_match_commit is not None:
            error_str = output[match_error.end() + 1:]
            error_str = error_str[:error_str.find('\n')]
            raise Exception('Cisco IOS XR', 'load error: ' + error_str)

    def _check_download_from_tftp(self, output):
        """Verify if file was successfully uploaded
        :param output: output from cli
        :return True or False, and success or error message
        :rtype tuple
        """

        status_match_copy = re.search(r'\[OK\]', output)
        status_match_append = re.search('Updated Commit', output)

        is_success = (status_match_copy is not None) # results of regular copy
        if not is_success:
            is_success = (status_match_append is not None)  # result of append copy

        message = 'Copy failed. Please see logs for additional info'
        if not is_success:
            match_error = re.search('%', output, re.IGNORECASE)
            if match_error:
                message = output[match_error.end():]
                message = message.split('\n')[0]

        error_match = re.search(r'(ERROR|[Ee]rror).*', output)
        if error_match:
            self.logger.error(error_match.group())
            if is_success is True:
                message = 'Copy completed with an errors. Please see logs for additional info'

        return is_success, message

