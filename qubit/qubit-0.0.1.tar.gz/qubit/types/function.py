import json

__all__ = ['Function']


class Function(object):

    @classmethod
    def create(cls, name, body, closure={}, *args, **kwargs):
        return cls.manager.insert(name=name,
                                  body=body,
                                  closure=json.dumps(closure),
                                  *args, **kwargs)

    @classmethod
    def format(cls, raw: dict):
        if not raw:
            return None
        return cls.prototype(**raw)

    @classmethod
    def get_raw(cls, mid):
        return cls.format(cls.manager.get(mid))

    @classmethod
    def activate(cls, func):
        return eval(func.body,
                    dict(func.closure, **{cls.__name__: cls}))

    @classmethod
    def get(cls, mid):
        return cls.activate(cls.get_raw(mid))

    @classmethod
    def delete(cls, mid):
        return cls.mapper.delete(id=mid)
