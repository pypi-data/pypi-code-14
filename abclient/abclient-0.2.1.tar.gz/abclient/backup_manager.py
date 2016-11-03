#    Copyright (c) 2016 Shanghai EISOO Information Technology Corp.
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


class BackupManager(object):
    '''EISOO AnyBackup Manager
    '''
    def __init__(self, http_client, **kwargs):
        self.http_client = http_client

    def get_data_source_list_from_all_clients(self, full_path, job_type):
        """Get data sources information

        This method used to get data sources information from all clients.
        First, it uses get_clients to get clients' machine_code, then get
        data sources' information from each of them.
        Then invoke get_valid_full_path to get whether a data source is
        authenticated.
        """
        # This RESTful api is used to get data sources information from a
        # given AnyBackup client which identified by machine code.
        url = '/openapi/openstack/backup/data_source'
        method = 'POST'
        clients = self.get_clients()

        data_sources = []
        for client in clients:
            machine_code = client['clientMac']
            data = {
                'clientMac': machine_code,
                'fullPath': full_path,
                'jobType': job_type
            }
            body = self.http_client.json_request(method, url,
                                                 data=data)
            data_source_list = body['data']['data_source']['datasourceList']
            for data_source in data_source_list:
                instance_name = data_source['dispPath']
                full_path = self.get_valid_full_path(machine_code,
                                                     instance_name, job_type)
                if full_path is not None:
                    data_source['is_authed'] = True
                else:
                    data_source['is_authed'] = False
            data_sources = data_sources + data_source_list
        return data_sources

    def get_data_source_list(self, machine_code, full_path, job_type):
        """Get data source information from a given Anybackup client defined
        by machine_code.
        """
        url = '/openapi/openstack/backup/data_source'
        method = 'POST'
        data = {
            'clientMac': machine_code,
            'fullPath': full_path,
            'jobType': job_type
        }
        body = self.http_client.json_request(method, url, data=data)
        data_source_list = body['data']['data_source']['datasourceList']
        data_sources = []
        for data_source in data_source_list:
            instance_name = data_source['dispPath']
            full_path = self.get_valid_full_path(machine_code,
                                                 instance_name, job_type)
            if full_path is not None:
                data_source['is_authed'] = True
            else:
                data_source['is_authed'] = False
            data_sources.append(data_source)
        return data_sources

    def get_clients(self):
        """Get AnyBackup clients information

        Return a list contain AnyBackup clients' information.
        And we remove AnyBackup console server itself from the
        list.
        """
        url = '/openapi/openstack/backup/get_clients'
        method = 'GET'
        clients = self.http_client.json_request(method, url)
        # Remove AnyBackup console server in the list
        for index, client in enumerate(clients):
            if client['clientName'] == 'localhost.Infoworks':
                clients.pop(index)
                break
        return clients

    def get_valid_full_path(self, machine_code, instance_name, job_type):
        """Get valid full path

        Return a vaild full path for a given oracle instance.
        If the given oracle instance is authenticated, this method will
        return a valid full path.
        If the given oracle instance haven't authenticated, this method
        will return None.
        We call it in get_data_source_list, to find a oracle instance is
        authenticated or not.
        """
        url = '/openapi/openstack/backup/client_mac/%(client_mac)s/instance_name/%(instance_name)s/job_type/%(job_type)s/get_valid_full_path' % {
            'client_mac': machine_code,
            'instance_name': instance_name,
            'job_type': str(job_type)
        }
        method = 'GET'
        resp = self.http_client.json_request(method, url)
        valid_full_path = resp['data']['full_path']
        return valid_full_path

    def add_instance(self, arguments, instance_name, job_type, user_name,
                     password, machine_code):
        url = '/openapi/openstack/backup/add_instance'
        method = 'POST'
        data = {
            'clientMac': machine_code,
            'jobType': job_type,
            'arguments': arguments,
            'instanceName': instance_name,
            'userName': user_name,
            'password': password
        }
        body = self.http_client.json_request(method, url,
                                             data=data)

        return body

    def create_job(self, job_name, job_adv_property, job_type, data_sources, machine_code):
        url = '/openapi/openstack/backup/job'
        method = 'POST'
        data = {
            'jobName': job_name,
            'clientMac': machine_code,
            'jobAdvPropertys': job_adv_property,
            'jobType': job_type,
            'dataSources': data_sources
        }
        body = self.http_client.json_request(method, url,
                                             data=data)

        return body

    def start_backup(self, job_name, backup_type, job_type):
        url = '/openapi/openstack/backup/job/%s/start_backup' % job_name
        method = 'POST'
        data = {'backupType': backup_type, 'jobType': job_type}
        body = self.http_client.json_request(method, url,
                                             data=data)

        return body

    def start_restore(self, job_name, gns, job_type, machine_code):
        url = '/openapi/openstack/backup/job/%s/start_restore' % job_name
        method = 'POST'
        data = {'gns': gns, 'jobType': job_type, 'clientMac': machine_code}
        body = self.http_client.json_request(method, url,
                                             data=data)

        return body

    def get_progress(self, job_name, exec_code):
        url = (
            '/openapi/openstack/backup/job/%(jobName)s/exec_code/%(execCode)s/progress'
        ) % {'jobName': job_name,
             'execCode': exec_code}
        method = 'GET'
        body = self.http_client.json_request(method, url)

        return body

    def delete_backup(self, job_name, time_point):
        url = '/openapi/openstack/backup/job/%(jobName)s/time_point/%(timePoint)s/delete_data' % {
            "jobName": job_name,
            "timePoint": time_point
        }
        method = 'DELETE'
        body = self.http_client.json_request(method, url)

        return body
