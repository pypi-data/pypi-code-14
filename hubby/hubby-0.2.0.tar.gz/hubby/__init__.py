from . import git_wrapper as git

from contextlib import contextmanager
import errno
import getpass
import os
import platform
import sys
import tempfile
import time


class Hub(object):

    def __init__(self, auth_token, session=None):
        self.auth_token = auth_token
        self._session = session
        user, repo = git.get_user_and_github_repo()
        self.user = user
        self.repo = repo


    @property
    def session(self):
        if not self._session:
            self._session = Hub.create_session(self.auth_token)
        return self._session


    @staticmethod
    def create_session(token=None):
        from requests import Session
        # Importing requests can be very slow, so only do it here when we
        # actually need it, as many invocations of the program can be entirely
        # offline
        session = Session()
        session.headers.update({
            'accept': 'application/vnd.github.v3+json'
        })
        if token:
            session.headers.update({
                'authorization': 'token %s' % (token)
            })
        return session


    def get_assignees(self):
        local_assignees = self.get_local_assignees()

        if not local_assignees:
            remote_assignees = self.get_remote_assignees()
            self.cache_assignees(remote_assignees)
            return remote_assignees

        if self.local_assignees_is_stale():
            self.update_local_assignees()
        return local_assignees


    def cache_assignees(self, assignees):
        with get_assignee_cache_file(self.user, self.repo, mode='w') as fh:
            for assignee in assignees:
                fh.write(assignee)
                fh.write('\n')


    def get_remote_assignees(self):
        response = self.get('/repos/%s/%s/assignees' % (self.user, self.repo))
        assignees = []
        for user in response:
            assignees.append(user['login'])
        return assignees


    def create_or_update_pull_request(self, title, body='', base='master', assignees=None):
        # assert that local branch is non-master, checkout new temp branch named after commit
        # if it is, create pull request, set assignees on issue
        # check if local branch is pushed upstream, if not do that
        remote_branch = git.get_remote_tracking_branch()

        if not remote_branch:
            git.push_and_set_upstream()
            remote_branch = git.get_remote_tracking_branch()

        request_body = {
            'title': title,
            'base': base,
            'head': '%s:%s' % (self.user, remote_branch),
        }
        if body:
            request_body['body'] = body

        response = self.post('/repos/%s/%s/pulls' % (self.user, self.repo), body=request_body)
        if assignees:
            issue_url = response['issue_url']
            self.post('%s/assignees' % issue_url, body={
                'assignees': assignees
            })
        return response['url']


    def update_local_assignees(self):
        # Fork and do the updates in a subprocess, to enable it to work leisurely
        # on its own
        if os.fork() == 0:
            # in child, mix the ssl pool to avoid copying the parent
            import ssl
            ssl.RAND_add(os.urandom(16), 0.0)

            remote_assignees = self.get_remote_assignees()
            self.cache_assignees(remote_assignees)
            sys.exit(0)


    def get(self, path):
        response = self.session.get(self.full_url(path))
        response.raise_for_status()
        return response.json()


    def post(self, path, body):
        response = self.session.post(self.full_url(path), json=body)
        if response.status_code in (400, 422):
            sys.stderr.write('Invalid request. Request to %s was:\n%s\nResponse said:\n%s\n' % (
                path, body, response.text,
            ))
            return None
        response.raise_for_status()
        return response.json()


    def full_url(self, path):
        if path.startswith('https://'):
            return path
        return 'https://api.github.com%s' % path


    def get_local_assignees(self):
        user, repo = git.get_user_and_github_repo()
        assignees = []
        with get_assignee_cache_file(user, repo) as fh:
            for line in fh:
                assignees.append(line.strip())

        return assignees


    def local_assignees_is_stale(self):
        cache_file_path = get_assignee_cache_path(self.user, self.repo)
        try:
            stats = os.stat(cache_file_path)
        except FileNotFoundError:
            return True
        stale_cutoff = time.time() - 3600*24
        ret = stats.st_mtime < stale_cutoff
        return ret


def get_auth_token():
    token = read_token()
    session = None
    if not token:
        token, session = create_auth_token()
        store_token(token)
    return token, session


def create_auth_token():
    user = read_username()
    password = read_password()
    local_user = getpass.getuser()
    hostname = get_hostname()
    create_auth_body = {
        "scopes": [
            "repo",
        ],
        "note": "hubby for %s@%s" % (local_user, hostname),
    }
    auth = (user, password)
    session = Hub.create_session()
    response = session.post('https://api.github.com/authorizations', auth=auth,
        json=create_auth_body)

    if response.status_code == 401 and 'x-github-otp' in response.headers:
        # Prompt for otp
        one_time_code = read_otp()
        response = session.post('https://api.github.com/authorizations', headers={
            'x-github-otp': one_time_code,
        }, auth=auth, json=create_auth_body)

    response.raise_for_status()

    auth_token = response.json()['token']
    session.headers.update({
        'authorization': 'token %s' % auth_token,
    })
    return auth_token, session


def read_username():
    return input('GitHub username: ') # pragma: no cover


def read_password():
    return getpass.getpass('GitHub password: ') # pragma: no cover


def read_otp():
    return input('One-time code: ') # pragma: no cover


def get_hostname():
    return platform.node()


def store_token(token):
    token_file = get_token_file()
    try:
        os.makedirs(os.path.dirname(token_file))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise e
    with secure_open_file(token_file) as fh:
        fh.write(token)
        fh.write('\n')


def read_token():
    token_file = get_token_file()
    try:
        with open(token_file, 'r') as fh:
            return fh.read().strip()
    except IOError:
        return None


def get_token_file():
    return os.path.expanduser('~/.config/hubby/token') # pragma: no cover


def get_assignee_cache_file(user, repo, mode='r'):
    cache_file_path = get_assignee_cache_path(user, repo)
    try:
        return open(cache_file_path, mode)
    except FileNotFoundError:
        # File missing, try to create it
        try:
            return open(cache_file_path, 'w+')
        except FileNotFoundError:
            # Probably missing parent directory, create that and retry creating
            # the file
            parent_dir = os.path.dirname(cache_file_path)
            os.makedirs(parent_dir)
            return open(cache_file_path, 'w+')


def get_assignee_cache_path(user, repo):
    return os.path.expanduser('~/.cache/hubby/%s/%s/assignees' % (user, repo))


@contextmanager
def secure_open_file(filename):
    """ Securely open or create a new file with 0600 permissions.
    Strategy: Create the file directly with O_EXCL if possible, which ensures that the file did
    not already exist and that no one thus already has an open file descriptor which can read from
    it. If this fails, fall back to creating a temporary file in the same directory, and move it to
    the target location using os.rename. This is not distruptive towards other genuine applications
    reading the files being written. On Windows we fall back to deleting the target and re-creating
    it.
    Note: We do not try to ensure permissions on windows due to entirely different security models.
    If this is necessary for you, please submit a pull request. Some inspiration might be found
    here: http://timgolden.me.uk/python/win32_how_do_i/add-security-to-a-file.html.
    """
    mode = 0o600
    old_umask = os.umask(0)
    try:
        fd = os.open(filename, os.O_CREAT | os.O_WRONLY | os.O_EXCL, mode)
        handle = os.fdopen(fd, 'w')
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            if os.name == 'nt':
                # Windows doesn't support renaming to existing file, try to delete the target
                # and try again
                os.remove(filename)
                fd = os.open(filename, os.O_CREAT | os.O_WRONLY | os.O_EXCL, mode)
                handle = os.fdopen(fd, 'w')
            else:
                # The file already exists, create a tempfile and replace the file with new one
                pardir = os.path.dirname(filename)
                handle = tempfile.NamedTemporaryFile(dir=pardir, delete=False, mode='w')
                os.rename(handle.name, filename)
        else:
            raise
    finally:
        os.umask(old_umask)

    try:
        yield handle
    finally:
        handle.close()
