"""MSSQL Cli Client written in python."""
# Copyright (C) 2016 Russell Troxel

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os

import click
import pymssql

from mssqlcli import formats
from mssqlcli.config import Config


@click.group()
def cli():
    """Placeholder Function for click group."""
    # RTrox: Currently there is only command. This layout is
    # to allow forward compatibility once a `configure`
    # option is added, as well as any other future commands
    # that may be needed for MS-SQL Administration.
    pass


@click.option("--config-file", "-c", type=click.Path(),
              default=os.path.expanduser("~/.config/mssqlcli.yml"),
              help=("Override default config file location"
                    " (default: ~/.config/pymssql.yml)."))
@click.option("--output", "-o",
              type=click.Choice(formats.FORMAT_OPTIONS.keys()),
              default="json")
@click.argument("query", type=click.File('r'))
@cli.command()
def query(config_file, output, query):
    """
    Run a query against an MS-SQL Database.

    Config-file must be created before the query will succeed.
    Example configs can be found in the README.md.

    :param string config_file: path to config file. (yaml)
    :param string output: output type. Choices: pretty,json,csv
    :param string query: location of query file to be ran against the server.
    :rtype: None

    """
    query = query.read()
    config = Config(config_file)
    conn = pymssql.connect(
        config.server,
        config.get_username(),
        config.password
    )
    cursor = conn.cursor(as_dict=True)
    cursor.execute(query)

    results = [row for row in cursor]

    output = formats.FORMAT_OPTIONS[output](results)
    click.echo(output)


if __name__ == "__main__":  # pragma: nocover
    cli()
