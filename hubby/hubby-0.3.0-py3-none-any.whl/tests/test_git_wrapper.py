import unittest.mock as mock

import hubby.git_wrapper as uut

def test_get_github_user_and_repo(git_origin):
    mocked_check_output = lambda cmd: git_origin.show_output.encode('utf-8')
    with mock.patch('hubby.git_wrapper.subprocess.check_output', mocked_check_output):
         assert uut.get_user_and_github_repo() == (git_origin.user, git_origin.url)


def test_current_branch():
    with mock.patch('hubby.git_wrapper.subprocess.check_output', lambda c: b'master\n'):
        assert uut.get_current_branch() == 'master'


def test_get_upstream_branch(git_remote_tracking_branch):
    mock_branch_output = lambda c: git_remote_tracking_branch.output.encode('utf-8')
    with mock.patch('hubby.git_wrapper.subprocess.check_output', mock_branch_output):
        assert uut.get_remote_tracking_branch() == git_remote_tracking_branch.branch
