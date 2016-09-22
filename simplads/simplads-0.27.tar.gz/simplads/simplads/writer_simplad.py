from simplads.simplad_monad.namedtuples.delta_overwrite import DeltaOverwrite
from simplads.simplad_monad.simplad_base_helper import SimpladBaseHelper
from .namedtuples.writer_delta import WriterDelta
import abc

# bind (func)(((unbound, annotation), higher_deltas))
#     returns (unbound, annotation), higher_deltas
# unit(i) returns annotation, unbound

class WriterSimplad(SimpladBaseHelper):
    @staticmethod
    def initial_annotation(unbound):
        def printit(keys, val):
            print('not initialised')
        return printit

    @staticmethod
    # returns annotation, overwrite_unbound
    def apply_delta(annotation, delta, unbound):
        write_func = annotation
        if delta.has_new_write_func is True:
            write_func = delta.new_write_func
        if delta.has_data:
            write_func(keys=delta.keys, val=delta.data)
        return write_func, DeltaOverwrite()

    @staticmethod
    def merge_deltas(a, b):
        return WrappedDelta(
                type=DeltaType.configured,
                delta=WriterDelta(
                    data=a.data + b.data,
                    write_funcs=a.write_funcs + b.write_funcs))

class WriterDeltaMaker():
    @staticmethod
    def data(keys, new_data):
        return WriterDelta(has_data=True, data=new_data, keys=keys)

    @staticmethod
    def set_obj(root_obj, keys=None, new_data=None):
        def write_to_object(keys, val):
            obj = root_obj
            for key in keys[:-1]:
                if key not in obj.keys():
                    obj[key] = {}
                obj = obj[key]
            obj[keys[-1]] = val
        if keys is None:
            return WriterDelta(
                has_new_write_func=True,
                new_write_func=write_to_object)
        else:
            return WriterDelta(
                has_data=True,
                keys=keys,
                data=new_data,
                has_new_write_func=True,
                new_write_func=write_to_object)
