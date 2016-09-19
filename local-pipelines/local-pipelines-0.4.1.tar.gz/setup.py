# vi:et:ts=4 sw=4 sts=4
#
# local-pipelines : run Bitbucket pipelines locally
# Copyright (C) 2016  Gary Kramlich <grim@reaperworld.com>
# Copyright (C) 2016  Sean Farley <sean@farley.io>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA

from setuptools import setup, find_packages

from pipelines import __version__


_DESC = "local-pipelines is a parser for bitbucket-pipelines.yml files " + \
        "that will run the pipeline using your local docker-engine."


def main():
    """ Creates our package """

    install_requires = []

    with open('requirements.txt') as ifp:
        for dependency in ifp.readlines():
            dependency = dependency.strip()

            if len(dependency) == 0 or dependency.startswith('#'):
                continue

            install_requires.append(dependency)

    setup(
        name='local-pipelines',
        version=__version__,
        description=_DESC,
        packages=find_packages('.'),
        install_requires=install_requires,
        zip_safe=True,
        author='Gary Kramlich',
        author_email='grim@reaperworld.com',
        url='http://bitbucket.org/rw_grim/local-pipelines',
        entry_points={
            'console_scripts': ['pipelines=pipelines.core:main'],
        },
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: DFSG approved',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',  # noqa
            'Natural Language :: English',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Topic :: Software Development :: Build Tools',
            'Topic :: Software Development :: Quality Assurance',
            'Topic :: Software Development :: Testing',
            'Topic :: Utilities',
        ],
    )


if __name__ == '__main__':
    main()
