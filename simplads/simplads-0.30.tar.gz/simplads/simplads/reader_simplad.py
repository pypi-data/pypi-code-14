from collections import namedtuple
from simplads.simplad_monad.namedtuples.delta_overwrite import DeltaOverwrite
from simplads.simplad_monad.simplad_base_helper import SimpladBaseHelper
from .namedtuples.reader_delta import ReaderDelta
from .namedtuples.reader_result import ReaderResult
import abc

# bind (func)(((unbound, annotation), higher_deltas))
#     returns (unbound, annotation), higher_deltas
# unit(i) returns annotation, unbound

class ReaderSimplad(SimpladBaseHelper):
    @staticmethod
    def initial_annotation(unbound):
        return lambda i: 'not initialised'

    @staticmethod
    # returns annotation, overwrite_unbound
    def apply_delta(annotation, delta, unbound):
        read_func = annotation
        if delta.has_new_read_func:
            read_func = delta.new_read_func

        if len(delta.keys) is 0:
            return read_func, DeltaOverwrite()

        if delta.overwrite:
            return read_func, DeltaOverwrite(
                overwrite=True,
                new_value=read_func(delta.keys))
        else:
            return read_func, DeltaOverwrite(
                overwrite=True,
                new_value=ReaderResult(read_val=read_func(delta.keys), val=unbound))

    @staticmethod
    def merge_deltas(a, b):
        return WrappedDelta(
                type=DeltaType.configured,
                delta=ReaderDelta(
                    keys = a.keys + b.keys,
                    has_new_read_func = False,
                    new_read_func = None))

class ReaderDeltaMaker():
    @staticmethod
    def read(keys, overwrite=None):
        if overwrite is None:
            return ReaderDelta(
                keys=keys,
                has_new_read_func=False,
                new_read_func=None)
        return ReaderDelta(
            keys=keys,
            has_new_read_func=False,
            new_read_func=None,
            overwrite=True)

    @staticmethod
    def set_obj(root_obj, keys=[]):
        def read_object(keys):
            obj = root_obj
            for key in keys:
                if key in obj.keys():
                    obj = obj[key]
                else:
                    return None
            return obj
        return ReaderDelta(
            keys=keys,
            has_new_read_func=True,
            new_read_func=read_object)
