from plato_cat.cases import wait_for_job
from plato_cat.cases import get_resource
from plato_cat.cases import wait_busy_resource
from plato_cat.cases import post_resource


class VolumeCase():

    def run(self, API, sleep):
        result = API.conn.call('CreateVolumes', {
            'size': 1,
            'name': 'create-volume-name',
            'volumeType': 'normal',
            'count': 2
        })

        job_id = result['jobId']
        wait_for_job(API, job_id, sleep)

        volume_ids = result['volumeIds']
        volumes = get_resource(API, 'DescribeVolumes', {
            'status': ['active'],
            'volumeIds': volume_ids
        }, 'volumeSet')

        for v in volumes:
            if v['status'] != 'active':
                raise Exception('volume (%s) creation job finished,'
                                ' but status is not [active], but [%s]'
                                % (v['volumeId'], v['status']))

        instances = get_resource(API, 'DescribeInstances', {
            'status': ['active', 'stopped', 'error']
        }, 'instanceSet')
        instance_ids = [i['instanceId'] for i in instances]

        # attach volume
        result = API.conn.call('AttachVolume', {
            'instanceId': instance_ids[0],
            'volumeId': volume_ids[0],
        })

        job_id = result['jobId']
        wait_for_job(API, job_id, sleep)

        # extend volumes
        result = API.conn.call('ExtendVolumes', {
            'volumeIds': [volume_ids[1]],
            'size': 2,
        })

        job_id = result['jobId']
        wait_for_job(API, job_id, sleep)


class CleanVolumes():

    def run(self, API, sleep):
        wait_busy_resource(API, 'DescribeVolumes', {
            'status': ['pending', 'attaching', 'detaching',
                       'backup_ing', 'backup_restoring'],
        }, sleep)

        volumes = get_resource(API, 'DescribeVolumes', {
            'status': ['active', 'inuse', 'error']
        }, 'volumeSet')

        # detach volumes
        job_ids = []
        for volume in volumes:
            if volume['instanceId']:
                result = API.conn.call('DetachVolumes', {
                    'volumeIds': [volume['volumeId']],
                    'instanceId': volume['instanceId']
                })

                job_ids.append(result['jobId'])

        wait_for_job(API, job_ids, sleep)

        volume_ids = [v['volumeId'] for v in volumes]
        post_resource(API, 'DeleteVolumes', volume_ids, 'volumeIds')
