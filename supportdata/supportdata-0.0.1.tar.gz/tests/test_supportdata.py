#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_supportdata
----------------------------------

Tests for `supportdata` module.
"""

import os
import tempfile

import pytest

from contextlib import contextmanager
#from click.testing import CliRunner

from supportdata.supportdata import download_file
#from supportdata import cli


@pytest.fixture
def response():
    """Sample pytest fixture.
    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument.
    """
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
#def test_command_line_interface():
#    runner = CliRunner()
#    result = runner.invoke(cli.main)
#    assert result.exit_code == 0
#    assert 'supportdata.cli.main' in result.output
#    help_result = runner.invoke(cli.main, ['--help'])
#    assert help_result.exit_code == 0
#    assert '--help  Show this message and exit.' in help_result.output


#def test_import():
#    assert hasattr(supportdata, 'download_file')


def test_download_file_nooutput():
    """ download_file requires a valid outputdir
    """
    try:
        download_file('non/existent/path', url=None, filename=None)
    except:
        return
    assert False, "download_file should file if invalid output path"


def test_download_file():
    download_file(
            tempfile.gettempdir(),
            "https://raw.githubusercontent.com/castelao/CoTeDe/master/LICENSE.rst",
            "LICENSE.rst")
    filename = os.path.join(tempfile.gettempdir(), "LICENSE.rst")
    assert os.path.exists(filename)
    os.remove(filename)


def download_file_md5():
    url = "https://raw.githubusercontent.com/castelao/CoTeDe/master/LICENSE.rst"
    md5hash = "68153c4036be9d8b8abd02011b5271ff"

    download_file(tempfile.gettempdir(), url, 'LICENSE.rst', md5hash)
    output = os.path.join(tempfile.gettempdir(), 'LICENSE.rst')
    assert os.path.exists(output)
    os.remove(output)

    try:
        download_file(tempfile.gettempdir(), url, 'LICENSE.rst', 'bad hash')
    except:
        return

    assert False, "download_file didn't fail with a bad hash"
