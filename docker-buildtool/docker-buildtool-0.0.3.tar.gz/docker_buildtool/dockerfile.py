import logging
import os
import six
import yaml
import logging

from docker_buildtool import error, utils

logger = logging.getLogger(__name__)

def assert_path(path, msg=None):
    if os.path.exists(path):
        return

    base = "Missing required path: {}".format(path)
    if msg is not None:
        base += '. {}'.format(msg)
    raise error.Error(base)

def path_from(file, *args):
    return os.path.join('.', os.path.dirname(file), *args)

def load_frontmatter(path):
    contents = []
    line_number = 0

    with open(path) as f:
        first = f.readline()
        line_number += 1
        if first != '# ---\n':
            logger.info('No frontmatter parsed from the head of %s. Must start with "# ---".', path)
            return None

        for line in f:
            line_number += 1
            if line == '# ---\n':
                # Reached the end!
                break
            elif line[:2] == '# ':
                # Contents
                line = line[1:]
                contents.append(line)
            else:
                raise UserError('Malformed docker-buildtool frontmatter {}:{}: {!r} must start with "# ". Frontmatter ends when it sees this marker: "# ---"'.format(path, line_number, line))

    contents = ''.join(contents)
    return yaml.load(contents)

def parse_include(includes):
    parsed = []
    for entry in includes:
        if isinstance(entry, six.string_types):
            include = StringInclude(entry)
        elif isinstance(entry, dict):
            path = entry['path']
            git = entry['git']
            setup = entry['setup']
            include = GitInclude(path, git, setup)
        else:
            raise error.Error('Bad include spec: {}'.format(include))
        parsed.append(include)
    return parsed

class StringInclude(object):
    installable = False

    def __init__(self, path):
        self.path = path
        self.installable = False

    def to_path(self, build_root):
        if '*' not in self.path: # don't try sanity checking patterns
            assert_path(os.path.join(build_root, self.path), '(While looking for specified include path {}.)'.format(self.path))
        return self.path

    def __str__(self):
        return '<StringInclude path={!r}>'.format(self.path)

class GitInclude(object):
    installable = True

    def __init__(self, path, git, setup):
        self.path = path
        self.git = git
        self.setup = setup

    def to_path(self, build_root):
        # Check if there's at least a directory there. (We can't
        # mandate anything about the actual git commit, since on
        # devboxes people may not sync their .git).
        assert_path(os.path.join(build_root, self.path), '(HINT: you can obtain this by running "git clone {} {}")'.format(self.git, self.path))
        return self.path

    def install(self, dryrun, build_root):
        path = os.path.join(build_root, self.path)
        if not os.path.exists(path):
            utils.execute_command(dryrun, ['git', 'clone', self.git, path])
            utils.execute_command(dryrun, self.setup, cwd=path, shell=True)
        else:
            # Pull in everything!
            utils.execute_command(dryrun, ['git', 'pull'], cwd=path)

    def __str__(self):
        return '<GitInclude git={!r} path={!r}>'.format(self.git, self.path)

class DockerfileBuildSpec(object):
    def __init__(self, path):
        frontmatter = self.frontmatter = load_frontmatter(path)
        if self.frontmatter is None:
            frontmatter = {}

        self.dockerfile = path
        self.build_root = frontmatter.get('build_root', path_from(self.dockerfile))
        include = frontmatter.get('include', [])
        include = parse_include(include)
        self.include = include
        self.ignore = frontmatter.get('ignore', [])
        self.workdir = frontmatter.get('workdir')

        self.setup = frontmatter.get('setup')

    def run_setup(self, dryrun):
        if self.setup is None:
            return
        utils.execute_command(dryrun, self.setup, cwd=path_from(self.dockerfile), shell=True)
