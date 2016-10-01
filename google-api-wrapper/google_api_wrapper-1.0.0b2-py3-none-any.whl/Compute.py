import time
from urllib.parse import urlparse

from googleapiclient.errors import HttpError
from googleapiwrapper.Exceptions import translate_exception, ResourceNotFoundException, \
    check_operation_status


class Compute:
    def __init__(self, api):
        self._api = api

    def wait_for_global_operation(self, project: str, operation_name: str):
        while True:
            operation_status = self._api.globalOperations().get(project=project, operation=operation_name).execute()
            operation_result = check_operation_status(operation_status)
            if operation_result is not None:
                return operation_result
            else:
                time.sleep(1)

    def wait_for_region_operation(self, project: str, region: str, operation_name: str):
        while True:
            operation_status = self._api.regionOperations().get(project=project,
                                                                region=region,
                                                                operation=operation_name).execute()
            operation_result = check_operation_status(operation_status)
            if operation_result is not None:
                return operation_result
            else:
                time.sleep(1)

    def wait_for_zonal_operation(self, project: str, zone: str, operation_name: str):
        while True:
            operation_status = self._api.zoneOperations().get(project=project,
                                                              zone=zone,
                                                              operation=operation_name).execute()
            operation_result = check_operation_status(operation_status)
            if operation_result is not None:
                return operation_result
            else:
                time.sleep(1)

    def instance_exists(self, project: str, zone: str, instance: str) -> bool:
        try:
            try:
                self._api.instances().get(project=project, zone=zone, instance=instance).execute()
                return True
            except HttpError as e:
                translate_exception(e)
        except ResourceNotFoundException:
            return False

    def disk_exists(self, project: str, zone: str, disk: str) -> bool:
        try:
            try:
                self._api.disks().get(project=project, zone=zone, disk=disk).execute()
                return True
            except HttpError as e:
                translate_exception(e)
        except ResourceNotFoundException:
            return False

    def get_instance_group_members(self, project: str, zone: str, instance_group_name: str) -> list:
        try:
            result = self._api.instanceGroups().listInstances(project=project,
                                                              zone=zone,
                                                              instanceGroup=instance_group_name,
                                                              body={}).execute()
            items = []
            try:
                items = result['items']
            except KeyError:
                pass

            members = []
            for member in items:
                # noinspection PyTypeChecker
                uri = urlparse(member['instance'])
                member_name = uri.path[uri.path.rfind('/') + 1:]
                members.append(member_name)
            return members

        except HttpError as e:
            translate_exception(e)

    def add_instance_to_instance_groups(self, project: str, zone: str, instance_group: str, instance: str):
        try:
            instance_url = 'projects/%s/zones/%s/instances/%s' % (project, zone, instance)
            result = self._api.instanceGroups().addInstances(project=project,
                                                             zone=zone,
                                                             instanceGroup=instance_group,
                                                             body={
                                                                 'instances': [{'instance': instance_url}]
                                                             }).execute()
            self.wait_for_zonal_operation(project, zone, result['name'])
        except HttpError as e:
            translate_exception(e)

    def remove_instance_from_instance_group(self, project: str, zone: str, instance_group: str, instance: str):
        try:
            instance_url = 'projects/%s/zones/%s/instances/%s' % (project, zone, instance)
            result = self._api.instanceGroups().removeInstances(project=project,
                                                                zone=zone,
                                                                instanceGroup=instance_group,
                                                                body={
                                                                    'instances': [{'instance': instance_url}]
                                                                }).execute()
            self.wait_for_zonal_operation(project, zone, result['name'])
        except HttpError as e:
            translate_exception(e)

    def remove_from_instance_groups(self, project: str, zone: str, instance: str):
        try:
            instance_groups = []
            instance_groups_result = self._api.instanceGroups().list(project=project, zone=zone).execute()
            if 'items' in instance_groups_result:
                for instance_group in instance_groups_result['items']:
                    instances_result = self._api.instanceGroups().listInstances(project=project,
                                                                                zone=zone,
                                                                                instanceGroup=instance_group['name'],
                                                                                body={}).execute()
                    if 'items' in instances_result:
                        for member in instances_result['items']:
                            member_url = member['instance']
                            if member_url.endswith('/instances/' + instance):
                                self.remove_instance_from_instance_group(project, zone, instance_group['name'],
                                                                         instance)
                                instance_groups.append(instance_group['name'])
            return instance_groups
        except HttpError as e:
            translate_exception(e)

    def stop_instance(self, project: str, zone: str, instance: str):
        try:
            stop_result = self._api.instances().stop(project=project, zone=zone, instance=instance).execute()
            self.wait_for_zonal_operation(project, zone, stop_result['name'])
        except HttpError as e:
            translate_exception(e)

    def delete_instance(self, project: str, zone: str, instance: str):
        try:
            delete_result = self._api.instances().delete(project=project, zone=zone, instance=instance).execute()
            self.wait_for_zonal_operation(project, zone, delete_result['name'])
        except HttpError as e:
            translate_exception(e)

    def create_disk(self, project: str, zone: str, disk_type: str, disk_name: str, size_gb: int):
        try:
            disk_type_uri = 'projects/%s/zones/%s/diskTypes/%s' % (project, zone, disk_type)
            create_result = self._api.disks().insert(project=project,
                                                     zone=zone,
                                                     body={
                                                         'type': disk_type_uri,
                                                         'name': disk_name,
                                                         'sizeGb': size_gb
                                                     }).execute()
            self.wait_for_zonal_operation(project, zone, create_result['name'])
        except HttpError as e:
            translate_exception(e)

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
                        static_ip_address_name: str,
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

        # discover static IP address
        access_config = [
            {
                "type": "ONE_TO_ONE_NAT",
                "name": "External NAT"
            },
        ]
        if static_ip_address_name is not None:
            region = zone[0:zone.rfind('-')]
            try:
                try:
                    get_addr_result = self._api.addresses().get(project=project, region=region,
                                                                address=static_ip_address_name).execute()
                    access_config[0]['natIP'] = get_addr_result['address']
                except HttpError as e:
                    translate_exception(e)
            except ResourceNotFoundException:
                try:
                    operation = self._api.addresses().insert(project=project, region=region, body={
                        "description": "Static IP address for " + instance_name,
                        "name": static_ip_address_name
                    }).execute()
                    self.wait_for_region_operation(project, region, operation['name'])

                    get_addr_result = self._api.addresses().get(project=project, region=region,
                                                                address=static_ip_address_name).execute()
                    access_config[0]['natIP'] = get_addr_result['address']
                except HttpError as e:
                    translate_exception(e)

        try:
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
                                                                 "accessConfigs": access_config,
                                                                 'network': network_url
                                                             }
                                                         ],
                                                         'metadata': {'items': metadata_items},
                                                         'tags': {'items': tags}
                                                     }).execute()
            self.wait_for_zonal_operation(project, zone, operation['name'])
        except HttpError as e:
            translate_exception(e)
