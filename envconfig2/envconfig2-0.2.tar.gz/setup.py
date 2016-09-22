# vi:et:ts=4 sw=4 sts=4
#
# envconfig2: easily read your config from the environment
# Copyright (C) 2016  Gary Kramlich <grim@reaperworld.com>
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

from setuptools import setup

from envconfig2 import __version__


_DESC = "envconfig2 makes it easy to read config settings from environment variables"  # noqa


def main():
    setup(
        name='envconfig2',
        version=__version__,
        description=_DESC,
        py_modules=['envconfig2'],
        zip_safe=True,
        author='Gary Kramlich',
        author_email='grim@reaperworld.com',
        url='http://bitbucket.org/rw_grim/envconfig2',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
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
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )


if __name__ == '__main__':
    main()

