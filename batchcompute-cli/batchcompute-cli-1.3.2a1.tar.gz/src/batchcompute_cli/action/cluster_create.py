
# -*- coding:utf-8 -*-

from ..util import client,util,config
from terminal import green
import json


def create_cluster(clusterName, image=None, type=None, nodes=1, description='', user_data=None, disk=None, show_json=False):

    image = config.get_default_image() if not image else image
    type = config.get_default_instance_type() if not type else type

    cluster_desc = {}
    cluster_desc['Name'] = clusterName
    cluster_desc['ImageId'] = image
    cluster_desc['InstanceType'] = type
    cluster_desc['Description'] = description

    cluster_desc['Groups']={
        'group': {
            'InstanceType': type,
            'DesiredVMCount': nodes,
            'ResourceType': 'OnDemand'
        }
    }

    if user_data:
        cluster_desc['UserData'] = {}
        for item in user_data:
           cluster_desc['UserData'][item.get('key')]=item.get('value')

    if disk:
        if not cluster_desc.get('Configs'):
            cluster_desc['Configs'] = {}
        cluster_desc['Configs']['Disks']=disk

    if show_json:
        print(json.dumps(cluster_desc, indent=4))
    else:
        result = client.create_cluster(cluster_desc)

        if result.StatusCode==201:
            print(green('Cluster created: %s' % result.Id))



def trans_image(image):

    if not image.startswith('m-') and not image.startswith('img-'):
        raise Exception('Invalid imageId: %s' % image)
    return image



def trans_nodes(n):
    try:
        n = int(n)
        return n if n > 0 else 1
    except:
        return 1


def trans_user_data(user_data):
    items = user_data.split(',')
    t = []
    for item in items:
        arr = item.split(':',1)
        t.append( {'key': arr[0], 'value': arr[1] if len(arr)==2 else ''} )
    return t


def trans_disk(disk):
    return util.trans_disk(disk)