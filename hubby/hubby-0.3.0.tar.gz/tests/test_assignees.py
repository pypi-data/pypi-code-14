from hubby import Hub
import hubby

import responses

import unittest.mock as mock
import time
import os

@responses.activate
def test_get_remote_assignees():
    responses.add(responses.GET, 'https://api.github.com/repos/user/repo/assignees',
        json=[{'login': 'user1'}, {'login': 'user2'}])

    with mock.patch('hubby.git_wrapper.get_user_and_github_repo', lambda: ('user', 'repo')):
        hub = Hub('foobar')
        assignees = hub.get_remote_assignees()

    assert assignees == ['user1', 'user2']


def test_list_local_assignees(tempfile):
    hub = Hub('foobar')
    tempfile.write('user1\nuser2\n')
    tempfile.close()
    with mock.patch('hubby.get_assignee_cache_file', lambda u, r: open(tempfile.name)):
        local_assignees = hub.get_local_assignees()

    assert local_assignees == ['user1', 'user2']


def test_get_assignees_only_remote_writes_to_cache(tempfile):
    hub = Hub('foobar')
    remote_assignees = ['user1']
    with mock.patch.object(hub, 'get_local_assignees', lambda: []), \
            mock.patch.object(hub, 'get_remote_assignees', lambda: remote_assignees), \
            mock.patch('hubby.get_assignee_cache_file', lambda u, r, mode: tempfile):
        assignees = hub.get_assignees()

    assert assignees == remote_assignees
    with open(tempfile.name) as fh:
        assert fh.read() == 'user1\n'


def test_get_assignees_local_if_up_to_date():
    hub = Hub('foobar')
    local_assignees = ['user1']
    with mock.patch.object(hub, 'get_local_assignees', lambda: local_assignees), \
            mock.patch.object(hub, 'update_local_assignees', mock.Mock()):
        assignees = hub.get_assignees()

    assert assignees == local_assignees


def test_get_assignees_stale_local(tempfile):
    tempfile.write('user1\n')
    tempfile.close()
    two_days_in_s = 3600*24*2
    atime = int(time.time()*10**9)
    mtime = int((time.time() - two_days_in_s)*10**9)
    os.utime(tempfile.name, ns=(atime, mtime))

    hub = Hub('foobar')
    local_assignees = ['user1']
    update_local_mock = mock.Mock()
    with mock.patch.object(hub, 'get_local_assignees', lambda: local_assignees), \
            mock.patch.object(hub, 'update_local_assignees', update_local_mock), \
            mock.patch('hubby.get_assignee_cache_path', lambda u, r: tempfile.name):
        assignees = hub.get_assignees()

    assert assignees == local_assignees
    assert update_local_mock.called


def test_update_assignees(tempfile):
    hub = Hub('foobar')
    with mock.patch('os.fork', lambda: 0), \
            mock.patch.object(hub, 'get_remote_assignees', lambda: ['user1']), \
            mock.patch('hubby.get_assignee_cache_file', lambda u, r, mode: tempfile), \
            mock.patch('sys.exit', lambda c: None):
        hub.update_local_assignees()

    with open(tempfile.name) as fh:
        assert fh.read() == 'user1\n'



def test_get_assignee_cache_file(tempfile):
    tempfile.close()
    with mock.patch('os.path.expanduser', lambda _: tempfile.name):
        fh = hubby.get_assignee_cache_file('user', 'repo')

    assert fh.name == tempfile.name


def test_get_nonexisting_cache_file(tempfile):
    tempfile.close()
    os.remove(tempfile.name)

    with mock.patch('os.path.expanduser', lambda _: tempfile.name):
        fh = hubby.get_assignee_cache_file('user', 'repo')

    assert fh.name == tempfile.name


def test_missing_parent_directory_cache_file(tempdir):
    tempfile = os.path.join(tempdir, 'tempfile')
    os.removedirs(tempdir)
    with mock.patch('os.path.expanduser', lambda _: tempfile):
        fh = hubby.get_assignee_cache_file('user', 'repo')

    assert fh.name == tempfile
