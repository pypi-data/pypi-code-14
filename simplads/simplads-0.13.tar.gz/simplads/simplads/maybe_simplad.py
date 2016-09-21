from enum import Enum
from simplads.simplad_monad.delta_type import DeltaType
from simplads.simplad_monad.namedtuples.bind_args import BindArgs
from simplads.simplad_monad.namedtuples.delta_overwrite import DeltaOverwrite
from simplads.simplad_monad.simplad_base_helper import SimpladBaseHelper
import abc

# delta: [messages], {new_listeners}, return_messages
# annotation_wrapper: is_default, {listeners}

# bind (func)(i) return (annotation_wrapper, unbound), higher_deltas
# unit(i) returns annotation_wrapper, unbound

class MaybeSimplad(SimpladBaseHelper):
    @staticmethod
    def initial_annotation(unbound):
        return MaybeType.has_value

    @staticmethod
    # returns Bound(unbound, higher_deltas)
    def run(func, annotation, unbound, higher_deltas):
        if annotation is MaybeType.has_value:
            return func(BindArgs(bound=unbound, deltas=higher_deltas))
        return BindArgs(bound=None, deltas=higher_deltas)

    @staticmethod
    # returns annotation, overwrite_unbound
    def apply_delta(annotation, delta, unbound):
        if delta is MaybeType.has_value:
            return delta, DeltaOverwrite()
        return delta, DeltaOverwrite(overwrite=True)

    @staticmethod
    def merge_deltas(a, b):
        if a is MaybeType.no_value:
            return a
        return b

class MaybeType(Enum):
    has_value = True
    no_value = False

class MaybeDeltaMaker():
    no_value = MaybeType.no_value
    has_value = MaybeType.has_value
