import pytest
from functools import partial
from ..util import CallableDict

def _set(x):
    x[823] = 23

_objects = [
    ([], {}),
    ([{4:923}], {}),
    ([], {'blah': 'aoeu'}),
]
_methods = [
    list,
    dict,
    lambda x: x[4],
    lambda x: x.get(4),
    _set,
]

@pytest.mark.parametrize('args, kwargs', _objects)
@pytest.mark.parametrize('method', _methods)
def test_callable_dict(args, kwargs, method):
    return check_callable(dict, CallableDict, args, kwargs, method)


_objects = [
#   None,
    [],
    (3,4),
]
_methods = [
    list,
    lambda x: x[4],
    lambda x: x.append(4),
]

'''
@pytest.mark.parametrize('arg', _objects)
@pytest.mark.parametrize('method', _methods)
def test_callable_list(args, kwargs, method):
    return check_callable(list, CallableList, (args,), {}, method)
'''

def check_callable(Class, CallableClass, args, kwargs, method):
    def func(x):
        return x + 4
    
    callable_obj = CallableClass(func, *args, **kwargs)
    obj = Class(*args, **kwargs)
    f = partial(method, callable_obj)
    try:
        exp = method(obj)
    except Exception as e:
        with pytest.raises(e.__class__):
            f()
    else:
        f() == exp
