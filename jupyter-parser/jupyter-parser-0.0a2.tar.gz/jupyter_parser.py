import click

from parsers import JupyterParser

from plugins import CellsCorrectPlugin
from plugins import NotebookLibrariesPlugin
from plugins import NotebookSparkPlugin


@click.command()
@click.option('--root', help='root directory to find files', default=".")
def parse(root):
    jp = JupyterParser(
        root, [
            CellsCorrectPlugin(),
            NotebookLibrariesPlugin(),
            NotebookSparkPlugin()
        ]
    )
    jp.parse()
