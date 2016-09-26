from plato_cat.cases import wait_for_job
from plato_cat.cases import get_resource
from plato_cat.cases import wait_busy_resource
from plato_cat.cases import post_resource


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

        # select proper instance_type & image
        selected_image = None
        selected_instance_type = None
        found = False
        for image in images:
            # pass non linux platorm
            # if not image['platform'] != 'linux':
            #     continue

            min_vcpus = image['minVcpus']
            min_memory = image['minMemory']
            min_disk = image['minDisk']
            min_size = image['size'] >> 30

            for instance_type in instance_types:
                # pass high flavor
                if (instance_type['memory'] >= 8192 or
                   instance_type['vcpus'] >= 8):
                    continue

                if (instance_type['vcpus'] >= min_vcpus and
                   instance_type['memory'] >= min_memory and
                   instance_type['disk'] >= min_disk and
                   instance_type['disk'] >= min_size):
                    # found
                    selected_image = image
                    selected_instance_type = instance_type

                    found = True
                    break

            if found:
                break

        if not found:
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
            'count': 2
        })
        job_id = result['jobId']
        instance_ids = result['instanceIds']

        sleep(10)
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

        # stop instances
        result = API.conn.call('StopInstances', {
            'instanceIds': instance_ids[0:1],
        })
        job_id = result['jobId']

        wait_for_job(API, job_id, sleep)

        wait_busy_resource(API, 'DescribeInstances', {
            'status': ['pending', 'starting', 'stopping',
                       'restarting', 'scheduling']
        }, sleep)

        # start instances
        result = API.conn.call('StartInstances', {
            'instanceIds': instance_ids[0:1],
        })
        job_id = result['jobId']

        wait_for_job(API, job_id, sleep)

        wait_busy_resource(API, 'DescribeInstances', {
            'status': ['pending', 'starting', 'stopping',
                       'restarting', 'scheduling']
        }, sleep)

        # restart instances
        result = API.conn.call('RestartInstances', {
            'instanceIds': instance_ids[0:1],
        })
        job_id = result['jobId']

        wait_for_job(API, job_id, sleep)

        wait_busy_resource(API, 'DescribeInstances', {
            'status': ['pending', 'starting', 'stopping',
                       'restarting', 'scheduling']
        }, sleep)

        # stop instances
        result = API.conn.call('StopInstances', {
            'instanceIds': instance_ids[0:1],
        })
        job_id = result['jobId']

        wait_for_job(API, job_id, sleep)

        wait_busy_resource(API, 'DescribeInstances', {
            'status': ['pending', 'starting', 'stopping',
                       'restarting', 'scheduling']
        }, sleep)

        # reset instances
        result = API.conn.call('ResetInstances', {
            'instanceIds': instance_ids[0:1],
            'loginMode': 'password',
            'loginPassword': 'chenjie1234',
        })
        job_id = result['jobId']

        wait_for_job(API, job_id, sleep)

        wait_busy_resource(API, 'DescribeInstances', {
            'status': ['pending', 'starting', 'stopping',
                       'restarting', 'scheduling']
        }, sleep)

        # select instance_type for resize
        selected_instance_type_1 = None

        min_vcpus = selected_image['minVcpus']
        min_memory = selected_image['minMemory']
        min_disk = selected_image['minDisk']
        min_size = selected_image['size'] >> 30

        for instance_type in instance_types:
            # pass high flavor
            if (instance_type['memory'] >= 8192 or
               instance_type['vcpus'] >= 8):
                continue

            if (instance_type == selected_instance_type):
                continue

            if (instance_type['vcpus'] >= min_vcpus and
               instance_type['memory'] >= min_memory and
               instance_type['disk'] >= min_disk and
               instance_type['disk'] >= min_size):
                # found
                selected_instance_type_1 = instance_type
                break

        test_status = get_resource(API, 'DescribeInstances', {
             'instanceIds': instance_ids[0:1]
        }, 'instanceSet')[0]['status']

        if test_status == 'active':
            result = API.conn.call('StopInstances', {
                'instanceIds': instance_ids[0:1],
            })
            job_id = result['jobId']

            wait_for_job(API, job_id, sleep)

        wait_busy_resource(API, 'DescribeInstances', {
            'status': ['pending', 'starting', 'stopping',
                       'restarting', 'scheduling']
        }, sleep)

        # resize instances
        result = API.conn.call('ResizeInstances', {
            'instanceIds': instance_ids[0:1],
            'instanceTypeId': selected_instance_type_1['instanceTypeId'],
        })
        job_id = result['jobId']

        wait_for_job(API, job_id, sleep)

        wait_busy_resource(API, 'DescribeInstances', {
            'status': ['pending', 'starting', 'stopping',
                       'restarting', 'scheduling']
        }, sleep)

        sleep(10)
        # capture instance
        result = API.conn.call('CaptureInstance', {
            'instanceId': instance_ids[0],
            'name': 'test-capture-instance',
        })
        job_id = result['jobId']

        wait_for_job(API, job_id, sleep)

        # connect VNC
        result = API.conn.call('ConnectVNC', {
            'instanceId': instance_ids[1],
        })

        # get instance output
        result = API.conn.call('GetInstanceOutput', {
            'instanceId': instance_ids[1],
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
