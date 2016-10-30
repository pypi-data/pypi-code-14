from hubby import Hub
import hubby

import responses

import unittest.mock as mock
import time
import os


@responses.activate
def test_create_pull_request_with_assignee():
    responses.add(responses.POST, 'https://api.github.com/repos/user/repo/pulls',
        json={
          "id": 1,
          "url": "https://api.github.com/repos/user/repo/pulls/1347",
          "issue_url": "https://api.github.com/repos/user/repo/issues/1347",
          "number": 1347,
          "state": "open",
          "title": "new-feature",
          "body": "Please pull these awesome changes",
        })
    responses.add(responses.POST, 'https://api.github.com/repos/user/repo/issues/1347/assignees',
        json={
            "id": 1,
            "url": "https://api.github.com/repos/user/repo/issues/1347",
            "number": 1347,
            "state": "open",
            "title": "Found a bug",
            "body": "I'm having a problem with this.",
            "user": {
                "login": "octocat",
                "id": 1,
                "type": "User",
            },
            "labels": [],
    })

    with mock.patch('hubby.git_wrapper.get_user_and_github_repo', lambda: ('user', 'repo')), \
            mock.patch('hubby.git_wrapper.get_current_branch', lambda: 'master'), \
            mock.patch('hubby.git_wrapper.get_remote_tracking_branch', lambda: 'master'):
        hub = Hub('foobar')
        url = hub.create_or_update_pull_request('new-feature', assignees=['user1'])

    assert url == 'https://api.github.com/repos/user/repo/pulls/1347'


@responses.activate
def test_create_pushes_local_branch():
    responses.add(responses.POST, 'https://api.github.com/repos/user/repo/pulls',
        json={
          "id": 1,
          "url": "https://api.github.com/repos/user/repo/pulls/1347",
          "issue_url": "https://api.github.com/repos/user/repo/issues/1347",
          "number": 1347,
          "state": "open",
          "title": "new-feature",
          "body": "Please pull these awesome changes",
        })

    push_mock = mock.Mock()
    with mock.patch('hubby.git_wrapper.get_user_and_github_repo', lambda: ('user', 'repo')), \
            mock.patch('hubby.git_wrapper.get_current_branch', lambda: 'master'), \
            mock.patch('hubby.git_wrapper.get_remote_tracking_branch', lambda: None), \
            mock.patch('hubby.git_wrapper.push_and_set_upstream', push_mock):
        hub = Hub('foobar')
        url = hub.create_or_update_pull_request('new-feature')
        assert push_mock.called

    assert url == 'https://api.github.com/repos/user/repo/pulls/1347'
