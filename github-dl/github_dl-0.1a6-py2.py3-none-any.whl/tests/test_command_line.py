import pytest
import download
from github import Github

from github_dl import github_dl
from github_dl import gist_dl

# TODO: update with monkey patching
# this might fail if we run out of
# requests so request for cameres' gists
# and github repositories

def monkey_setup_github(username, password, token, config):
    return Github()

# overwride setup to return a new github
# object with no credentials for a
# small limit on the number of requests
def test_github(monkeypatch):
    monkeypatch.setattr(download, 'setup_github', monkey_setup_github)
    pass


def test_gist(monkeypatch):
    monkeypatch.setattr(download, 'setup_github', monkey_setup_github)
    pass
