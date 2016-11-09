import os
import shutil


def local_from_config(config):
    return Local(local_path_from_config(config))


def local_path_from_config(config):
    return [os.path.expanduser(d['local']) for d in config if 'local' in d][0]


class LocalResource(object):

    def __init__(self, local, path):
        self.local = local
        if path.startswith('/'):
            self.path = os.path.relpath(path, local.root)
        else:
            self.path = path

    def __hash__(self):
        return hash(repr(self))

    def __lt__(self, other):
        return self.path < other.path

    def __repr__(self):
        return '<{0.__class__.__name__} {0.path}>'.format(self)

    @property
    def basename(self):
        return os.path.basename(self.path)

    @property
    def dirname(self):
        return os.path.dirname(self.path)

    @property
    def full_path(self):
        return os.path.join(self.local.root, self.path)


class LocalFile(LocalResource):

    is_dir = False
    is_file = True

    def copy_to(self, sunvox_dir):
        with open(self.full_path, 'rb') as f:
            sunvox_dir.write_file(self.basename, f)

    def remove(self):
        os.unlink(self.full_path)


class LocalDir(LocalResource):

    is_dir = True
    is_file = False

    @property
    def abspath(self):
        return os.path.abspath(os.path.join(self.local.root, self.path))

    @property
    def children(self):
        for child_name in os.listdir(self.abspath):
            if child_name.startswith('.'):
                continue
            child_path = os.path.join(self.abspath, child_name)
            resource_type = \
                LocalDir if os.path.isdir(child_path) else LocalFile
            yield resource_type(self.local, child_path)

    def mkdir(self, name):
        os.makedirs(self.abspath, exist_ok=True)

    def remove(self):
        shutil.rmtree(self.full_path)

    def write_file(self, basename, content):
        local_path = os.path.join(self.abspath, basename)
        with open(local_path, 'wb') as f:
            f.write(content)


class Local(object):

    def __init__(self, root):
        self.root = root

    def __str__(self):
        return '<Local {}>'.format(self.root)

    def all_resources(self, top='/'):
        while top.startswith('/'):
            top = top[1:]
        os.path.abspath(os.path.join(self.root, top))
        root = LocalDir(self, top)
        paths_to_get = [root]
        while len(paths_to_get) > 0:
            path = paths_to_get.pop()
            yield path
            for child in path.children:
                if child.is_dir:
                    paths_to_get.append(child)
                elif child.is_file:
                    yield child

    def dir(self, path):
        return LocalDir(self, path)
