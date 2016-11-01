import click
from uamconfig import commands

@click.group()
def cli():
    pass

@click.command()
@click.argument("old")
@click.argument("new")
@click.option('--output', '-o', default="output.csv", help="Output file")
def diff(old, new, output):
    commands.diff.run(old, new, output)

@click.command()
@click.argument("properties")
@click.argument("patch")
@click.option('--output', '-o', default="ApplicationResoucres_en_US.properties", help="Output file")
def patch(properties, patch, output):
    commands.patch.run(properties, patch, output)

cli.add_command(diff)
cli.add_command(patch)

if __name__ == "__main__":
    cli()
