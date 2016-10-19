from plato_cat.cases import get_resource


class MonitorCase():

    def run(self, API, sleep):
        instances = get_resource(API, 'DescribeInstances', {
            'status': ['active']
        }, 'instanceSet')

        # delete instances
        instance_ids = [i['instanceId'] for i in instances]

        metrics = [
            'instance.cpu',
            'instance.memory',
            'instance.disk.usage',
            'instance.disk.iops',
            'instance.disk.io',
            'instance.network.traffic',
            'instance.network.packets',
            'volume.usage',
            'volume.iops',
            'volume.io',
            'eip.traffic',
            'eip.packets',
        ]

        for period in [
            '120mins',
            '720mins',
            '48hours',
            '14days',
            '30days',
        ]:
            API.conn.call('GetMonitor', {
                'resourceIds': instance_ids,
                'metrics': metrics,
                'period': period,
            })
