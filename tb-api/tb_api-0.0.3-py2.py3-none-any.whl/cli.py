# encoding=utf-8
import click

from tb_api.script import start


@click.command(help="Path to service. E.g.: my_package.service")
@click.argument("base_name")
@click.option("--module-suffix", "module_suffix", default="Service")
@click.option("--project", "project_dir", default=".")
@click.option("--debug", "debug", is_flag=True)
def cli_start(base_name, module_suffix, project_dir, debug):
    print(base_name, module_suffix, project_dir, debug)
    start(base_name, module_suffix, project_dir, debug)
