from multicorn import ForeignDataWrapper
from multicorn.utils import log_to_postgres, DEBUG, ERROR

import utils


class MongoDBStatFDW(ForeignDataWrapper):

    def __init__(self, options, columns):
        super(MongoDBStatFDW, self).__init__(options, columns)
        self._client = utils.getMongoConnection(options)

    def execute(self, quals, columns):
        log_to_postgres('exec quals: %s' % quals, DEBUG)
        log_to_postgres('exec columns: %s' % columns, DEBUG)

        db_names = []
        for q in quals:
            if q.field_name != u'db' or \
               not (
                   isinstance(q.operator, unicode) and q.operator == u'=' or
                   isinstance(q.operator, tuple) and q.operator[0] == u'='
               ):
                continue
            if isinstance(q.value, basestring):
                db_names = [q.value]
            elif isinstance(q.value, list):
                db_names = q.value
            break

        for db_name in self._client.database_names():
            if len(db_names) and db_name not in db_names:
                continue
            try:
                res_rows = self._client.get_database(name=db_name).command({'dbStats': 1})
                utils.convertNestedItemsToJson(res_rows)

                yield res_rows
            except Exception as e:
                log_to_postgres('could not get stats for db [%s]: %s' % (db_name, str(e)), ERROR)


class MongoCollStatFDW(ForeignDataWrapper):

    def __init__(self, options, columns):
        super(MongoCollStatFDW, self).__init__(options, columns)

        client = utils.getMongoConnection(options)

        if 'db' not in options:
            log_to_postgres('db name is not specified', ERROR)

        self._db = client.get_database(name=options['db'])

    def execute(self, quals, columns):
        log_to_postgres('exec quals: %s' % quals, DEBUG)
        log_to_postgres('exec columns: %s' % columns, DEBUG)

        for coll_name in self._db.collection_names():
            try:
                res_rows = self._db.command({'collStats': coll_name})
                utils.convertNestedItemsToJson(res_rows)

                yield res_rows
            except Exception as e:
                log_to_postgres('could not get stats for coll [%s]: %s' % (coll_name, str(e)), ERROR)
