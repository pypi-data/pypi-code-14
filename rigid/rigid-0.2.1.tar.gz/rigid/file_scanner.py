import os
import fnmatch
import tarfile


def scan(directory):
    for root, dirs, files in os.walk(directory):
        for name in files:
            yield os.path.relpath(os.path.join(root, name), directory)


def tar(tarball, files, source):
    with tarfile.open(tarball, 'w:gz') as tar:
        for path in files:
            tar.add(os.path.join(source, path), arcname=path)


class Skipper(object):
    DEFAULT_RULES = [
        '.git',
        '.DS_Store',
        '.rigid.yaml',
        '.rigid-*.yaml',

        # Vim swap files
        '*~',
        '*.swp',
        '*.swo',
    ]

    @classmethod
    def open(cls, path, default=True):
        with open(path) as fp:
            lines = map(lambda line: line.strip(), fp.readlines())
            lines = filter(lambda line: not line.startswith('#') and not len(line) == 0, lines)

        return cls(lines, default=default)

    def __init__(self, rules, default=True):
        self.rules = list(rules)

        if default:
            self.rules += self.DEFAULT_RULES

    def test(self, path):
        """
        Test if a file matches the rules.
        """

        components = path.split(os.sep)

        for component in components:
            for rule in self.rules:
                if rule == component:
                    return True

                if fnmatch.fnmatch(component, rule):
                    return True

        return False

    def __call__(self, path):
        return not self.test(path)
