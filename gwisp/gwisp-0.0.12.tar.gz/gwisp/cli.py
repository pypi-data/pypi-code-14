import sys
import click
import configparser
import os
from os import path
from .service import Service


root = path.realpath(path.join(path.dirname(__file__), '..'))
dconfig_file = path.join(root, 'dconfig.conf')


def read_config():
    config_file = path.join(root, 'config.conf')
    if not path.isfile(config_file):
        if os.name == 'posix':
            config_file = '/etc/gwisp/config.conf'
        else:
            config_file = '%SYSTEMDRIVE%\\gwisp\\config.conf'
    if not path.isfile(config_file):
        raise RuntimeError('Configuration file not found')

    config = configparser.ConfigParser()
    config.read([dconfig_file, config_file])
    app_config = config['app']

    return app_config


def get_service():
    config = read_config()

    return Service(int(config['port']), config['db_url'],
                   config['client_id'], config['client_secret'],
                   config['redirect_uri'], config['jwt_key'])


@click.group()
@click.version_option(version='0.0.1')
def cli():
    pass


@cli.command(help='Register root account')
@click.option('--passwd', required=True, help='Password of root account')
@click.option('--email', required=True, help='Email of root account')
def regroot(passwd, email):
    get_service().reg_root(email, passwd)


@cli.command(help='Empty database')
def renewdb():
    get_service().renew_db()


@cli.command(help='drop database then push sample data to database')
@click.option('--yes', count=True, help='skip confirm message')
def new(yes):
    if not yes:
        confirm = input('This action will drop databse y/n: ')
        if confirm.lower() != 'y':
            sys.exit(0)

    get_service().setup(path.join(root, 'asset/sample-data'))


@cli.command(help='start service')
@click.option('--port', default=9001, help='start gwisp on port')
@click.option('--verbose', count=True, help='show message during run')
def start(port, verbose):
    get_service().start()


@cli.command(help='show information of configuration file')
def info():
    config = read_config()

    print('verbose: {:s}'.format(config['verbose']))
    print('port: {:s}'.format(config['port']))
    print('db_url: {:s}'.format(config['db_url']))
    print('client_id: {:s}'.format(config['client_id']))
    print('client_secret: {:s}'.format(config['client_secret']))
    print('redirect_url: {:s}'.format(config['redirect_url']))
