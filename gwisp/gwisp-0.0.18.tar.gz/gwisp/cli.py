import sys
import click
import configparser
import os
from os import path
from .service import Service


root = path.realpath(path.join(path.dirname(__file__), '..'))


def read_config():
    config_file = path.join(root, 'config.conf')
    if not path.isfile(config_file):
        if os.name == 'posix':
            config_file = '/etc/gwisp/config.conf'
        else:
            config_file = '%SYSTEMDRIVE%\\gwisp\\config.conf'

    config = configparser.ConfigParser()
    config['DEFAULT'] = {
        'port': 9001,
        'redirect_uri': 'http://localhost/oauth/login',
        'db_url': 'mongodb://localhost/gwisp',
        'client_id': '736160870024-0cu341if9scqjfpvdsaqhutjebobjjq0.apps.'
                     'googleusercontent.com',
        'client_secret': 'hiznIzdC508X3sNOJpSfCrx7',
        'jwt_key': 'mirana-9870'
    }
    config.read([config_file])
    if 'APP' not in config:
        return config['DEFAULT']

    return config['APP']


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


@cli.command(help='Create new database with empty data')
def newdb():
    get_service().renew_db()


@cli.command(help='Create new database then push sample data to it')
@click.option('--yes', count=True, help='skip confirm message')
def new(yes):
    if not yes:
        confirm = input('This action will drop databse y/n: ')
        if confirm.lower() != 'y':
            sys.exit(0)

    get_service().setup(path.join(root, 'asset/sample-data'))


@cli.command(help='Start service')
def start():
    get_service().start()


@cli.command(help='Show information of configuration file')
def info():
    config = read_config()

    print('port: {:s}'.format(config['port']))
    print('db_url: {:s}'.format(config['db_url']))
    print('client_id: {:s}'.format(config['client_id']))
    print('client_secret: {:s}'.format(config['client_secret']))
    print('redirect_uri: {:s}'.format(config['redirect_uri']))
