from plato_cat.cases import wait_for_job
from plato_cat.cases import get_resource
from plato_cat.cases import wait_busy_resource
from plato_cat.cases import post_resource


class NetworkCase():

    def run(self, API, sleep):
        result = API.conn.call('CreateNetwork', {
            'name': 'network-creation-case',
        })

        network_id = result['networkId']
        job_id = result['jobId']

        wait_for_job(API, job_id, sleep)

        networks = get_resource(API, 'DescribeNetworks', {
            'status': ['active'],
            'networkIds': [network_id]
        }, 'networkSet')

        for n in networks:
            if n['status'] != 'active':
                raise Exception('network (%s) creation job finished,'
                                ' but status is not [active], but [%s]'
                                % (n['networkId'], n['status']))

        API.conn.call('CreateSubnet', {
            'networkId': network_id,
            'cidr': '192.168.200.0/24',
        })['subnetId']

        subnets = get_resource(API, 'DescribeSubnets', {
            'networkIds': [network_id],
            'status': ['active']
        }, 'subnetSet')

        if len(subnets) != 1:
            raise Exception('create subnet failed.')

        # set external gateway
        result = API.conn.call('SetExternalGateway', {
            'networkIds': [network_id],
        })
        result['networkIds']

        # update external gateway bandwidth
        API.conn.call('UpdateExternalGatewayBandwidth', {
            'networkIds': [network_id],
            'bandwidth': 1,
        })

        # create port forwarding
        API.conn.call('CreatePortForwarding', {
            'networkId': network_id,
            'protocol': 'tcp',
            'outsidePort': 10086,
            'insideAddress': '192.168.200.3',
            'insidePort': 10010,
        })


class CleanNetworks():

    def run(self, API, sleep):
        port_forwardings = get_resource(API, 'DescribePortForwardings', {
            'status': ['active']
        }, 'portForwardingSet')

        port_forwarding_ids = [i['portForwardingId']
                               for i in port_forwardings]

        post_resource(API, 'DeletePortForwardings',
                      port_forwarding_ids, 'portForwardingIds')

        wait_busy_resource(API, 'DescribeNetworks', {
            'status': ['pending', 'building'],
        }, sleep)

        networks = get_resource(API, 'DescribeNetworks', {
            'status': ['active', 'disabled', 'error']
        }, 'networkSet')

        network_ids = [n['networkId']
                       for n in networks if n['externalGatewayIp']]

        # unset external gateway
        post_resource(API, 'UnsetExternalGateway',
                      network_ids, 'networkIds')

        subnets = get_resource(API, 'DescribeSubnets', {
            'status': ['active']
        }, 'subnetSet')

        subnet_ids = [i['subnetId'] for i in subnets]

        post_resource(API, 'DeleteSubnets', subnet_ids, 'subnetIds')

        # delete networks
        network_ids = [n['networkId'] for n in networks]
        post_resource(API, 'DeleteNetworks', network_ids, 'networkIds')
