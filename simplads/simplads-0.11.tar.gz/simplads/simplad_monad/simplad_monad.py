from delta_type import DeltaType
from namedtuples.bind_args import BindArgs
from namedtuples.simplad_result import SimpladResult
from namedtuples.wrapped_delta import WrappedDelta

def compose(functions):
        return reduce(
            lambda acc, func: func(acc),
            functions[1:],
            functions[0])

def echo(i):
    return i

class SimpladMonad(object):
    @classmethod
    def get_four(cls):
        return 4

    @classmethod
    def make(cls):
        return {
            'simplad_order': [],
            'simplad_name_order': [],
            'binds': [],
            'simplads': {},
            'next_key': 1
        }

    @classmethod
    def set_simplad_order(cls, simplad_name_order):
        def ret(sm):
            sm['simplad_name_order'] = simplad_name_order
            sm['simplad_name_order'].reverse()

            def simpladf(acc, name):
                acc.append(sm['simplads'][name])
                return acc
            sm['simplad_order'] = reduce(
                simpladf,
                simplad_name_order,
                [])

            def bindf(acc, name):
                acc.append(sm['simplads'][name].bind)
                return acc
            sm['binds'] = reduce(
                bindf,
                simplad_name_order,
                [])
            sm['binds'].reverse()

            return sm
        return ret

    @classmethod
    def add_simplad(cls, simplad, key):
        def ret(sm):
            sm['simplads'][key] = simplad
            return sm
        return ret

    @classmethod
    def add_simplads(cls, simplads):
        def ret(sm):
            for key, simplad in simplads.iteritems():
                sm = cls.add_simplad(key=key, simplad=simplad)(sm=sm)
            return sm
        return ret

    @classmethod
    def unit(cls, sm):
        def ret(val):
            return reduce(
                lambda acc, simplad: simplad.unit(acc),
                sm['simplad_order'],
                echo
            )(val)
        return ret

    @classmethod
    def get_box(cls, sm):
        def g(func):
            def f(unboxed):
                res = func(unboxed.bound)
                bound = res.val
                delta_map = res.delta_map
                delta_keys = delta_map.keys()
                def f(acc, name):
                    if name in delta_keys:
                        acc.append(WrappedDelta(type=DeltaType.configured,
                            delta=delta_map[name]))
                    else:
                        acc.append(WrappedDelta(type=DeltaType.default,
                            delta=None))
                    return acc
                deltas = reduce(f, sm['simplad_name_order'], [])
                return BindArgs(bound=bound, deltas=deltas)
            return f
        return g

    @classmethod
    def bind(cls, func):
        def ret((sm, bound_before)):
            functions = sm['binds'] + [cls.get_box(sm), func]
            functions.reverse()
            return sm, compose(functions)(bound_before)
        return ret

    @classmethod
    def push_simplad(cls, simplad, key=None):
        def ret(sm):
            new_key = key
            if new_key is None:
                new_key = sm['next_key']
                sm['next_key'] = sm['next_key'] + 1
            sm = cls.add_simplad(simplad, new_key)(sm)
            sm['simplad_name_order'].append(new_key)
            sm['simplad_order'].reverse()
            sm['simplad_order'].append(simplad)
            sm['simplad_order'].reverse()
            sm['binds'].append(simplad.bind)
            return sm
        return ret
