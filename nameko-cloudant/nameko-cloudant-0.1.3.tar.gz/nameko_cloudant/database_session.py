from weakref import WeakKeyDictionary
from nameko.extensions import DependencyProvider
from cloudant.client import Cloudant

DATABASE_CONFIG = 'DATABASE'


class DatabaseSession(DependencyProvider):
    def __init__(self, database):
        self.database = database
        self.clients = WeakKeyDictionary()

    def setup(self, config=None):
        self.config=config if config else self.container.config[DATABASE_CONFIG]

    def stop(self):
        for client in self.clients:
            client.disconnect()
            del client

    def get_dependency(self, worker_ctx):
        client = Cloudant(
            self.config['username'],
            self.config['password'],
            account=self.config['account'],
            database=self.database,
        )

        self.clients[worker_ctx] = client
        client.connect()
        return client[self.database]

    def worker_teardown(self, worker_ctx):
        client = self.clients.pop(worker_ctx)
        client.disconnect()
