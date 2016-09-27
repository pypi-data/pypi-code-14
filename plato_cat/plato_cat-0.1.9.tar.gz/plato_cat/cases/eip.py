from plato_cat.cases import get_resource
from plato_cat.cases import post_resource


class EIPCase():

    def run(self, API, sleep):
        eips = get_resource(API, 'DescribeEips', {
            'status': ['active']
        }, 'eipSet')

        eip_ids = API.conn.call('AllocateEips', {
            'bandwidth': 1,
            'count': 1
        })['eipIds']

        new_eips = get_resource(API, 'DescribeEips', {
            'status': ['active']
        }, 'eipSet')

        if len(new_eips) - len(eips) != 1:
            raise Exception("after Allocate 1 Eips,"
                            "DescribeEips did not increase by 1!")

        API.conn.call('UpdateBandwidth', {
            'eipIds': eip_ids,
            'bandwidth': 1
        })

        instances = get_resource(API, 'DescribeInstances', {
            'status': ['active', 'stopped', 'error']
        }, 'instanceSet')
        instance_ids = [i['instanceId'] for i in instances]

        API.conn.call('AssociateEip', {
            'eipId': eip_ids[0],
            'instanceId': instance_ids[0],
        })


class CleanEips():

    def run(self, API, sleep):
        eips = get_resource(API, 'DescribeEips', {
            'status': ['active', 'associated'],
        }, 'eipSet')

        # dissociate eips
        eip_ids = [e['eipId'] for e in eips if e['resourceId']]
        post_resource(API, 'DissociateEips', eip_ids, 'eipIds')

        eip_ids = [e['eipId'] for e in eips]
        post_resource(API, 'ReleaseEips', eip_ids, 'eipIds')
