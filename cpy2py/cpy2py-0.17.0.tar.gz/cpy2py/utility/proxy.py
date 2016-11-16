# - # Copyright 2016 Max Fischer
# - #
# - # Licensed under the Apache License, Version 2.0 (the "License");
# - # you may not use this file except in compliance with the License.
# - # You may obtain a copy of the License at
# - #
# - #     http://www.apache.org/licenses/LICENSE-2.0
# - #
# - # Unless required by applicable law or agreed to in writing, software
# - # distributed under the License is distributed on an "AS IS" BASIS,
# - # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# - # See the License for the specific language governing permissions and
# - # limitations under the License.
"""
Tools for creating proxies to objects
"""


def clone_function_meta(real_func, wrap_func):
    """Clone the public metadata of `real_func` to `wrap_func`"""
    wrap_func.__wrapped__ = real_func
    for attribute in (
            '__doc__', '__twin_id__',
            '__signature__', '__defaults__',
            '__name__', '__module__',
            '__qualname__', '__annotations__'
    ):
        try:
            setattr(wrap_func, attribute, getattr(real_func, attribute))
        except AttributeError:
            if attribute in ('__name__', '__module__'):
                raise TypeError('Unable to inherit __module__.__name__ from %r to %r' % (real_func, wrap_func))


def make_dunder_name(opnames, fmts=('__%s__',)):
    return [fmt % opname for opname in opnames for fmt in fmts]


#: names of mathematical operator special methods, e.g. `__add__`
DUNDER_MATH = make_dunder_name((
    'add', 'sub', 'mul',
    'divmod', 'floordiv', 'mod', 'truediv',
    'pow',
), (
    '__%s__', '__i%s__', '__r%s__'
))
#: names of comparison operator special methods, e.g. `__eq__`
DUNDER_COMPARISON = make_dunder_name((
    'eq', 'ne', 'lt', 'gt', 'ge', 'le'
))
#: names of bitwise operator special methods, e.g. `__rshift__`
DUNDER_BITWISE = make_dunder_name((
    'and', 'or', 'xor',
    'rand', 'ror', 'rxor',
    'iand', 'ior', 'ixor',
    'invert',
    'lshift', 'rshift'
))
#: names of conversion special methods, e.g. `__float__`
DUNDER_CONVERSION = make_dunder_name((
    'complex', 'float', 'int', 'index', 'long', 'nonzero', 'bool',
    'abs', 'ceil', 'floor', 'round',
    'neg', 'pos',
))
#: names of magic special methods, e.g. `__enter__`
DUNDER_SPECIAL = make_dunder_name((
    'hash',
    'reduce', 'reduce_ex',
    'enter', 'exit',
))
#: names of attribute special methods, e.g. `__getattr__`
DUNDER_ATTRIBUTE = make_dunder_name((
    'getattr', 'setattr', 'delattr',
))
#: names of magic operator special methods, e.g. `__str__`
DUNDER_PRINT = make_dunder_name((
    'str', 'repr', 'unicode',
))
#: names of class lifetime special methods, e.g. `__init__`
DUNDER_CONSTRUCT = make_dunder_name((
    'new', 'init', 'del',
))
DUNDER_ALL = DUNDER_MATH + DUNDER_COMPARISON + DUNDER_BITWISE + DUNDER_CONVERSION + \
             DUNDER_SPECIAL + DUNDER_ATTRIBUTE + DUNDER_PRINT + DUNDER_CONSTRUCT


class ProxyType(type):
    """
    Metaclass/Type for classes acting as proxies towards other objects
    """

    def __new__(mcs, name, bases, class_dict):
        pass
