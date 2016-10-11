
from mambo import db, utils, get_config
from mambo.exceptions import ModelError
import json
from . import _get_app_options
from six import string_types
from active_alchemy import ActiveAlchemy


class AppDataMixin(object):

    @classmethod
    def _syncdb(cls):
        o = _get_app_options()
        syncdb = o.get("syncdb_defaults")
        if syncdb:
            cls.import_preferences(syncdb)


    @classmethod
    def import_preferences(cls, prefs):
        """
        Import preferences
        :param prefs: list of dicts
        :return:
        """
        for p in prefs:
            if "key" not in p:
                raise AttributeError(
                    "Importing preference is missing attribute 'key'")
            try:
                cls.new(key=p.get("key"),
                        value=p.get("value"),
                        description=p.get("description"),
                        namespace=p.get("namespace", "Default"))
            except AttributeError as e:
                pass


    @classmethod
    def new(cls, namespace, key, value, description=None):
        _key = cls.make_key(namespace, key)
        k = cls.get_by_key(namespace, key)
        if k:
            raise AttributeError("Preference key '%s' exists already" % _key)
        k = cls.create(key=_key, description=description)
        k.data = value
        return k


    @classmethod
    def set(cls, namespace, key, value):
        _key = cls.make_key(namespace, key)
        k = cls.get_by_key(namespace, key)
        if not k:
            raise AttributeError("Preference key '%s' doesn't exist" % _key)
        k.data = value
        return k


    @classmethod
    def get_by_key(cls, namespace, key):
        key = cls.make_key(namespace, key)
        return cls.query().filter(cls.key == key).first()


    @property
    def data(self):
        return json.loads(self.value)["data"] if self.value else None


    @data.setter
    def data(self, value):
        if isinstance(value, string_types):
            if value.strip().lower() == "true":
                value = True
            elif value.strip().lower() == "false":
                value = False

        value = json.dumps({"data": value})
        self.update(value=value)


    @property
    def is_editable(self):
        """
        Based on the value type, it can determine to manually edit or not
        :return: bool
        """
        return True if isinstance(self.data, (string_types, int, bool)) else False


    @classmethod
    def make_key(cls, namespace, key):
        """
        Create a keyspace
        :param namespace:
        :param key:
        :return:
        """
        if not namespace:
            raise AttributeError("Preference namespace is missing")
        if not key:
            raise AttributeError("Preference key is missing")
        key = utils.slugify(key)
        return "%s.%s" % (namespace, key)


class AppData(db.Model, AppDataMixin):
    key = db.Column(db.String(255), index=True)
    value = db.Column(db.Text)
    description = db.Column(db.String(255))


# inmemdb = ActiveAlchemy("sqlite://")
#
# class InMemAppData(inmemdb, AppDataMixin):
#     key = inmemdb.Column(inmemdb.String(255), index=True)
#     value = inmemdb.Column(inmemdb.Text)
#     description = inmemdb.Column(inmemdb.String(255))




