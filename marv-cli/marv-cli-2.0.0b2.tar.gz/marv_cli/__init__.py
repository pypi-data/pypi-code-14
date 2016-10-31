# -*- coding: utf-8 -*-
#
# MARV
# Copyright (C) 2016  Ternaris, Munich, Germany
#
# This file is part of MARV
#
# MARV is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# MARV is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with MARV.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, division, print_function

from pkg_resources import iter_entry_points

import click


CONFIG = None
VERBOSE = None


@click.group()
@click.option('--config', default='marv.conf',
              type=click.Path(dir_okay=False, resolve_path=True),
              help='Path to config file')
@click.option('-v', '--verbose', count=True, help='Increase verbosity')
def marv(config, verbose):
    """Manage a Marv site"""
    global CONFIG, VERBOSE
    CONFIG = config
    VERBOSE = verbose


def cli():
    """setuptools entry_point"""
    for ep in iter_entry_points(group='marv_cli'):
        ep.load()
    marv(auto_envvar_prefix='MARV')


if __name__ == '__main__':
    cli()
