u"""
LICENSE:
Copyright 2016 Hermann Krumrey

This file is part of comunio-manager.

    comunio-manager is a program that allows a user to track his/her comunio.de
    profile

    comunio-manager is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    comunio-manager is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with comunio-manager.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
from __future__ import absolute_import
from raven import Client


u"""
The metadata is stored here. It can be used by any other module in this project this way, most
notably by the setup.py file
"""

project_name = u"comunio"
u"""
The name of the project
"""

project_description = u"A Comunio Desktop Application"
u"""
A short description of the project
"""

version_number = u"0.1.0"
u"""
The current version of the program.
"""

development_status = u"Development Status :: 3 - Alpha"
u"""
The current development status of the program
"""

project_url = u"http://gitlab.namibsun.net/namboy94/comunio-manager"
u"""
A URL linking to the home page of the project, in this case a
self-hosted Gitlab page
"""

download_url = u"http://gitlab.namibsun.net/namboy94/comunio-manager/repository/archive.zip?ref=master"
u"""
A URL linking to the current source zip file.
"""

author_name = u"Hermann Krumrey"
u"""
The name(s) of the project author(s)
"""

author_email = u"hermann@krumreyh.com"
u"""
The email address(es) of the project author(s)
"""

license_type = u"GNU GPL3"
u"""
The project's license type
"""

dependencies = [u"raven", u"requests", u"bs4", u"matplotlib"]
u"""
Python Packaging Index requirements
"""

audience = u"Intended Audience :: Developers"
u"""
The intended audience of this software
"""

environment = u"Environment :: Console"
u"""
The intended environment in which the program will be used
"""

programming_language = u"Programming Language :: Python"
u"""
The programming language used in this project
"""

topic = u"Topic :: Database :: Front-Ends"
u"""
The broad subject/topic of the project
"""

language = u"Natural Language :: English"
u"""
The (default) language of this project
"""

compatible_os = u"Operating System :: OS Independent"
u"""
The Operating Systems on which the program can run
"""

license_identifier = u"License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
u"""
The license used for this project
"""

# Sentry Configuration
sentry = Client(dsn=u"http://978e4ecaaa6b49e2ac5bba667d2b708d:67fcad2935614f44b02681d1ae12219e@85.214.124.204:9000/4",
                release=version_number)
u"""
The Sentry client for logging bugs
"""