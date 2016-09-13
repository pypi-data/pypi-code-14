import os

from triptan import BaseStorage


class FileStorage(BaseStorage):
    """
        Stores the current revision in the configured path.
    """

    @property
    def storage_path(self):
        return os.path.join(self.path, self.config['filename'])

    def get_current_revision(self):
        try:
            with open(self.storage_path, 'r') as f:
                revision = f.read()
            return int(revision)
        except:
            return -1

    def set_current_revision(self, revision):
        with open(self.storage_path, 'w') as f:
            f.write(str(revision))
