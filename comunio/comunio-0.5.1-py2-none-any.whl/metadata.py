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

from __future__ import absolute_import
u"""
The metadata is stored here. It can be used by any other module in this project this way, most
notably by the setup.py file
"""


class GitRepository(object):
    u"""
    Class that stores information about the git repository sites used by this project
    """

    repository_name = u"comunio-manager"
    u"""
    The name of the repository
    """

    github_owner = u"namboy94"
    u"""
    The owner's Github username
    """

    gitlab_owner = u"namboy94"
    u"""
    The project's owner's username on Gitlab
    """

    gitlab_site_url = u"https://gitlab.namibsun.net/"
    u"""
    The address of the Gitlab instance
    """

    github_url = u"https://github.com/" + github_owner + u"/" + repository_name
    u"""
    The Github site URL
    """

    gitlab_url = gitlab_site_url + gitlab_owner + u"/" + repository_name
    u"""
    The Gitlab Project URL
    """


class General(object):
    u"""
    Class that stores general information about a project
    """

    project_description = u"A python program that keeps track of a user's comunio profile"
    u"""
    A short description of the project
    """

    version_number = u"0.5.1"
    u"""
    The current version of the program.
    """

    author_names = u"Hermann Krumrey"
    u"""
    The name(s) of the project author(s)
    """

    author_emails = u"hermann@krumreyh.com"
    u"""
    The email address(es) of the project author(s)
    """

    license_type = u"GNU GPL3"
    u"""
    The project's license type
    """

    project_name = GitRepository.repository_name
    u"""
    The name of the project
    """

    download_master_zip = GitRepository.gitlab_url + u"/repository/archive.zip?ref=master"
    u"""
    A URL linking to the current source zip file of the master branch.
    """


class PypiVariables(object):
    u"""
    Variables used for distributing with setuptools to the python package index
    """

    classifiers = [

        u"Environment :: Console",
        u"Natural Language :: English",
        u"Programming Language :: Python",
        u"Topic :: Database :: Front-Ends",
        u"Intended Audience :: Developers",
        u"Development Status :: 3 - Alpha",
        u"Operating System :: OS Independent",
        u"License :: OSI Approved :: GNU General Public License v3 (GPLv3)"

    ]
    u"""
    The list trove classifiers applicable to this project
    """

    install_requires = [u"raven", u"requests", u"bs4", u"matplotlib"]
    u"""
    Python Packaging Index dependencies
    """

    extras_require = {u"gui": [u"PyQt5"]}
    u"""
    Optional dependencies for Pypi
    """

    name = u"comunio"
    u"""
    The name of the project on Pypi
    """

    version = General.version_number
    u"""
    The version of the project on pypi
    """

    description = General.project_description
    u"""
    The short description of the project on pypi
    """

    url = GitRepository.gitlab_url
    u"""
    A URL linking to the home page of the project, in this case a
    self-hosted Gitlab page
    """

    download_url = General.download_master_zip
    u"""
    A link to the current source zip of the project
    """

    author = General.author_names
    u"""
    The author(s) of this project
    """

    author_email = General.author_emails
    u"""
    The email adress(es) of the author(s)
    """

    license = General.license_type
    u"""
    The License used in this project
    """


class SentryLogger(object):
    u"""
    Class that handles the sentry logger initialization
    """

    sentry_dsn = u"http://6a675d23de874b91ae455a7ee4790e8e:9337f78f416e4fdc8888b79b8827f592@sentry.namibsun.net/3"
    u"""
    The DSN associated with this project
    """

    sentry = None
    u"""
    The sentry client
    """

    # Create the Sentry client to log bugs
    try:
        from raven import Client
        sentry = Client(dsn=sentry_dsn, release=General.version_number)
    except ImportError:
        Client = None
