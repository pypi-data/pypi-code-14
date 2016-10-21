import json
import os

import click
import requests
import yaml

import gbboxcli.api


def main():
    try:
        cli(obj={})
    except gbboxcli.api.HttpRemoteError as e:
        error_obj = {
            'status_code': e.status_code,
            'error_type': e.error_type,
            'message': e.message,
        }
        print_error(error_obj)
    except requests.exceptions.ConnectionError as e:
        error_obj = {
            'error_type': 'Connection error',
            'message': str(e),
        }
        print_error(error_obj)
    except Exception as e:
        error_obj = {
            'error_type': str(e.__class__),
            'message': str(e),
        }
        print_error(error_obj)


@click.group()
def cli():
    pass


@cli.group()
def meta():
    pass


@meta.command(name='register')
@click.option('--service-id', required=True)
def meta_register(service_id):
    api = get_api()
    res = api.register_service(service_id)
    print_res(res)


@meta.command(name='list')
def meta_list():
    api = get_api()
    res = api.list_services()
    print_res(res)


@meta.command(name='update')
@click.option('--service-id', required=True)
@click.option('--config-path', required=True)
def meta_update(service_id, config_path):
    api = get_api()
    with open(config_path, 'r') as f:
        config = yaml.load(f)
        res = api.update_config(service_id, config)
        print_res(res)


@meta.command(name='get')
@click.option('--service-id', required=True)
def meta_get(service_id):
    api = get_api()
    res = api.get_config(service_id)
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

    api = get_api()
    res = api.route(
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
    api = get_api()
    log = {'tid': tid, 'q': q}
    if uid is not None:
        log['uid'] = uid
    res = api.process_log(service_id, log)
    print_res(res)


@cli.command(name='report')
@click.option('--service-id', required=True)
@click.option('--exp-id')
@click.option('--arm-id')
def report(service_id, exp_id, arm_id):
    api = get_api()
    if exp_id is None and arm_id is not None:
        raise click.BadOptionUsage('Specify exp-id option')

    if arm_id is not None:
        res = api.report_arm_perf(service_id, exp_id, arm_id)
    elif exp_id is not None:
        res = api.report_arm_perfs(service_id, exp_id)
    else:
        res = api.report_all_arm_perfs(service_id)
    print_res(res)


def get_api():
    # Try environment variables
    end_point = os.environ.get('GB_END_POINT', None)
    secret = os.environ.get('GB_SECRET', None)

    # Try configuration file
    if end_point is None or secret is None:
        home = os.path.expanduser('~')
        try:
            with open(os.path.join(home, '.gbbox.json'), 'r') as f:
                config = json.load(f)
                end_point = end_point or str(config['GB_END_POINT'])
                secret = secret or str(config['GB_SECRET'])
        except FileNotFoundError:
            pass
        except json.decoder.JSONDecodeError as e:
            raise ValueError('Invalid .gbbox.json file. %s' % str(e))
        except KeyError as e:
            raise ValueError('Key not found in .gbbox.json: %s' % str(e))

    # Error
    if end_point is None or secret is None:
        message = 'Provide GB_END_POINT and GB_SECRET environment variable ' \
                  'or create configuration file at ~/.gbbox.json'
        raise ValueError(message)

    return gbboxcli.api.API.get_http_api(end_point, secret)


def print_res(res):
    print(json.dumps(res, sort_keys=True, indent=4, separators=(',', ': ')))


def print_error(error_obj):
    print(json.dumps(error_obj, sort_keys=True, indent=4, separators=(',', ': ')))


if __name__ == '__main__':
    main()
