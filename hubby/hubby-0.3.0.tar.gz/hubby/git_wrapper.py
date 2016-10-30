import subprocess
import re

_git_ref = r'[a-zA-Z0-9-_/.]+'
_git_commitish = r'[0-9a-f]{4,}'
FETCH_URL_RE = re.compile(r'Fetch URL: (https://github.com/|[a-zA-Z0-9-_@.]+:)([a-zA-Z0-9-_]+)/([a-zA-Z0-9-_]+)')
REMOTE_TRACKING_BRANCH_RE = re.compile(
    r'\* ' + _git_ref + r' +' + _git_commitish + r' \[' + _git_ref + r'/(' + _git_ref + r').*\]'
)

def get_user_and_github_repo():
    cmd = ['git', 'remote', 'show', '-n', 'origin']
    output = subprocess.check_output(cmd).decode('utf-8')
    for line in output.split('\n'):
        line = line.strip()
        match = FETCH_URL_RE.match(line)
        if match:
            _, user, repo = match.groups()
            return (user, repo)
    return (None, None)


def get_current_branch():
    cmd = ['git', 'rev-parse', '--abbrev-ref', 'HEAD']
    output = subprocess.check_output(cmd).decode('utf-8')
    return output.strip()


def get_remote_tracking_branch():
    cmd = ['git', 'branch', '-vv']
    output = subprocess.check_output(cmd).decode('utf-8')
    for line in output.split('\n'):
        current_branch_match = REMOTE_TRACKING_BRANCH_RE.match(line)
        if current_branch_match:
            return current_branch_match.groups(1)[0]
    return None


def push_and_set_upstream():
    cmd = ['git', 'push', '--set-upstream', 'origin', get_current_branch()]
    subprocess.check_call(cmd)


def get_commits_ahead_of_master():
    cmd = ['git', 'log', '--reverse', '--format=%H', 'master..HEAD']
    output = subprocess.check_output(cmd).decode('utf-8').strip()
    return output.split('\n')


def get_commit_message(commitish):
    cmd = ['git', 'log', '--format=%B', '--max-count=1', commitish]
    output = subprocess.check_output(cmd).decode('utf-8')
    return output.strip()
