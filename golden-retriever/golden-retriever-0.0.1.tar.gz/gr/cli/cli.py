import sys
import context
import click
import yaml
import requests
from requests.exceptions import ConnectionError
from ..api import *
from .. import __version__

import logging
logger = logging.getLogger(__name__)

try:
    from logging import NullHandler
except ImportError:
    from logging import Handler

    class NullHandler(Handler):
        def emit(self, record):
            pass


@click.group()

@click.option('--settingsfile',
              help='Settings File',
              type=str,
              default=context.settings['settingsfile'])

@click.option('--url', help='API URL', type=str)

@click.option('--timeout',
              help='Global request timeout',
              type=int,
              default=60,
              required=False)

@click.version_option(version=__version__)
def cli(settingsfile, url, timeout):

    try:
        # load some settings from file over the top of the defaults
        stream = open(settingsfile, 'r')
        file_settings = yaml.load(stream)
        context.settings.update({k: v for k, v in file_settings.iteritems() if v})
    except IOError:
        pass

    # command line options override defaults and settings file
    args = {
        'settingsfile': settingsfile,
        'url': url,
        'timeout': timeout
    }
    for arg, value in args.iteritems():
        if value:
            context.settings[arg] = value


@click.command(short_help="status")
def status():

    url = context.settings['url']
    timeout = context.settings['timeout']

    click.echo('URL: %s' % url)
    click.echo('Timeout: %s' % timeout)

    try:
        resp = requests.get(url).status_code
        if resp == 200:
            click.echo('Authenticated: %s' % click.style('True', fg='green'))
        else:
            click.echo('Authenticated: %s, Status Code: %s' % (click.style('False', fg='red'), click.style(str(resp), fg='red')))
    except ConnectionError:
        click.echo(click.style(str('Connection Error'), fg='red'))

cli.add_command(status)
