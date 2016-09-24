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

from abclient import http


class eisooBackupManager(object):
    def __init__(self, endpoint, machine_code, **kwargs):
        self.http_client = self._construct_http_client(endpoint)
        self._client_mac = machine_code

    def _construct_http_client(self, endpoint):
        return http.HTTPClient(endpoint)

    def get_data_source_list(self, full_path, job_type):
        url = '/openapi/hw/backup/data_source'
        data = {
            'clientMac': self._client_mac,
            'fullPath': full_path,
            'jobType': job_type
        }

        body = self.http_client.json_request('POST', url, data=data)

        return body

    def add_instance(self, arguments, instance_name, job_type, user_name,
                     password):
        url = "/openapi/hw/backup/add_instance"
        data = {
            'clientMac': self._client_mac,
            'jobType': job_type,
            'arguments': arguments,
            'instanceName': instance_name,
            'userName': user_name,
            'password': password
        }

        body = self.http_client.json_request('POST', url, data=data)

        return body

    def create_job(self, job_name, job_adv_property, job_type, data_sources):
        url = '/openapi/hw/backup/job'
        data = {
            'jobName': job_name,
            'clientMac': self._client_mac,
            'jobAdvPropertys': job_adv_property,
            'jobType': job_type,
            'dataSources': data_sources
        }

        body = self.http_client.json_request('POST', url, data=data)

        return body

    def start_backup(self, job_name, backup_type, job_type):
        url = '/openapi/hw/backup/job/%s/start_backup' % job_name
        data = {'backupType': backup_type, 'jobType': job_type}

        body = self.http_client.json_request('POST', url, data=data)

        return body

    def start_restore(self, job_name, gns, job_type):
        url = '/openapi/hw/backup/job/%s/start_restore' % job_name
        data = {'gns': gns, 'jobType': job_type, 'clientMac': self._client_mac}

        body = self.http_client.json_request('POST', url, data=data)

        return body

    def delete_backup(self, job_name, time_point):
        url = '/openapi/hw/backup/job/%(jobName)s/time_point/%(timePoint)s/delete_data' % {
            "jobName": job_name,
            "timePoint": time_point
        }

        body = self.http_client.json_request('DELETE', url)
 
        return body

    def get_progress(self, job_name, exec_code):
        url = (
            '/openapi/hw/backup/job/%(jobName)s/exec_code/%(execCode)s/progress'
        ) % {'jobName': job_name,
             'execCode': exec_code}

        body = self.http_client.json_request('GET', url)

        return body

    def delete_backup_by_timepoint(self, job_name, time_point):
        url = '/openapi/openstack/smaug_backup/job/%(jobName)s/time_point/%(timePoint)s/data' % {
            'jobName': job_name,
            'timePoint': time_point
        }

        body = self.http_client.json_request('GET', url)

        return body
