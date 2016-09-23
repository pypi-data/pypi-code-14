from .delta_type import DeltaType
from .namedtuples.bind_args import BindArgs
from .namedtuples.bound import Bound
from .simplad_base import SimpladBase
from .simplad_monad import WrappedDelta
import abc

'''
bind process

input
    (~bound~, [])

extract unbound and annotation from ~bound~

 call bind until lowest layer

  call box
  input
      ([higher deltas, ..], unbound) bind

   call function
   input
       unbound

  returned (value, {deltas: delta, ...})
  bind up

 returned (unbound, [(is_default, delta), ...)
returned (bound, [])
'''

class SimpladBaseHelper(SimpladBase):
    @abc.abstractmethod
    def apply_delta(annotation, delta):
        ''' returns a single bound value '''
        return

    @abc.abstractmethod
    def initial_annotation(unbound):
        ''' returns the initial annotation '''
        return

    @abc.abstractmethod
    def merge_deltas(a, b):
        ''' returns WrappedDelta '''
        return

    @classmethod
    # returns (unbound,annotation), higher_deltas
    def bind(cls, func):
        def lam(i):
            higher_deltas = i.deltas
            higher_deltas.append(
                WrappedDelta(type=DeltaType.default, delta=None))
            res = cls.run(
                func, i.bound.annotation, i.bound.unbound, higher_deltas)
            unbound = res.bound
            higher_deltas = res.deltas
            wrapped_delta = cls.merge_r(higher_deltas.pop())
            delta_type = wrapped_delta.type
            if delta_type is DeltaType.finish:
                return BindArgs(bound=unbound, deltas=higher_deltas)
            if delta_type is DeltaType.default:
                return BindArgs(bound=Bound(unbound=unbound, annotation=i.bound.annotation),
                    deltas=higher_deltas)
            if delta_type is not DeltaType.configured:
                raise TypeError('unknown delta type')
            annotation, overwrite_unbound = cls.apply_delta(
                    i.bound.annotation,
                    wrapped_delta.delta,
                    unbound)
            if overwrite_unbound.overwrite is True:
                unbound = overwrite_unbound.new_value
            return BindArgs(
                    bound=Bound(unbound=unbound, annotation=annotation),
                    deltas=higher_deltas)
        return lam

    @classmethod
    # returns value, annotation
    def unit(cls, func):
        def ret(i):
            applied = func(i)
            return Bound(unbound=applied,
                    annotation=cls.initial_annotation(applied))
        return ret

    @classmethod
    # return [unbound, higher_deltas]
    def run(cls, func, annotation_before, unbound, higher_deltas):
        return func(BindArgs(bound=unbound, deltas=higher_deltas))

    @classmethod
    # returns WrappedDelta
    def merge_r(cls, wrapped_delta):
        if (wrapped_delta.type is not DeltaType.list):
            return wrapped_delta
        sub_deltas = [cls.merge_r(d) for d in wrapped_delta.delta]
        return reduce(
                lambda acc, d: cls.merge_deltas_wrap(acc, d),
                sub_deltas[1:],
                sub_deltas[0])

    @classmethod
    # returns WrappedDelta
    def merge_deltas_wrap(cls, a, b):
        if a.type is b.type is DeltaType.finish:
            return a
        if a.type is b.type is DeltaType.default:
            return a
        return WrappedDelta(
                type=DeltaType.configured,
                delta=cls.merge_deltas(a.delta, b.delta))
