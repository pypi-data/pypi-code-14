# -*- coding: utf-8 -*-
#
#   mete0r.recipe.nodejs: a buildout recipe to install node.js
#   Copyright (C) 2015-2016 mete0r <mete0r@sarangbang.or.kr>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import
from __future__ import unicode_literals
from textwrap import dedent
import platform


class Recipe:

    def __init__(self, buildout, name, options):

        #
        # options
        #
        version = options['version']

        downloads = options.setdefault(
            'downloads',
            buildout['buildout']['parts-directory'],
        )

        is64bit = platform.machine().endswith('64')
        system = platform.system().lower()
        if system in ('linux', 'darwin'):

            if system == 'linux':
                if is64bit:
                    bits = 'x64'
                else:
                    bits = 'x86'
            else:
                bits = 'x64'

            filename = b'node-{version}-{system}-{bits}.tar.xz'
            filename = filename.format(
                version=version,
                system=system,
                bits=bits,
            )

            url = b'https://nodejs.org/dist/{version}/{filename}'
            url = url.format(
                version=version,
                filename=filename,
            )
        else:
            raise NotImplementedError(system)

        url = options.setdefault(
            'url',
            url
        )

        directory = b'${buildout:directory}'
        directory = options.setdefault(
            'directory',
            directory,
        )

        #
        # download
        #
        section = '''
            [{name}.download]
            recipe = hexagonit.recipe.download
            url = {url}
            download-only = true
            filename = {filename}
            destination = {downloads}
        '''
        section = dedent(section)
        section = section.format(
            name=name,
            url=url,
            filename=filename,
            downloads=downloads,
        )
        buildout.parse(section)

        #
        # exclude
        #
        output = '${buildout:parts-directory}/${:_buildout_section_name_}'
        section = '''
            [{name}.exclude]
            recipe = collective.recipe.template
            output = {output}
            input =
                    inline:
                    CHANGELOG.md
                    README.md
                    LICENSE
        '''
        section = dedent(section)
        section = section.format(
            name=name,
            output=output,
        )
        buildout.parse(section)

        #
        # unpack
        #
        exclude_from = '${%(name)s.exclude:output}' % {
            'name': name,
        }
        archive_path = '${%(name)s.download:destination}/${%(name)s.download:filename}' % {  # noqa
            'name': name,
        }
        section = '''
            [{name}.unpack]
            recipe = collective.recipe.cmd
            on_install = true
            on_update = true
            cmds =
                    mkdir -p {directory}
                    tar -C {directory} --no-same-owner --strip-components=1 --exclude-from={exclude_from} -xJf {archive_path}
        '''  # noqa
        section = dedent(section)
        section = section.format(
            name=name,
            directory=directory,
            exclude_from=exclude_from,
            archive_path=archive_path,
        )
        buildout.parse(section)

    def install(self):
        return tuple()

    def update(self):
        return tuple()
