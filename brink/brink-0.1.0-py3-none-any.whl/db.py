import rethinkdb as r


class Connection(object):

    def setup(self, config):
        r.set_loop_type("asyncio")
        self.config = config

    async def get(self):
        return await r.connect(
            db=self.config.get("db", "test"),
            port=self.config.get("port", 28015)
        )


conn = Connection()

