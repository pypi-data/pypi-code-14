from plato_cat.cases import wait_for_job
from plato_cat.cases import get_resource
from plato_cat.cases import wait_busy_resource
from plato_cat.cases import post_resource


def find_proper_flavor(instance_types, memory, vcpus, disk):
    for instance_type in instance_types:
        if instance_type['memory'] == memory and \
           instance_type['vcpus'] == vcpus and \
           instance_type['disk'] == disk:
            return instance_type


class InstanceCase():

    def run(self, API, sleep):
        instances = get_resource(API, 'DescribeInstances', {
            'status': ['active']
        }, 'instanceSet')

        result = API.conn.call('CreateNetwork', {
            'name': 'network-for-instance1',
        })

        job_id = result['jobId']
        network_id = result['networkId']

        # wait network creation finish
        wait_for_job(API, job_id, sleep)

        subnet_id = API.conn.call('CreateSubnet', {
            'networkId': network_id,
            'cidr': '192.168.200.0/24',
        })['subnetId']

        # set external gateway
        result = API.conn.call('SetExternalGateway', {
            'networkIds': [network_id],
        })

        instance_types = get_resource(API, 'DescribeInstanceTypes', {
            'status': ['active']
        }, 'instanceTypeSet')

        images = get_resource(API, 'DescribeImages', {
            'status': ['active'],
            'isPublic': True,
        }, 'imageSet')
        selected_image = images[0]

        # select proper instance_type & image
        selected_instance_type = find_proper_flavor(
            instance_types, 2048, 1, 40)

        if not selected_image:
            raise Exception('no proper image or proper instance_type '
                            'found to create instance')

        # create the instance and wait for it to be done.
        result = API.conn.call('CreateInstances', {
            'name': 'created-instance',
            'imageId': selected_image['imageId'],
            'instanceTypeId': selected_instance_type['instanceTypeId'],
            'subnetId': subnet_id,
            'loginMode': 'password',
            'loginPassword': 'chenjie1234',
            'count': 3
        })
        job_id = result['jobId']
        instance_ids = result['instanceIds']

        wait_for_job(API, job_id, sleep)
        # double check.
        instances = get_resource(API, 'DescribeInstances', {
            'instanceIds': instance_ids
        }, 'instanceSet')

        for i in instances:
            if i['status'] != 'active':
                raise Exception('instance (%s) creation job finished,'
                                ' but status is not [active], but [%s]'
                                % (i['instanceId'], i['status']))

        instance_id_1 = instance_ids[0]
        instance_id_2 = instance_ids[1]
        instance_id_3 = instance_ids[2]

        # stop all instances:  NO 1. NO 2. NO 3.
        result = API.conn.call('StopInstances', {
            'instanceIds': instance_ids,
        })
        job_id = result['jobId']

        wait_for_job(API, [job_id], sleep)

        # start instances  NO 1.
        result = API.conn.call('StartInstances', {
            'instanceIds': [instance_id_1],
        })
        job_id_1 = result['jobId']

        # reset instances  NO 2.
        result = API.conn.call('ResetInstances', {
            'instanceIds': [instance_id_2],
            'loginMode': 'password',
            'loginPassword': 'chenjie1234',
        })
        job_id_2 = result['jobId']

        # resize instances NO 3.
        instance_type_new = find_proper_flavor(
            instance_types, 2048, 2, 40)
        result = API.conn.call('ResizeInstances', {
            'instanceIds': [instance_id_3],
            'instanceTypeId': instance_type_new['instanceTypeId'],
        })
        job_id_3 = result['jobId']

        wait_for_job(API, [job_id_1, job_id_2, job_id_3], sleep)

        # after reset, instance may enter active status. stop it.
        double_check = get_resource(API, 'DescribeInstances', {
             'instanceIds': [instance_id_2]
        }, 'instanceSet')[0]['status']
        if double_check == 'active':
            result = API.conn.call('StopInstances', {
                'instanceIds': [instance_id_2],
            })
            job_id = result['jobId']
            wait_for_job(API, job_id, sleep)

        #
        # from here, instance NO 1 active, NO 2 stopped, NO 3 stopped.
        #

        # restart instances NO 1.
        result = API.conn.call('RestartInstances', {
            'instanceIds': [instance_id_1],
        })
        job_id_1 = result['jobId']
        # start instance NO 2 and NO 3.
        result = API.conn.call('StartInstances', {
            'instanceIds': [instance_id_2, instance_id_3],
        })
        job_id_2 = result['jobId']

        wait_for_job(API, [job_id_1, job_id_2], sleep)

        # capture instance
        result = API.conn.call('CaptureInstance', {
            'instanceId': instance_id_1,
            'name': 'test-capture-instance',
        })
        job_id = result['jobId']

        wait_for_job(API, job_id, sleep)

        # connect VNC
        result = API.conn.call('ConnectVNC', {
            'instanceId': instance_id_2,
        })
        # get instance output
        result = API.conn.call('GetInstanceOutput', {
            'instanceId': instance_id_2,
        })


class CleanInstances():

    def run(self, API, sleep):
        wait_busy_resource(API, 'DescribeInstances', {
            'status': ['pending', 'starting', 'stopping',
                       'restarting', 'scheduling']
        }, sleep)

        instances = get_resource(API, 'DescribeInstances', {
            'status': ['active', 'stopped', 'error']
        }, 'instanceSet')

        # delete instances
        instance_ids = [i['instanceId'] for i in instances]
        post_resource(API, 'DeleteInstances', instance_ids, 'instanceIds')
