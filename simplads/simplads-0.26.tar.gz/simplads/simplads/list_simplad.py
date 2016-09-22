from enum import Enum
from simplads.simplad_monad.delta_type import DeltaType
from simplads.simplad_monad.namedtuples.bind_args import BindArgs
from simplads.simplad_monad.namedtuples.bound import Bound
from simplads.simplad_monad.namedtuples.delta_overwrite import DeltaOverwrite
from simplads.simplad_monad.namedtuples.wrapped_delta import WrappedDelta
from simplads.simplad_monad.simplad_base_helper import SimpladBaseHelper
import abc

# delta: [messages], {new_listeners}, return_messages
# annotation_wrapper: is_default, {listeners}

# bind (func)(i) return (annotation_wrapper, unbound), higher_deltas
# unit(i) returns annotation_wrapper, unbound

class ListSimplad(SimpladBaseHelper):
    @classmethod
    def unit(cls, func):
        def ret(i):
            return Bound(unbound=[func(child) for child in i], annotation=None)
        return ret

    @staticmethod
    def initial_annotation():
        raise NotImplementedException()

    @staticmethod
    # returns Bound(unbound, deltas)
    def run(func, annotation, unbound, higher_deltas):
        bounds = []
        deltas = []
        for elem in unbound:
            res = func(BindArgs(bound=elem, deltas=higher_deltas))
            bounds.append(res.bound)
            deltas.append(res.deltas)
        deltas = ListSimplad.rotate(deltas)
        return BindArgs(bound=bounds, deltas=deltas)

    @staticmethod
    def rotate(deltas_by_children):
        deltas_by_simplad = [[] for i in deltas_by_children[0]]
        for child in deltas_by_children:
            simplad_index = 0
            for simplad_delta in child:
                deltas_by_simplad[simplad_index].append(simplad_delta)
                simplad_index += 1
        return [WrappedDelta(type=DeltaType.list, delta=delta_list)
                for delta_list in deltas_by_simplad]

    @staticmethod
    # returns annotation, overwrite_unbound
    def apply_delta(annotation, delta, unbound):
        return delta, DeltaOverwrite()

    @staticmethod
    def merge_deltas(a, b):
        raise NotImplementedError
