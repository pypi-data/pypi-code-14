import click
import configparser
import os
from .web import create_app
from .console import run_console


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


@click.group()
def cli():
    """
    Entry point for the application's CLI
    """
    pass


@cli.command()
@click.option('--auth-file', default='auth.cfg', help='The authentication file location.')
@click.option('--debug/--no-debug', default=False, help='Run Flask in debug mode')
def webapp(**kwargs):
    """
    Runs the Flask web application. Should only be used when running from the command line.
    """
    app = create_app(kwargs['auth_file'], kwargs['debug'])
    app.run()


@cli.command()
@click.argument('query')
@click.option('--auth-file', default='auth.cfg', help='The authentication file location.')
@click.option(
    '--count', '-c',
    default=10,
    type=click.IntRange(0, 100),
    help='Number of tweets to load at startup.')
@click.option(
    '--interval', '-i',
    default=4,
    type=click.IntRange(1, 60),
    help='The number of seconds to wait between each Twitter request')
@click.option(
    '--result-type', '-t',
    type=click.Choice(['recent', 'mixed', 'popular']),
    default='recent',
    help='The result type')
def console(*args, **kwargs):
    """
    Runs the console application. Should only be used when running from the command line.
    """
    run_console(*args, **kwargs)


def read_config(config_file_path):
    """
    Reads the configuration file specified by the argument and the internal settings file, mashing them together into
    a single :mod:`configparser` instance.
    :param config_file_path: The path to the configuration file (usually containing OAuth credentials)
    :return: An instance of :mod:`configparser` that has read both configuration files.
    """
    config = configparser.ConfigParser()
    config.read([config_file_path, os.path.join(__location__, 'settings.cfg')])
    return config


def main():
    cli()
