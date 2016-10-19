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
"""Package to standardize Sphinx documentation in a GitHub organization."""

import importlib

from jinja2 import Environment, PackageLoader
from steenzout.object import Object


class ResourceGenerator(Object):
    """Class to generate Sphinx resources.

    Args:
        organization (str): name of the profile of the organization on GitHub.
        package (str): package to be documented.
        metadata (:py:module): module containing the package metadata.
        env (:py:class`jinja2.Environment`): the Jinja2 environment.
    """

    def __init__(self, organization, package):
        self.organization = organization
        self.package = package
        self.metadata = importlib.import_module('%s.metadata' % package)
        self.env = Environment(
            keep_trailing_newline=True,
            loader=PackageLoader('%s.sphinx' % self.organization, 'templates'))

    def conf(self):
        """Generate the Sphinx `conf.py` configuration file

        Returns:
            (str): the contents of the `conf.py` file.
        """
        return self.env.get_template('conf.py.j2').render(
            metadata=self.metadata,
            package=self.package)

    def makefile(self):
        """Generate the documentation Makefile.

        Returns:
            (str): the contents of the `Makefile`.
        """
        return self.env.get_template('Makefile.j2').render(
            metadata=self.metadata,
            package=self.package)
