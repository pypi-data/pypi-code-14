import click

from .config import config_from_file
from .local import local_from_config
from .remote import remote_from_config
from .sync import Sync

DEFAULT_CONFIG_FILE = '~/.voxplex.yaml'


@click.group()
def main():
    pass


@main.command()
@click.argument('source_name')
@click.option('--config', '-c', default=DEFAULT_CONFIG_FILE,
              help='Config file.')
def ls(source_name, config):
    """List all files present at a source"""
    c = config_from_file(config)
    if source_name == 'local':
        source = local_from_config(c)
    else:
        source = remote_from_config(c, source_name)
    for path in source.all_resources():
        print(path)


@main.command()
@click.option('--config', '-c', default=DEFAULT_CONFIG_FILE,
              help='Config file.')
def paths(config):
    c = config_from_file(config)
    for path in [d['path'] for d in c if 'path' in d]:
        print(path)


@main.command()
@click.argument('remote_name')
@click.argument('path')
@click.option('--config', '-c', default=DEFAULT_CONFIG_FILE,
              help='Config file.')
def sync(remote_name, path, config):
    """Sync files between local and remote"""
    c = config_from_file(config)
    local = local_from_config(c)
    remote = remote_from_config(c, remote_name)
    path_config = [d for d in c if d.get('path') == path][0]
    if path_config['source'] == remote_name:
        source, dest = remote, local
    else:
        source, dest = local, remote
    sync = Sync(
        path, source, dest,
        sync_deletes=path_config.get('sync_deletes', False),
        always_copy=path_config.get('always_copy', False),
    )
    sync.perform()
