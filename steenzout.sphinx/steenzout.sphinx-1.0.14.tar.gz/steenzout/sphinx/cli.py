# -*- coding: utf-8 -*-
#
# Copyright 2016 Pedro Salgado
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Command line interface package."""

import os.path
import shutil
import tempfile

import click

from . import ResourceGenerator


@click.command()
@click.argument('organization', type=click.STRING)
@click.argument('package', type=click.STRING)
@click.argument('destination', type=click.Path(
    exists=True, file_okay=False, dir_okay=True, writable=True, resolve_path=True))
def generate(organization, package, destination):
    """Generates the Sphinx configuration and Makefile.

    Args:
        organization (str): the organization name.
        package (str): the package to be documented.
        destination (str): the destination directory.
    """
    gen = ResourceGenerator(organization, package)

    tmp = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
    try:
        tmp.write(gen.conf())
    finally:
        tmp.close()

    shutil.copy(tmp.name, os.path.join(destination, 'conf.py'))

    tmp = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
    try:
        tmp.write(gen.makefile())
    finally:
        tmp.close()

    shutil.copy(tmp.name, os.path.join(destination, 'Makefile'))
