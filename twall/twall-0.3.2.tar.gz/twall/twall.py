import click
from .web import create_app
from .console import run_console


@click.group()
def cli():
    pass


@cli.command()
@click.option('--auth-file', default='auth.cfg', help='The authentication file location.')
@click.option('--debug/--no-debug', default=False, help='Run Flask in debug mode')
def webapp(**kwargs):
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
    run_console(*args, **kwargs)


def main():
    cli()
