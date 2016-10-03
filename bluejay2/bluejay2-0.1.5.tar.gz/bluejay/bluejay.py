import os
import ConfigParser
import json

import click

from openstack import Client


class Bluejay(object):
    """
    Command line tool to interface with nibiru
    """

    def __init__(self, home='~/.bluejay'):
        self.home = home
        self.verbose = True
        self.config = {}

    def read_configuration(self, profile='default'):
        config = ConfigParser.ConfigParser()
        config.read([
            os.path.expanduser('~/.bluejay/nibiru.ini'),
            './nibiru.ini',
            os.path.expanduser('{0}/nibiru.ini'.format(self.home)),
        ])
        # print os.path.expanduser('~/.bluejay/nibiru.ini')
        self.token = config.get(profile, 'token').strip("'")
        self.team = config.get(profile, 'team').strip("'")

    def set_config(self, key, value):
        self.config[key] = value

    def get_auth_headers(self):
        return {
            'Authorization': 'Bearer {}'.format(
                self.token.encode('base64').strip()),
            'Content-Type': 'application/json'
        }



pass_jay = click.make_pass_decorator(Bluejay)


@click.group()
@click.option(
    '--config-dir', envvar='CONFIG_DIR', default='.',
    help='Location to find ini files')
@click.option(
    '--profile', default='default',
    help='Profile to use for credentials')
@click.option(
    '--config', nargs=2, multiple=True,
    metavar='KEY VALUE', help='Overrides a config key/value pair.')
@click.option(
    '--host', '-h', default='https://nibiru-prod.prsn.us',
    help='Server URL')
@click.option(
    '--verbose', '-v', is_flag=True,
    help='Enable verbose mode')
@click.pass_context
def cli(ctx, config_dir, profile, config, host, verbose):
    """
    Command line tool to interface with nibiru
    """
    ctx.obj = Bluejay(config_dir)
    ctx.obj.read_configuration(profile=profile)
    ctx.verbose = verbose
    ctx.server_url = host
    ctx.obj.client = Client(
        url=ctx.server_url, token=ctx.obj.token, team=ctx.obj.team)
    for key, value in config:
        ctx.obj.set_config(key, value)


@cli.command()
@click.option(
    '--env', '-e', default='dev',
    help='Select envrionment for deployment')
@click.option(
    '--location', '-l', default='cocna',
    help='Region to deploy')
@click.option(
    '--instance-count', '-c', default=1,
    help='Number of instances to deploy')
@click.option(
    '--instance-size', '-s', default='small',
    help='Size of the instance')
@click.option(
    '--app-name', required=True,
    help='Name of the application')
@click.option(
    '--app-version', default='0.0.1',
    help='Version of the application')
@click.option(
    '--public', default=False, is_flag=True,
    help='Deploy to public network')
@click.option(
    '--aws', is_flag=True, default=False,
    help='Specify provider for deployment')
@click.option(
    '--tags', '-t', required=True, multiple=True,
    help='Tags for application')
@pass_jay
def create(
        jay, env, location, instance_count, instance_size,
        app_name, app_version, public, aws, tags):

    instances_ids = []
    privacy = 'pub'
    provider = 'openstack'

    if public is False:
        privacy = 'priv'

    if aws is True:
        provider = 'aws'

    processed_tags = {}
    processed_tags['created_by'] = 'bluejay'
    for t in tags:
        key, value = t.split(':')
        processed_tags[key] = value

    for i in xrange(0, instance_count):
        response = jay.client.create_instance(
            env=env, location=location, pub=privacy, provider=provider,
            instance_size=instance_size, app_name=app_name,
            app_version=app_version, tags=processed_tags)
        instances_ids.append(response.get('id', None))

        if jay.verbose is True:
            print response

    for i in instances_ids:
        print i


@cli.command()
@click.option(
    '--instance-id', '-i', required=True,
    help='ID of the instance to delete')
@pass_jay
def delete(jay, instance_id):
    status_code, response = jay.client.delete_instance(instance_id)
    print status_code, response


@cli.command()
@click.option(
    '--instance-id', '-i', required=True,
    help='ID of the instance to delete')
@click.option(
    '--size', '-s',
    help='Update size of the instance')
@click.option(
    '--tags', '-t', multiple=True,
    help='Update tags')
@pass_jay
def update(jay, instance_id, size, tags):
    tags_map = {}
    if tags is not None:
        for tag in tags:
            key, value = tag.strip().split(':')
            tags_map[key] = value

    print json.dumps(tags_map)
    status_code, response = jay.client.update_instance(
        instance_id, size=size, tags=tags_map)
    print status_code, response


@cli.command()
@click.option(
    '--all', '-a', is_flag=True, default=False,
    help='Update size of the instance')
@click.option(
    '--instance-id', '-i',
    help='ID of the instance')
@click.option(
    '--ip', '-n',
    help='Get instance information by IP')
@click.option(
    '--detailed', is_flag=True, default=False,
    help='Detailed information about an instance')
@click.option(
    '--tags', is_flag=True, default=False,
    help='Return tags of the instance')
@pass_jay
def get(jay, all, instance_id, detailed, tags, ip):

    if instance_id is not None:
        status_code, response = jay.client.get_instance(
            id=instance_id, detailed=detailed, tags=tags)
        print status_code, response
        return

    status_code, response = jay.client.get_instances(full=all, ip=ip)
    for i in response:
        print status_code, i
