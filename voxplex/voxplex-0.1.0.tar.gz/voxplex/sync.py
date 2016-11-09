import posixpath


class Sync(object):

    def __init__(self, path, source, dest,
                 sync_deletes=False, always_copy=False):
        self.path = path
        self.source = source
        self.dest = dest
        self.sync_deletes = sync_deletes
        self.always_copy = always_copy
        self._ensured = set()

    def perform(self):
        print('Syncing {0.path!r}, {0.source} => {0.dest}'.format(self))
        print('  Sync deletes? {}'.format(self.sync_deletes))
        print('  Always copy? {}'.format(self.always_copy))
        print()
        self.ensure_dir(self.path)
        print('Finding resources...')
        source_resources = set(self.source.all_resources(self.path))
        dest_resources = set(self.dest.all_resources(self.path))
        print('  {} files at source'.format(
            len([r for r in source_resources if r.is_file])))
        print('  {} files at dest'.format(
            len([r for r in dest_resources if r.is_file])))
        print()
        print('Ensuring directories:')
        dest_paths = set(r.path for r in dest_resources if r.is_dir)
        for resource in sorted(source_resources):
            if resource.is_dir and resource.path not in dest_paths:
                self.ensure_dir(resource.path)
                print('  {}'.format(resource.path))
        print()
        print('Matching paths...')
        resources = {}
        for r in source_resources:
            if r.is_file:
                resources.setdefault(r.path, {})['source'] = r
        for r in dest_resources:
            if r.is_file:
                resources.setdefault(r.path, {})['dest'] = r
        print()
        print('Copying files...')
        for path, locations in sorted(resources.items()):
            s, d = locations.get('source'), locations.get('dest')
            if s and (self.always_copy or not d):
                print('  {}'.format(path))
                dest_dir = self.dest.dir(s.dirname)
                s.copy_to(dest_dir)
        print()
        if self.sync_deletes:
            print('Deleting files...')
            for path, locations in sorted(resources.items()):
                source, dest = locations.get('source'), locations.get('dest')
                if dest and not source:
                    print('  {}'.format(path))
                    dest.remove()

    def ensure_dir(self, path):
        parent_path = ''
        for path_part in path.split('/'):
            ensure_path = posixpath.join(parent_path, path_part)
            if ensure_path not in self._ensured:
                self.source.dir(parent_path).mkdir(path_part)
                self.dest.dir(parent_path).mkdir(path_part)
                self._ensured.add(ensure_path)
            parent_path = ensure_path
