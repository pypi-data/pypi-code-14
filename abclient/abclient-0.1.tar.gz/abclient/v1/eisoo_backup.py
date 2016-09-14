class eisooBackupManager(object):
    def __init__(self, http_client):
        self.client = http_client
        #self.client_mac = '1RR70L2V983CVPGG'
        #self.client_mac = '00505687F535'
        self.client_mac = 'S44T3XGLH8LIN03T'

    def get_data_source_list(self, full_path, job_type):
        url = '/openapi/hw/backup/data_source'
        data = {
            'clientMac': self.client_mac,
            'fullPath': full_path,
            'jobType': job_type
        }

        # TODO (response handling)
        result = self.client.json_request('POST', url, data=data)

        return result

    def add_instance(self, arguments, instance_name, job_type, user_name,
                     password):
        #url = '/openapi/hw/smaug_backup/add_instance'
        url = "/openapi/hw/backup/add_instance"

        data = {
            'clientMac': self.client_mac,
            'jobType': job_type,
            'arguments': arguments,
            'instanceName': instance_name,
            'userName': user_name,
            'password': password
        }
        # TODO (response handling)
        body = self.client.json_request('POST', url, data=data)

        return body

    def create_job(self, job_name, job_adv_property, job_type, data_sources):
        url = '/openapi/hw/backup/job'

        data = {
            'jobName': job_name,
            'clientMac': self.client_mac,
            'jobAdvPropertys': job_adv_property,
            'jobType': job_type,
            'dataSources': data_sources
        }

        # TODO (response handling)
        body = self.client.json_request('POST', url, data=data)

        return body

    def start_backup(self, job_name, backup_type, job_type):

        url = '/openapi/hw/backup/job/%s/start_backup' % job_name
        data = {'backupType': backup_type, 'jobType': job_type}

        #TODO (response handling)
        body = self.client.json_request('POST', url, data=data)

        return body

    def start_restore(self, job_name, gns, job_type):
        '''There is some differences between Interfaces Document and
        unit test about how to use 'start_restore' interface.
            I just implement it according to the unit test source code.
        '''

        url = '/openapi/hw/backup/job/%s/start_restore' % job_name
        data = {'gns': gns, 'jobType': job_type, 'clientMac': self.client_mac}

        # TODO (response handling)
        body = self.client.json_request('POST', url, data=data)

        return body

    def delete_backup(self, job_name, time_point):
        url = '/openapi/hw/backup/job/%(jobName)s/time_point/%(timePoint)s/delete_data' % {
            "jobName": job_name,
            "timePoint": time_point
        }
        body = self.client.json_request('DELETE', url)
        return body

    def get_progress(self, job_name, exec_code):
        url = (
            '/openapi/hw/backup/job/%(jobName)s/exec_code/%(execCode)s/progress'
        ) % {'jobName': job_name,
             'execCode': exec_code}
        # TODO (response handling)
        body = self.client.json_request('GET', url)

        return body

    def delete_backup_by_timepoint(self, job_name, time_point):
        url = '/openapi/openstack/smaug_backup/job/%(jobName)s/time_point/%(timePoint)s/data' % {
            'jobName': job_name,
            'timePoint': time_point
        }

        # TODO (response handling)
        body = self.client.json_request('GET', url)

        return body
