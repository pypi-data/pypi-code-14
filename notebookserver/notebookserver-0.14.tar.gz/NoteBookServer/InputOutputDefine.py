# -*- coding: utf-8 -*-
import re
import json
from datacanvas.io_types import load_io_obj, BaseIO
from datacanvas.utils import mask_key


class Input(str):
    def __new__(cls, x, _types):
        return str.__new__(cls, x)

    def __init__(self, x, _types):
        super(Input, self).__init__()
        self.x = x
        self._types = _types

    def __repr__(self):
        return str(self.x)

    def __str__(self):
        return str(self.x)

    def as_first_line(self):
        with open(self.x, "r") as f:
            return f.readline().rstrip()

    def as_whole(self):
        with open(self.x, "r") as f:
            return f.read()

    def as_file(self, mode="r"):
        return open(self.x, mode)

    def as_datasource(self, mode="r"):
        ds = json.loads(open(self.x, mode).read())
        return ds

    def as_obj(self):
        ds = load_io_obj(self.x)
        return ds

    def as_raw(self):
        return str(self.x)

    @property
    def val(self):
        """Unboxing Input depends on its types."""
        if "any" in self._types:
            return self.as_raw()
        elif any([re.match(r"raw.*", t) for t in self._types]):
            return self.as_raw()
        else:
            return self.as_obj()

    @property
    def types(self):
        return self._types


class Output(str):
    def __new__(cls, x, _types):
        return str.__new__(cls, x)

    def __init__(self, x, _types):
        super(Output, self).__init__()
        self.x = x
        self._types = _types

    def __repr__(self):
        return str(self.x)

    def __str__(self):
        return str(self.x)

    def as_first_line(self):
        with open(self.x, "r") as f:
            return f.readline().rstrip()

    def as_whole(self):
        with open(self.x, "r") as f:
            return f.read()

    def as_file(self, mode="r"):
        return open(self.x, mode)

    def as_obj(self):
        ds = load_io_obj(self.x)
        return ds

    def as_raw(self):
        return str(self.x)

    @property
    def val(self):
        """Unboxing Input depends on its types."""
        if "any" in self._types:
            return self.as_raw()
        elif any([re.match(r"raw.*", t) for t in self._types]):
            return self.as_raw()
        else:
            return load_io_obj(self.x)

    @val.setter
    def val(self, value):
        with open(self.x, "w+") as f:
            if "any" in self._types or any([re.match(r"raw.*", t) for t in self._types]):
                return

            if isinstance(value, BaseIO):
                f.write(json.dumps(value))
            else:
                f.write(value)

    @property
    def types(self):
        return self._types


class Param(str):
    def __new__(cls, x, typeinfo,scope):
        return str.__new__(cls, x)

    def __init__(self, x, typeinfo ,scope):  # 声明类的2个属性
        super(Param, self).__init__()
        self._x = x
        self._typeinfo = typeinfo
        self._scope = scope

    def __repr__(self):
        if self.is_cluster:
            return self.show()
        else:
            return str(self._x)

    def __str__(self):
        if self.is_cluster:
            return self.show()
        else:
            return self.val#str(self._x)

    def show(self, mask_keys=True):
        def get_safe_cluster_param(cp):
            security_mask_names = ['accessKey', 'accessSecret', 'qubole_api_token', 'subscriptionId']
            if mask_keys and cp['Name'] in security_mask_names and 'Val' in cp:
                cp['Val'] = mask_key(cp['Val'])
                return cp
            return cp

        o = self.val
        if isinstance(o, dict):
            if self.is_cluster:
                cluster_params = o['Parameters']
                o['Parameters'] = [get_safe_cluster_param(cp) for cp in cluster_params]
                return json.dumps(o)
        else:
            return str(self._x)

    @property
    def type(self):
        return self._typeinfo['Type']

    @property
    def is_primitive(self):
        return self._typeinfo['Type'] not in ["cluster"]

    @property
    def is_cluster(self):
        return self._typeinfo['Type'] in ["cluster"]

    @property  #To call a method into attributes
    def val(self):
        type_handler = {
            "string": lambda x: x,
            "float": lambda x: float(x),
            "integer": lambda x: int(x),
            "enum": lambda x: x,
            "cluster": lambda x: json.loads(x),
            "file": read_whole_file,
            "map": lambda x:x,
            "enum2": lambda x:x
        }
        param_type = self._typeinfo['Type']
        if param_type in type_handler:
            return type_handler[param_type](self._x)
        else:
            return self._x


def read_whole_file(filename):
    with open(filename, "r") as f:
        return f.read()