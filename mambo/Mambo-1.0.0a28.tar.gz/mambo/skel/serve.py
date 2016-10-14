"""
________________________________________________________________________________

 /$$      /$$  /$$$$$$  /$$      /$$ /$$$$$$$   /$$$$$$
| $$$    /$$$ /$$__  $$| $$$    /$$$| $$__  $$ /$$__  $$
| $$$$  /$$$$| $$  \ $$| $$$$  /$$$$| $$  \ $$| $$  \ $$
| $$ $$/$$ $$| $$$$$$$$| $$ $$/$$ $$| $$$$$$$ | $$  | $$
| $$  $$$| $$| $$__  $$| $$  $$$| $$| $$__  $$| $$  | $$
| $$\  $ | $$| $$  | $$| $$\  $ | $$| $$  \ $$| $$  | $$
| $$ \/  | $$| $$  | $$| $$ \/  | $$| $$$$$$$/|  $$$$$$/
|__/     |__/|__/  |__/|__/     |__/|_______/  \______/

https://github.com/mardix/mambo

________________________________________________________________________________
"""

from mambo import MamboInit

# To create a command
from mambo.cli import MamboCLI

# Init Mambo
# The 'app' variable is required for the CLI tool, which is accessed at `mambo`
app = MamboInit(__name__)

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# CLI
class MyCLI(MamboCLI):
    def __init__(self, command, click):
        """
        Initiate the command line
        Place all your command functions in this method
        And they can be called with

            > mambo $fn_name

        ie:

            @command
            def hello():
                click.echo("Hello World!")

        In your terminal:
            > mambo hello


        :param command: copy of the cli.command
        :param click: click
        """

        @command()
        def setup():
            """
            The setup
            """
            click.echo("This is a setup!")

