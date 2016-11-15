from weakref import WeakKeyDictionary
from nameko.extensions import DependencyProvider
from cloudant.client import Cloudant
from cloudant.adapter import Replay429Adapter

DATABASE_CONFIG = 'DATABASE'


class DatabaseSession(DependencyProvider):
    def __init__(self, database, config=None):
        self.database = database
        self.config = config
        self.clients = WeakKeyDictionary()

    def setup(self):
        if not self.config:
            self.config = self.container.config[DATABASE_CONFIG]

    def stop(self):
        for client in self.clients:
            client.disconnect()
            del client

    def get_dependency(self, worker_ctx):
        adapter = Replay429Adapter(retries=100, initialBackoff=0.25)
        client = Cloudant(
            self.config['username'],
            self.config['password'],
            account=self.config['account'],
            adapter=adapter
        )

        self.clients[worker_ctx] = client
        client.connect()
        return client[self.database]

    def worker_teardown(self, worker_ctx):
        client = self.clients.pop(worker_ctx)
        client.disconnect()
