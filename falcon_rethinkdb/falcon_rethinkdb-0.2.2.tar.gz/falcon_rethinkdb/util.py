from typing import Union, List, Optional
from urllib.parse import urlparse

import rethinkdb as r
from toolz.dicttoolz import merge, valfilter

from .types import IDType, ItemType

_default_config = dict(host='localhost',
                       port=r.DEFAULT_PORT,
                       db=None,
                       auth_key=None,
                       user='admin',
                       password=None,
                       timeout=20)


def parse_rethinkdb_url(url: str) -> dict:
    parse_ret = urlparse(url)
    config = {
        "host": parse_ret.hostname,
        "port": parse_ret.port,
        "user": parse_ret.username,
        "password": parse_ret.password,
        "db": parse_ret.path[1:] if len(parse_ret) > 1 else None
    }

    config = valfilter(lambda x: x is not None, config)

    return merge(_default_config, config)


def connect_rethinkdb(conf_or_url: Union[str, dict]) -> r.Connection:
    if isinstance(conf_or_url, str):
        conf = parse_rethinkdb_url(conf_or_url)
    else:
        conf = conf_or_url

    return r.connect(**conf)


class RethinkDBMixin(object):
    _table_name = None
    _index_names = []
    _primary_key = "id"

    def create_table(self, conn: r.Connection):
        table_list = list(r.table_list().run(conn))
        if self._table_name not in table_list:
            r.table_create(self._table_name, primary_key=self._primary_key).run(conn)

    def get_table(self):
        return r.table(self._table_name)

    def create_custom_indices(self, conn: r.Connection):
        pass

    def create_indices(self, conn: r.Connection):
        index_list = list(self.get_table().index_list().run(conn))
        for idx_name in self._index_names:
            if idx_name not in index_list:
                self.get_table().index_create(idx_name).run(conn)
        self.create_custom_indices(conn)

    def list_items(self, conn: r.Connection) -> List[ItemType]:
        return list(self.get_table().run(conn))

    def get_item(self, item_id: IDType, conn: r.Connection) -> Optional[ItemType]:
        return self.get_table().get(item_id).run(conn)

    def post_item(self, item: ItemType, conn: r.Connection) -> IDType:
        result = self.get_table().insert(item).run(conn)
        generated_key = result["generated_keys"][0]
        return generated_key

    def put_item(self, item_id: IDType, item: ItemType, conn: r.Connection) -> IDType:
        item[self._primary_key] = item_id
        self.get_table().insert(item, conflict="replace").run(conn)
        return item_id

    def update_item(self, item_id: IDType, partial_body: ItemType, conn: r.Connection) -> bool:
        result = self.get_table().get(item_id).update(partial_body).run(conn)
        ok = result["skipped"] == 0
        return ok

    def delete_item(self, item_id: IDType, conn: r.Connection) -> bool:
        result = self.get_table().get(item_id).delete().run(conn)
        ok = result["deleted"] == 1
        return ok
