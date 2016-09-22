import footmark
import footmark.ecs


def build_conn(region_id, **connect_args):
    return footmark.ecs.connect_to_region(region_id, **connect_args)


def operate_instance(region_id, **connect_args):
    conn = build_conn(region_id, **connect_args)

    filters = {}
    instance_ids = ["i-280k0cyh0"]
    # tag_key = 'xz_test'
    # tag_value = '1.20'
    # filters['tag:' + tag_key] = tag_value
    volume_ids = []
    filters['instance_id'] = 'i-280k0cyh0'
    get_all_instances = conn.get_all_instances(instance_ids=instance_ids, filters=filters)
    for inst in get_all_instances:
        print 'block_maping', inst.block_device_mapping
        bdm = getattr(inst, 'block_device_mapping')
        bdm_dict={}
        for device_name in bdm.keys():
            bdm_dict[device_name] = {
                'status': bdm[device_name].status,
                'volume_id': bdm[device_name].volume_id,
                'delete_on_termination': bdm[device_name].delete_on_termination
            }
        print bdm_dict
        print 'groups', inst.groups, inst.group_name
        for group in inst.groups:
            print group.id, group.name
        print 'state:', inst.state
    #     if inst.state == 'stopped':
    #         inst.start()
    #     if inst.status == 'running':
    #         inst.stop()
    #     print 'state:', inst.state
    get_all_volumes = conn.get_all_volumes(volume_ids=volume_ids, filters=filters)
    for disk in get_all_volumes:
        print disk.id, disk.status, disk.delete_on_termination
    filters = {}
    filters['security_group_id'] = get_all_instances[0].group_id
    get_all_groups = conn.get_all_security_groups(group_ids=None, filters=filters)
    for group in get_all_groups:
        print vars(group)

def run_instances(region_id, **connect_args):
    conn = build_conn(region_id, **connect_args)

    run_params = dict(zone_id='cn-shenzhen-a',
                      image_id='centos6u5_64_40G_cloudinit_20160427.raw',
                      instance_type='ecs.s1.small',
                      group_id='XXXXXXXXXX',
                      instance_name='test_footmark',
                      count=2)

    instances = conn.run_instances(**run_params)
    for inst in instances:
        print inst.id


def delete_instances(region_id, **connect_args):
    conn = build_conn(region_id, **connect_args)
    instance_ids = ["XXXXXXXXX"]
    force = False
    get_all_instances = conn.get_all_instances(instance_ids=instance_ids)
    for inst in get_all_instances:
        inst.terminate(force=force)


def main():
    connect_args = dict(acs_access_key_id='Q1QzBSnuozXv7y98',
                        acs_secret_access_key='4g4QQ6cBtyN3D7DjghtHOKm8ygRkZD')
    region_id = 'cn-qingdao'
    # test start stop restart instance
    operate_instance(region_id, **connect_args)

    # test delete instance
    # delete_instances(region_id, **connect_args)

    # test create instance
    # run_instances(region_id, **connect_args)


main()
