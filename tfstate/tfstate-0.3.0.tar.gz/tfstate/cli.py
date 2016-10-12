import click
import json
from . import constants
from . import convenience


@click.command()
@click.option('--state-uri', envvar=constants.STATE_URI_ENV_VAR, required=True)
@click.option('--cache-dir', default=constants.DEFAULT_CACHE_DIR,
              envvar=constants.CACHE_DIR_ENV_VAR, required=True)
@click.option('--cache-max-seconds', default=60, type=click.INT)
@click.option('--tf-module', help='The terraform module to use')
def cli(state_uri, cache_dir, cache_max_seconds, tf_module):
    output = convenience.get(
        state_uri, cache_dir=cache_dir,
        cache_max_seconds=cache_max_seconds,
        module=tf_module
    )
    click.echo(json.dumps(output))


if __name__ == '__main__':
    cli()
