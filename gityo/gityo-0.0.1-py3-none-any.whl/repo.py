import uuid
import os
from contextlib import contextmanager
import json
import errno

from . import gitx


class GitRepo:
    def __init__(self, root):
        root = os.path.abspath(root)
        ensure_dir_exist(root)
        self.root = root
        self.repository = None
        self.branch = None
        self.state = GitRepoState.INVALID
        self.git = gitx.Git(cwd=root)

    @staticmethod
    def clone(path, repository, branch=None):
        if branch is None:
            cmd = 'clone %s \"%s\"' % (repository, path)
        else:
            cmd = 'clone -b %s %s \"%s\"' % (branch, repository, path)
        git = gitx.Git()
        git.execute(cmd)
        repo = GitRepo(path)
        repo.repository = repository
        repo.branch = branch
        return repo

    def pull(self, repository=None, branch=None):
        if repository is None:
            cmd = 'pull'
        elif branch is None:
            cmd = 'pull %s' % repository
        else:
            cmd = 'pull %s %s' % (repository, branch)
        self.git.execute(cmd)

    def reset(self):
        self.git.execute('clean -d -f')
        self.git.execute('checkout -- .')


class GitRepoBucket:
    def __init__(self, base):
        self.base = base
        self.repos = []

    @contextmanager
    def open(self, repository, branch=None, reset=True):
        available_repos = self.find(repository, branch=branch, state=GitRepoState.AVAILABLE)
        if available_repos:
            repo = available_repos[0]
            if reset:
                repo.reset()
        else:
            rid = str(uuid.uuid4())
            repo_root = os.path.join(self.base, rid)
            repo = GitRepo.clone(path=repo_root, repository=repository, branch=branch)
            self.repos.append(repo)
        repo.state = GitRepoState.BEING_USED
        yield repo
        repo.state = GitRepoState.AVAILABLE

    def find(self, repository, branch=None, state=None):
        return [repo for repo in self.repos
                if repo.repository.lower() == repository.lower() and
                (branch is None or repo.branch is not None and branch.lower() == repo.branch.lower()) and
                (state is None or repo.state == state or repo.state in state)]

    def dump(self, dump_file=None):
        if dump_file is None:
            dump_file = os.path.join(self.base, 'bucket_dump.json')
        repos_data = [dict(repository=r.repository, branch=r.branch, root=r.root, state=r.state)
                      for r in self.repos]
        data = dict(base=self.base, repos=repos_data)
        ensure_dir_exist(os.path.dirname(dump_file))
        with open(dump_file, mode='w') as f:
            json.dump(data, f, indent=4)

    def open_each(self, repo_configs):
        if type(repo_configs) is str:
            configs = GitRepoConfig.load(repo_configs)
        else:
            configs = repo_configs
        for conf in configs:
            with self.open(conf.repository, conf.branch) as repo:
                yield repo

    @staticmethod
    def restore(base):
        dump_file = os.path.join(base, 'bucket_dump.json')
        if not os.path.isfile(dump_file):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), dump_file)
        with open(dump_file) as f:
            data = json.load(f)
        bucket = GitRepoBucket(data['base'])
        for r in data['repos']:
            repo = GitRepo(r['root'])
            repo.repository = r['repository']
            repo.branch = r['branch']
            repo.state = r['state']
            bucket.repos.append(repo)
        return bucket

    @staticmethod
    def restore_or_init(base):
        dump_file = os.path.join(base, 'bucket_dump.json')
        if not os.path.isfile(dump_file):
            bucket = GitRepoBucket(base)
        else:
            bucket = GitRepoBucket.restore(base)
        return bucket


class GitRepoState:
    INVALID = 'INVALID'
    BEING_USED = 'BEING_USED'
    AVAILABLE = 'AVAILABLE'


class GitRepoConfig:
    def __init__(self, name, repository, branch):
        self.name = name
        self.repository = repository
        self.branch = branch

    @staticmethod
    def load(config_file):
        with open(config_file) as f:
            data = json.load(f)
        return [GitRepoConfig(r['name'], r['repository'], r['branch']) for r in data]

    @staticmethod
    def save(configs, config_file):
        repos_data = [dict(name=r.name, repository=r.repository, branch=r.branch)
                      for r in configs]
        ensure_dir_exist(os.path.dirname(config_file))
        with open(config_file, mode='w') as f:
            json.dump(repos_data, f, indent=4)

    def __eq__(self, other):
        if other is None:
            return False
        return self.name == other.name and \
            self.repository == other.repository and \
            self.branch == other.branch

    def __hash__(self):
        return hash(self.name) ^ hash(self.repository) ^ hash(self.branch)


def ensure_dir_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)