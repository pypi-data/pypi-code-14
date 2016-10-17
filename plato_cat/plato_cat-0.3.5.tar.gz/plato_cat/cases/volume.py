import Queue
from instance import find_proper_flavor

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


class BenchVolumes():

    def __init__(self, API, concurrent, sleep):
        result = API.conn.call('CreateNetwork', {
            'name': 'network-for-bench-volumes',
        })

        job_id = result['jobId']
        network_id = result['networkId']

        # wait network creation finish
        wait_for_job(API, job_id, sleep)

        subnet_id = API.conn.call('CreateSubnet', {
            'networkId': network_id,
            'cidr': '192.168.200.0/24',
        })['subnetId']

        instance_types = get_resource(API, 'DescribeInstanceTypes', {
            'status': ['active']
        }, 'instanceTypeSet')
        selected_instance_type = find_proper_flavor(
            instance_types, 2048, 1, 40)

        images = get_resource(API, 'DescribeImages', {
            'status': ['active'],
            'isPublic': True,
        }, 'imageSet')
        selected_image = images[0]

        # create the instance and wait for it to be done.
        result = API.conn.call('CreateInstances', {
            'name': 'instance-for-bench-volumes',
            'imageId': selected_image['imageId'],
            'instanceTypeId': selected_instance_type['instanceTypeId'],
            'subnetId': subnet_id,
            'loginMode': 'password',
            'loginPassword': 'chenjie1234',
            'count': concurrent
        })
        job_id = result['jobId']
        wait_for_job(API, job_id, sleep)

        self.instance_ids_queue = Queue.Queue()
        [self.instance_ids_queue.put(instance_id)
            for instance_id in result['instanceIds']]

    def run(self, API, sleep):
        # do a complete process:
        # step 1. create volume
        # step 2. attach volume
        # step 3. detach volume
        # step 4. delete volume
        try:
            instance_id = self.instance_ids_queue.get()

            result = API.conn.call('CreateVolumes', {
                'name': 'bench-volume-name',
                'size': 1, 'count': 1, 'volumeType': 'normal'
            })

            job_id = result['jobId']
            wait_for_job(API, job_id, sleep)

            volume_id = result['volumeIds'][0]

            # attach volume
            result = API.conn.call('AttachVolume', {
                'instanceId': instance_id,
                'volumeId': volume_id,
            })

            job_id = result['jobId']
            wait_for_job(API, job_id, sleep)

            result = API.conn.call('DetachVolumes', {
                'volumeIds': [volume_id],
                'instanceId': instance_id
            })

            job_id = result['jobId']
            wait_for_job(API, job_id, sleep)

            post_resource(API, 'DeleteVolumes', [volume_id], 'volumeIds')

            return True

        except Exception as ex:
            print ex
            return False

        finally:
            self.instance_ids_queue.put(instance_id)
