from brink.db import conn
import rethinkdb as r


class ObjectManager(object):

    def __init__(self, model_cls, table_name):
        self.model_cls = model_cls
        self.table_name = table_name

    def all(self):
        return ObjectSet(self.model_cls, r.table(self.table_name))

    def filter(self, *args, **kwargs):
        return self.all().filter(*args, **kwargs)

    async def get(self, id):
        return self.model_cls(
            **(await r.table(self.table_name).get(id).run(await conn.get())))

    async def delete(self, id):
        await r.table(self.table_name).get(id).delete().run(await conn.get())


class ObjectSet(object):

    cursor = None

    def __init__(self, model_cls, query):
        self.query = query
        self.model_cls = model_cls
        self.returns_changes = False

    def changes(self):
        self.query = self.query.changes()
        self.returns_changes = True
        return self

    async def as_list(self):
        return [obj async for obj in self]

    async def run(self):
        return await self.query.run(await conn.get())

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.cursor is None:
            self.cursor = await self.query.run(await conn.get())

        if (await self.cursor.fetch_next()):
            data = await self.cursor.next();

            if self.returns_changes:
                data = data["new_val"]

            return self.model_cls(**data)
        else:
            raise StopAsyncIteration

    def __getattr__(self, attr):
        def func_proxy(*args, **kwargs):
            self.query = getattr(self.query, attr)(*args, **kwargs)
            return self
        return func_proxy

