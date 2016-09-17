import json
import time

from googleapiwrapper.Exceptions import ResourceAccessDeniedException, ResourceNotFoundException, ResourceException, \
    OperationException


class Compute:
    def __init__(self, api):
        self._api = api

    @staticmethod
    def translate_exception(e: Exception):
        if hasattr(e, "content"):
            content = json.loads(e.content.decode())
            if content['error']:
                code = content['error']['code']
                message = content['error']['message']
                if code == 404:
                    raise ResourceNotFoundException(code, message) from e
                elif code == 403:
                    raise ResourceAccessDeniedException(code, message) from e
                else:
                    raise ResourceException(code, message) from e
        raise ResourceException('-1', "Unknown error has occurred") from e

    @staticmethod
    def check_operation_status(operation_result):
        if operation_result['status'] == 'DONE':
            if 'warnings' in operation_result:
                [print('WARN -> %s: %s' % (warn['code'], warn['message'])) for warn in operation_result['warnings']]

            if 'error' in operation_result:
                error = operation_result['error']
                if 'code' in error and 'message' in error:
                    raise OperationException(error['code'], error['message'])
                elif 'errors' in error:
                    error = error['errors'][0]
                    raise OperationException(error['code'], error['message'])
                else:
                    raise OperationException('-1', 'Unknown error: ' + json.dumps(error))
            else:
                return operation_result
        else:
            return None

    def wait_for_global_operation(self, project: str, operation_name: str):
        while True:
            operation_status = self._api.globalOperations().get(project=project, operation=operation_name).execute()
            operation_result = Compute.check_operation_status(operation_status)
            if operation_result is not None:
                return operation_result
            else:
                time.sleep(1)

    def instance_exists(self, project: str, zone: str, instance: str):
        try:
            self._api.instances().get(project=project, zone=zone, instance=instance).execute()
            return True
        except Exception as e:
            self.translate_exception(e)

    def disk_exists(self, project: str, zone: str, disk: str):
        try:
            self._api.disks().get(project=project, zone=zone, disk=disk).execute()
            return True
        except Exception as e:
            self.translate_exception(e)

    def add_instance_to_instance_groups(self, project: str, zone: str, instance_group: str, instance: str):
        result = self._api.instanceGroups().addInstances(project=project,
                                                         zone=zone,
                                                         instanceGroup=instance_group,
                                                         body={
                                                             'instances': [
                                                                 'projects/%s/zones/%s/instances/%s' % (
                                                                     project, zone, instance)
                                                             ]
                                                         }).execute()
        self.wait_for_global_operation(project, result['name'])

    def remove_instance_from_instance_group(self, project: str, zone: str, instance_group: str, instance: str):
        result = self._api.instanceGroups().removeInstances(project=project,
                                                            zone=zone,
                                                            instanceGroup=instance_group,
                                                            body={
                                                                'instances': [
                                                                    'projects/%s/zones/%s/instances/%s' % (
                                                                        project, zone, instance)
                                                                ]
                                                            }).execute()
        self.wait_for_global_operation(project, result['name'])

    def remove_from_instance_groups(self, project: str, zone: str, instance: str):
        instance_groups = []

        instance_groups_result = self._api.instanceGroups().list(project=project, zone=zone).execute()
        if 'items' in instance_groups_result:
            for instance_group in instance_groups_result['items']:
                instances_result = self._api.instanceGroups().listInstances(project=project,
                                                                            zone=zone,
                                                                            instanceGroup=instance_group['name'],
                                                                            body={},
                                                                            filter='name=' + instance).execute()
                if 'items' in instances_result:
                    for member in instances_result['items']:
                        member_url = member['instance']
                        if member_url.endswith('/instances/' + instance):
                            self.remove_instance_from_instance_group(project, zone, instance_group['name'], instance)
                            instance_groups.append(instances_result['name'])

        return instance_groups

    def stop_instance(self, project: str, zone: str, instance: str):
        stop_result = self._api.instances().stop(project=project, zone=zone, instance=instance).execute()
        self.wait_for_global_operation(project, stop_result['name'])

    def delete_instance(self, project: str, zone: str, instance: str):
        delete_result = self._api.instances().delete(project=project, zone=zone, instance=instance).execute()
        self.wait_for_global_operation(project, delete_result['name'])

    def create_disk(self, project: str, zone: str, disk_type: str, disk_name: str, size_gb: int):
        disk_type_uri = 'projects/%s/zones/%s/diskTypes/%s' % (project, zone, disk_type)
        create_result = self._api.disks().insert(project=project,
                                                 zone=zone,
                                                 body={
                                                     'type': disk_type_uri,
                                                     'name': disk_name,
                                                     'sizeGb': size_gb
                                                 }).execute()
        self.wait_for_global_operation(project, create_result['name'])

    def create_instance(self,
                        project: str,
                        zone: str,
                        instance_name: str,
                        service_account_email: str,
                        service_account_scopes: str,
                        boot_disk_image_name: str,
                        boot_disk_type: str,
                        boot_disk_size: int,
                        data_disk_name: str,
                        machine_type: str,
                        network: str,
                        startup_script_path: str,
                        tags: list):
        #
        # if using a built-in image, this is an example URI for the CentOS image:
        # boot_disk_image_uri = 'projects/centos-cloud/global/images/centos-7-v20160803'
        #

        # augment names into URLs
        network_url = 'projects/%s/global/networks/%s' % (project, network)
        boot_disk_image_uri = 'projects/%s/global/images/%s' % (project, boot_disk_image_name)
        boot_disk_type_uri = 'projects/%s/zones/%s/diskTypes/%s' % (project, zone, boot_disk_type)
        machine_type_uri = 'projects/%s/zones/%s/machineTypes/%s' % (project, zone, machine_type)

        # create disks list
        disks = [
            {
                'deviceName': instance_name + '-boot',
                'initializeParams': {
                    'diskSizeGb': boot_disk_size,
                    'diskName': instance_name + '-boot',
                    'sourceImage': boot_disk_image_uri,
                    'diskType': boot_disk_type_uri
                },
                'autoDelete': True,
                'index': 0,
                'boot': True,
                'mode': 'READ_WRITE',
                'type': 'PERSISTENT'
            }
        ]
        if data_disk_name is not None:
            disks.append(
                {
                    'deviceName': data_disk_name,
                    'autoDelete': False,
                    'boot': False,
                    'mode': 'READ_WRITE',
                    'type': 'PERSISTENT',
                    'source': 'projects/%s/zones/%s/disks/%s' % (project, zone, data_disk_name)
                }
            )

        # build instance metadata
        metadata_items = []
        if startup_script_path is not None:
            startup_script_file = open(startup_script_path, 'r')
            try:
                metadata_items.append({
                    'key': 'startup-script',
                    'value': startup_script_file.read()
                })
            finally:
                startup_script_file.close()

        # TODO: support attaching static external IP address
        operation = self._api.instances().insert(project=project,
                                                 zone=zone,
                                                 body={
                                                     'disks': disks,
                                                     'name': instance_name,
                                                     'scheduling': {
                                                         'automaticRestart': True,
                                                         'preemptible': False,
                                                         'onHostMaintenance': 'MIGRATE'
                                                     },
                                                     'machineType': machine_type_uri,
                                                     'serviceAccounts': [
                                                         {
                                                             'scopes': service_account_scopes,
                                                             'email': service_account_email
                                                         }
                                                     ],
                                                     'networkInterfaces': [
                                                         {
                                                             "accessConfigs": [
                                                                 {
                                                                     "type": "ONE_TO_ONE_NAT",
                                                                     "name": "External NAT"
                                                                 },
                                                             ],
                                                             'network': network
                                                         }
                                                     ],
                                                     'metadata': {'items': metadata_items},
                                                     'tags': {'items': tags}
                                                 }).execute()
        self.wait_for_global_operation(project, operation['name'])
