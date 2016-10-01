import sys
try:
    from importlib import machinery
except ImportError:
    # patching for import machinery
    # https://bitbucket.org/ericsnowcurrently/importlib2/issues/8/unable-to-import-importlib2machinery
    import importlib2._fixers as f
    fix_importlib_original = f.fix_importlib

    def fix_importlib(ns):
        if ns["__name__"] == 'importlib2.machinery':
            class _LoaderBasics:
                load_module = object()
            ns["_LoaderBasics"] = _LoaderBasics

            class FileLoader:
                load_module = object()
            ns["FileLoader"] = FileLoader

            class _NamespaceLoader:
                load_module = object()
                module_repr = object()
            ns["_NamespaceLoader"] = _NamespaceLoader
        fix_importlib_original(ns)
    f.fix_importlib = fix_importlib
    from importlib2 import machinery


def expose_all_members(module, globals_=None, _depth=2):
    members = {k: v for k, v in module.__dict__.items() if not k.startswith("_")}
    return expose_members(module, members, globals_=globals_, _depth=_depth)


def expose_members(module, members, globals_=None, _depth=1):
    if globals_ is None:
        frame = sys._getframe(_depth)
        globals_ = frame.f_globals
    globals_.update({k: module.__dict__[k] for k in members})
    return globals_


def import_from_physical_path(path, as_=None):
    module_id = as_ or path.replace("/", "_").rstrip(".py")
    return machinery.SourceFileLoader(module_id, path).load_module()
