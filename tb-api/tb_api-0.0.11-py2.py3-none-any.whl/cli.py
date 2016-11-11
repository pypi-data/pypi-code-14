# encoding=utf-8
import click
from os.path import join, exists

import sys

from tb_api.loader.ioc import LoaderIOC
from tb_api.loader.simple import LoaderSimple
from tb_api.model import Config
from tb_api.script import start


# @click.command(help="Path to service. E.g.: my_package.service")
# @click.argument("base_name")
# @click.option("--module-suffix", "module_suffix", default="Service")
# @click.option("--project", "project_dir", default=".")
# @click.option("--debug", "debug", is_flag=True)
# @click.option("--port", '-p', "port", default=5000)
# def cli_start2(base_name, module_suffix, project_dir, debug, port):
#     # print(base_name, module_suffix, project_dir, debug)
#     start(base_name, module_suffix, project_dir, debug, port)

def error_exit_msg(msg):
    print(msg)
    sys.exit(1)


@click.group()
@click.option("--project", "project_dir", default=".")
@click.option("--debug", "debug", is_flag=True)
@click.option("--port", '-p', "port", default=5000)
@click.pass_context
def cli(ctx, project_dir, debug, port):
    ctx.obj['config'] = Config(project_dir, debug, port)


@cli.command(help='Simple load static module')
@click.argument("base_name")
@click.option("--module-suffix", "module_suffix", default="Service")
@click.pass_context
def simple(ctx, base_name, module_suffix):
    do_start(ctx, LoaderSimple(base_name, module_suffix))


@cli.command(help='Load using tb-ioc')
@click.option('--app', '-a', 'app', help='Application name. The config file will be loaded from app/<app>/services.yml')
@click.option('--config', '-c', 'config_files', multiple=True, help='Config files')
@click.option("--module-suffix", "module_suffix", default="")
@click.pass_context
def ioc(ctx, app, config_files, module_suffix):
    final_config_files = list(config_files)
    config = ctx.obj['config']
    if app:
        app_config_file = join(config.project_dir, 'app', app, 'services.yml')
        if not exists(app_config_file):
            error_exit_msg('Could not detect app at %s' % app_config_file)

        final_config_files.append(app_config_file)

    do_start(ctx, LoaderIOC(final_config_files, module_suffix))


def do_start(ctx, loader):
    config = ctx.obj['config']
    config.loader = loader

    start(config)


def cli_start():
    cli(obj={})
