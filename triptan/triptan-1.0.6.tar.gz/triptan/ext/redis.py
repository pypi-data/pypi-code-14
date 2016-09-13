import os

from redis import StrictRedis

from triptan import BaseStorage


class RedisStorage(BaseStorage):
    """
        Stores the current revision in the configured path.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._redis = None
        self.key_name = self.config.get(
            'storage_key', 'triptan_current_version'
        )

    @property
    def redis(self):
        if not self._redis:
            self._redis = StrictRedis(
                host=self.config['host'],
                port=self.config.get('port', 6379),
                db=self.config.get('db')
            )

        return self._redis

    @property
    def storage_path(self):
        return os.path.join(self.path, self.config['filename'])

    def get_current_revision(self):
        if self.redis.exists(self.key_name):
            return int(self.redis.get(self.key_name).decode("utf-8"))
        else:
            return -1

    def set_current_revision(self, revision):
        self.redis.set(self.key_name, str(revision))
