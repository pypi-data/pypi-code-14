
from mambo import db, utils, get_config
from mambo.exceptions import ModelError
import json
from . import _get_app_options


class GlobalAppPreference(db.Model):
    app_id = db.Column(db.String(255), index=True)
    key = db.Column(db.String(255), index=True)
    value = db.Column(db.Text)
    description = db.Column(db.String(255))

    @classmethod
    def _syncdb(cls):
        o = _get_app_options()
        syncdb = o.get("syncdb_defaults")
        if syncdb:
            for k in syncdb:
                cls.set(key=k["key"],
                        value=k.get("value"),
                        description=k.get("description"),
                        app_id=k.get("app_id"))

    @classmethod
    def set(cls, key, value, description=None, app_id=None):

        key = utils.slugify(key)
        value = json.dumps({"data": value})

        k = cls.get_by_key(key, app_id=app_id)
        if k:
            k.update(value=value)
        else:
            cls.create(key=key,
                       value=value,
                       description=description,
                       app_id=app_id)

    @classmethod
    def get_by_key(cls, key, app_id=None):
        key = utils.slugify(key)
        k = cls.query().filter(cls.key == key)
        if app_id:
            k = k.filter(cls.app_id == app_id)
        return k.first()

    @classmethod
    def get_value(cls, key, app_id=None):
        k = cls.get_by_key(key, app_id=app_id)
        if not k:
            return None
        return json.loads(k.value)["data"]

    @classmethod
    def delete(cls, key, app_id=None):
        k = cls.get_by_key(key=key, app_id=app_id)
        if k:
            k.delete()
