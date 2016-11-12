import json

from six import string_types
from tb_ioc.class_utils import get_class


class JsonDumper(object):
    def __init__(self, cls=None):
        if cls:
            if isinstance(cls, string_types):
                cls = get_class(cls)

        self.cls = cls

    def dumps(self, data):
        return json.dumps(data, cls=self.cls)
