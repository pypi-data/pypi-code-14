from importlib import machinery
import sys


def expose_all_members(module, globals_=None, _depth=2):
    members = {k: v for k, v in module.__dict__.items() if not k.startswith("_")}
    return expose_members(module, members, globals_=globals_, _depth=_depth)


def expose_members(module, members, globals_=None, _depth=1):
    if globals_ is None:
        frame = sys._getframe(_depth)
        globals_ = frame.f_globals
    globals_.update({k: module.__dict__[k] for k in members})
    return globals_


def import_by_physical_path(path, as_=None):
    module_id = as_ or path.replace("/", "_").rstrip(".py")
    return machinery.SourceFileLoader(module_id, path).load_module()
