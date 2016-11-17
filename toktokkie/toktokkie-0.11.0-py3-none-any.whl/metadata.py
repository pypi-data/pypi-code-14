"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of toktokkie.

    toktokkie is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    toktokkie is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    toktokkie is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with toktokkie.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

"""
The metadata is stored here. It can be used by any other module in this project this way, most
notably by the setup.py file
"""


class GitRepository:  # pragma: no cover
    """
    Class that stores information about the git repository sites used by this project
    """

    repository_name = "toktokkie"
    """
    The name of the repository
    """

    github_owner = "namboy94"
    """
    The owner's Github username
    """

    gitlab_owner = "namboy94"
    """
    The project's owner's username on Gitlab
    """

    gitlab_site_url = "https://gitlab.namibsun.net/"
    """
    The address of the Gitlab instance
    """

    github_url = "https://github.com/" + github_owner + "/" + repository_name
    """
    The Github site URL
    """

    gitlab_url = gitlab_site_url + gitlab_owner + "/" + repository_name
    """
    The Gitlab Project URL
    """


class General:  # pragma: no cover
    """
    Class that stores general information about a project
    """

    project_description = "A personal media manager program"
    """
    A short description of the project
    """

    version_number = "0.11.0"
    """
    The current version of the program.
    """

    author_names = "Hermann Krumrey"
    """
    The name(s) of the project author(s)
    """

    author_emails = "hermann@krumreyh.com"
    """
    The email address(es) of the project author(s)
    """

    license_type = "GNU GPL3"
    """
    The project's license type
    """

    project_name = GitRepository.repository_name
    """
    The name of the project
    """

    download_master_zip = GitRepository.gitlab_url + "/repository/archive.zip?ref=master"
    """
    A URL linking to the current source zip file of the master branch.
    """


class PypiVariables:  # pragma: no cover
    """
    Variables used for distributing with setuptools to the python package index
    """

    classifiers = [

        "Environment :: Other Environment",
        "Natural Language :: English",
        "Intended Audience :: End Users/Desktop",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"

    ]
    """
    The list trove classifiers applicable to this project
    """

    install_requires = ['tvdb_api', 'beautifulsoup4', 'typing', 'raven', 'urwid', 'xdcc_dl']  # , "manga_dl"
    """
    Python Packaging Index dependencies
    """

    name = General.project_name
    """
    The name of the project on Pypi
    """

    version = General.version_number
    """
    The version of the project on pypi
    """

    description = General.project_description
    """
    The short description of the project on pypi
    """

    url = GitRepository.gitlab_url
    """
    A URL linking to the home page of the project, in this case a
    self-hosted Gitlab page
    """

    download_url = General.download_master_zip
    """
    A link to the current source zip of the project
    """

    author = General.author_names
    """
    The author(s) of this project
    """

    author_email = General.author_emails
    """
    The email adress(es) of the author(s)
    """

    license = General.license_type
    """
    The License used in this project
    """


class SentryLogger:  # pragma: no cover
    """
    Class that handles the sentry logger initialization
    """

    sentry_dsn = "https://82919205c6e8434683783f57939149ae:8f27907cecb7419184dd274cb41963fc@sentry.io/110683"
    """
    The DSN associated with this project
    """

    sentry = None
    """
    The sentry client
    """

    # Create the Sentry client to log bugs
    try:
        from raven import Client
        sentry = Client(dsn=sentry_dsn, release=General.version_number)
    except ImportError:
        Client = None
