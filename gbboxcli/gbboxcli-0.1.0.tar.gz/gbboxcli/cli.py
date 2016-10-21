# TODO: Handle exception

import json
import os

import click
import yaml

from gbboxcli import api


def main():
    cli(obj={})


@click.group()
def cli():
    pass


@cli.group()
def meta():
    pass


@meta.command(name='register')
@click.option('--service-id', required=True)
def meta_register(service_id):
    gb = get_api()
    try:
        res = gb.register_service(service_id)
        print_res(res)
    except api.HttpRemoteError as e:
        print_error(e)


@meta.command(name='list')
def meta_list():
    gb = get_api()
    res = gb.list_services()
    print_res(res)


@meta.command(name='update')
@click.option('--service-id', required=True)
@click.option('--config-path', required=True)
def meta_update(service_id, config_path):
    gb = get_api()
    with open(config_path, 'r') as f:
        config = yaml.load(f)
        res = gb.update_config(service_id, config)
        print_res(res)


@meta.command(name='get')
@click.option('--service-id', required=True)
def meta_get(service_id):
    gb = get_api()
    res = gb.get_config(service_id)
    print_res(res)


@cli.command(name='route')
@click.option('--service-id', required=True)
@click.option('--exp-ids', required=True)
@click.option('--tid', required=True)
@click.option('--uid')
@click.option('--forced-arm-ids', help='expid1=armid1 expid2=armid2 ...')
def route(service_id, exp_ids, tid, uid, forced_arm_ids):
    if forced_arm_ids is not None:
        forced_arm_ids_parsed = dict(
            pair.split('=')
            for pair in forced_arm_ids.split(' ')
        )
    else:
        forced_arm_ids_parsed = {}

    gb = get_api()
    res = gb.route(
        service_id,
        exp_ids.split(','),
        tid,
        uid,
        forced_arm_ids_parsed
    )
    print_res(res)


@cli.command(name='collect')
@click.option('--service-id', required=True)
@click.option('--tid', required=True)
@click.option('--uid')
@click.option('--q', required=True)
def collect(service_id, tid, uid, q):
    gb = get_api()
    log = {'tid': tid, 'q': q}
    if uid is not None:
        log['uid'] = uid
    res = gb.process_log(service_id, log)
    print_res(res)


@cli.command(name='report')
@click.option('--service-id', required=True)
@click.option('--exp-id')
@click.option('--arm-id')
def report(service_id, exp_id, arm_id):
    gb = get_api()
    if exp_id is None and arm_id is not None:
        raise click.BadOptionUsage('Specify exp-id option')

    if arm_id is not None:
        res = gb.report_arm_perf(service_id, exp_id, arm_id)
    elif exp_id is not None:
        res = gb.report_arm_perfs(service_id, exp_id)
    else:
        res = gb.report_all_arm_perfs(service_id)
    print_res(res)


def get_api():
    return api.API.get_http_api(
        os.environ.get('GB_END_POINT'),
        os.environ.get('GB_SECRET'),
    )


def print_res(res):
    print(json.dumps(res, sort_keys=True, indent=4, separators=(',', ': ')))


def print_error(e):
    error = {
        'status_code': e.status_code,
        'error_type': e.error_type,
        'message': e.message,
    }
    print(json.dumps(error, sort_keys=True, indent=4, separators=(',', ': ')))


if __name__ == '__main__':
    main()
