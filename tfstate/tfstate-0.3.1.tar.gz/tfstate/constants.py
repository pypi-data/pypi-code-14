import click

APP_NAME = 'tfstate'
STATE_URI_ENV_VAR = 'TFSTATE_URI'
CACHE_DIR_ENV_VAR = 'TFSTATE_CACHE_DIR'
DEFAULT_CACHE_DIR = click.get_app_dir(APP_NAME, force_posix=True)
