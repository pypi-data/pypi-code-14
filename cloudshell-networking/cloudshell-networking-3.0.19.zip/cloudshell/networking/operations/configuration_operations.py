import datetime
import jsonpickle

from abc import abstractmethod
import re

from posixpath import join

from cloudshell.networking.core.json_request_helper import JsonRequestDeserializer
from cloudshell.networking.networking_utils import UrlParser
from cloudshell.networking.operations.interfaces.configuration_operations_interface import \
    ConfigurationOperationsInterface
from cloudshell.shell.core.context_utils import get_attribute_by_name, decrypt_password
from cloudshell.shell.core.interfaces.save_restore import OrchestrationSaveResult, OrchestrationSavedArtifactInfo, \
    OrchestrationSavedArtifact, OrchestrationRestoreRules


def _get_snapshot_time_stamp():
    return datetime.datetime.now()


def set_command_result(result, unpicklable=False):
    """Serializes output as JSON and writes it to console output wrapped with special prefix and suffix

    :param result: Result to return
    :param unpicklable: If True adds JSON can be deserialized as real object.
                        When False will be deserialized as dictionary
    """

    json = jsonpickle.encode(result, unpicklable=unpicklable)
    result_for_output = str(json)
    return result_for_output


class ConfigurationOperations(ConfigurationOperationsInterface):
    REQUIRED_SAVE_ATTRIBUTES_LIST = ['resource_name', ('saved_artifact', 'identifier'),
                                     ('saved_artifact', 'artifact_type'), ('restore_rules', 'requires_same_resource')]

    AUTHORIZATION_REQUIRED_STORAGES = ['ftp', 'sftp', 'scp']

    @property
    @abstractmethod
    def logger(self):
        pass

    @property
    @abstractmethod
    def resource_name(self):
        pass

    @property
    @abstractmethod
    def api(self):
        pass

    def orchestration_save(self, mode="shallow", custom_params=None):
        """Orchestration Save command

        :param mode:
        :param custom_params: json with all required action to configure or remove vlans from certain port
        :return Serialized DriverResponseRoot to json
        :rtype json
        """

        save_params = {'folder_path': '', 'configuration_type': 'running'}
        params = dict()
        if custom_params:
            params = jsonpickle.decode(custom_params)

        save_params.update(params.get('custom_params', {}))

        if save_params['folder_path'] and not save_params['folder_path'].endswith('/'):
            save_params['folder_path'] += '/'

        save_params['folder_path'] = self.get_path(save_params['folder_path'])

        url = UrlParser.parse_url(save_params['folder_path'])
        artifact_type = url[UrlParser.SCHEME].lower()

        self.logger.info('Start saving configuration')

        host = save_params['folder_path'].replace('{}:'.format(artifact_type), '')

        identifier = join(host, self.save(**save_params).strip(','))

        saved_artifact = OrchestrationSavedArtifact(identifier=identifier, artifact_type=artifact_type)

        saved_artifact_info = OrchestrationSavedArtifactInfo(resource_name=self.resource_name,
                                                             created_date=_get_snapshot_time_stamp(),
                                                             restore_rules=self.get_restore_rules(),
                                                             saved_artifact=saved_artifact)
        save_response = OrchestrationSaveResult(saved_artifacts_info=saved_artifact_info)
        self._validate_artifact_info(saved_artifact_info)

        return set_command_result(save_response)

    def get_path(self, path=''):
        if not path:
            host = get_attribute_by_name('Backup Location')
            if ':' not in host:
                scheme = get_attribute_by_name('Backup Type')
                scheme = re.sub('(:|/+).*$', '', scheme, re.DOTALL)
                host = re.sub('^/+', '', host)
                host = '{}://{}'.format(scheme, host)
            path = host

        url = UrlParser.parse_url(path)
        if UrlParser.SCHEME not in url or not url[UrlParser.SCHEME]:
            raise Exception('ConfigurationOperations', "Backup Type is wrong or empty")

        if url[UrlParser.SCHEME].lower() in self.AUTHORIZATION_REQUIRED_STORAGES:
            if UrlParser.USERNAME not in url or not url[UrlParser.USERNAME]:
                url[UrlParser.USERNAME] = get_attribute_by_name('Backup User')
            if UrlParser.PASSWORD not in url or not url[UrlParser.PASSWORD]:
                url[UrlParser.PASSWORD] = decrypt_password(get_attribute_by_name('Backup Password'))
        try:
            result = UrlParser.build_url(url)
        except Exception as e:
            self.logger.error('Failed to build url: {}'.format(e))
            raise Exception('ConfigurationOperations', 'Failed to build path url to remote host')
        return result

    def orchestration_restore(self, saved_artifact_info, custom_params=None):
        """Orchestration restore

        :param saved_artifact_info: json with all required data to restore configuration on the device
        :param custom_params: custom parameters
        :return Serialized DriverResponseRoot to json
        :rtype json
        """

        restore_params = {'configuration_type': 'running'}

        if saved_artifact_info is None or saved_artifact_info == '':
            raise Exception('ConfigurationOperations', 'saved_artifact_info is None or empty')

        saved_artifact_info = JsonRequestDeserializer(jsonpickle.decode(saved_artifact_info))
        if not hasattr(saved_artifact_info, 'saved_artifacts_info'):
            raise Exception('ConfigurationOperations', 'Saved_artifacts_info is missing')
        saved_config = saved_artifact_info.saved_artifacts_info
        params = None
        if custom_params:
            params = JsonRequestDeserializer(jsonpickle.decode(custom_params))
            self._validate_custom_params(params)

        self._validate_artifact_info(saved_config)

        if saved_config.restore_rules.requires_same_resource \
                and saved_config.resource_name.lower() != self.resource_name.lower():
            raise Exception('ConfigurationOperations', 'Incompatible resource, expected {}'.format(self.resource_name))

        url = self.get_path('{}:{}'.format(saved_config.saved_artifact.artifact_type,
                                           saved_config.saved_artifact.identifier))

        restore_params['restore_method'] = 'override'
        restore_params['configuration_type'] = 'running'
        restore_params['vrf_management_name'] = None

        if hasattr(params, 'custom_params'):
            if hasattr(params.custom_params, 'restore_method'):
                restore_params['restore_method'] = params.custom_params.restore_method

            if hasattr(params.custom_params, 'configuration_type'):
                restore_params['configuration_type'] = params.custom_params.configuration_type

            if hasattr(params.custom_params, 'vrf_management_name'):
                restore_params['vrf_management_name'] = params.custom_params.vrf_management_name

        if UrlParser.FILENAME in url and url[UrlParser.FILENAME] and 'startup' in url[UrlParser.FILENAME]:
            restore_params['configuration_type'] = 'startup'

        if 'vrf_management_name' not in restore_params:
            restore_params['vrf_management_name'] = self._get_resource_attribute(self.resource_name,
                                                                                 'VRF Management Name')
        restore_params['path'] = url

        self.restore(**restore_params)

    def _validate_artifact_info(self, saved_config):
        """Validate action from the request json, according to APPLY_CONNECTIVITY_CHANGES_ACTION_REQUIRED_ATTRIBUTE_LIST

        """
        is_fail = False
        fail_attribute = ''
        for class_attribute in self.REQUIRED_SAVE_ATTRIBUTES_LIST:
            if type(class_attribute) is tuple:
                if not hasattr(saved_config, class_attribute[0]):
                    is_fail = True
                    fail_attribute = class_attribute[0]
                if not hasattr(getattr(saved_config, class_attribute[0]), class_attribute[1]):
                    is_fail = True
                    fail_attribute = class_attribute[1]
            else:
                if not hasattr(saved_config, class_attribute):
                    is_fail = True
                    fail_attribute = class_attribute

        if is_fail:
            raise Exception('ConfigurationOperations',
                            'Mandatory field {0} is missing in Saved Artifact Info request json'.format(
                                fail_attribute))

    def _validate_custom_params(self, custom_params):
        if not hasattr(custom_params, 'custom_params'):
            raise Exception('ConfigurationOperations', 'custom_params attribute is empty')

    def get_restore_rules(self):
        return OrchestrationRestoreRules(True)

    def _get_resource_attribute(self, resource_name, attribute_name):
        """Get resource attribute by provided attribute_name

        :param resource_name: resource name or full name
        :param attribute_name: name of the attribute
        :return: attribute value
        :rtype: string
        """

        try:
            result = self.api.GetAttributeValue(resource_name, attribute_name).Value
        except Exception as e:
            raise Exception(e.message)
        return result

    @abstractmethod
    def save(self, folder_path, configuration_type, vrf_management_name=None):
        pass

    @abstractmethod
    def restore(self, path, configuration_type, restore_method, vrf_management_name=None):
        pass
