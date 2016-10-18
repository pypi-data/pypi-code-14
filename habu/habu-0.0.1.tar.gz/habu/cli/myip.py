import click
from habu.lib.myip import get_myip

@click.command()
def myip():
    """Example script."""
    print(get_myip())


