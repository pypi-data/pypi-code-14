def patch_out_tecutil():
    """
    Patch out loading of DLL so we can
    import tecplot without pulling in
    the tecinterprocess binaries
    """
    from unittest.mock import patch, Mock

    class AutoAttr:
        def __call__(self):
            pass
        def __getattr__(self, attr):
            return self

    no_dlopen_patch = patch('ctypes.cdll.LoadLibrary', Mock(return_value=AutoAttr()))
    no_dlopen_patch.start()

patch_out_tecutil()
import tecplot

import fnmatch
import os
import pprint
import yaml

from importlib import import_module
from inspect import *
from os import path
from textwrap import dedent

def import_object(objname):
    try:
        return import_module(objname)
    except ImportError:
        try:
            mod, obj = objname.rsplit('.', 1)
            return getattr(import_module(mod), obj)
        except (AttributeError, ValueError):
            raise ImportError

def write_header(fout, title, level):
    uline = '=-^+~'
    fout.write('{}\n{}\n\n'.format(title, uline[level]*len(title)))

def write_ref(fout, name):
    fout.write('.. _{}:\n\n'.format(name))

def write_toc(fout, depth):
    fout.write(dedent('''\
        ..  contents::
            :local:
            :depth: {}

    '''.format(depth)))

def write_object(fout, name, typename, **opts):
    fout.write('.. auto{}:: {}\n'.format(typename, name))
    directives = ['members', 'inherited-members', 'imported-members',
                  'undoc-members']
    for d in directives:
        if opts.get(d, False):
            fout.write('    :{}:\n'.format(d))

def write_summary(fout, names, level):
    fmt = '.. autosummary::\n\n    {}\n'
    fout.write(indent('    '*level, fmt.format('\n    '.join(names))))

def write_class(fout, name, level):
    obj = import_object(name)

    #ignored_methods = ['next']
    #ignored_properties = []
    ignored_attrs = '''
        Range.count
        Range.index
        Array.from_param
    '''.split()

    methods = getmembers(obj, isfunction)
    methods = filter(lambda x: not x[0].startswith('_'), methods)
    #methods = filter(lambda x: x[0] not in ignored_methods, methods)
    methods = list(methods)

    def isproperty(x):
        return isdatadescriptor(x) or (not (isfunction(x) or isbuiltin(x)))

    properties = getmembers(obj, isproperty)
    properties = filter(lambda x: not x[0].startswith('_'), properties)
    #properties = filter(lambda x: x[0] not in ignored_properties, properties)
    properties = list(properties)

    namespace, classname = name.rsplit('.',1)

    fout.write('.. py:currentmodule:: {}\n\n'.format(namespace))
    write_header(fout, classname, level)
    write_object(fout, classname, 'class')

    if properties:
        fout.write('''
    **Attributes**

    .. autosummary::
        :nosignatures:

''')
        names, objs = list(zip(*properties))
        for obj_name, prop in sorted(properties):
            if '.'.join([classname, obj_name]) not in ignored_attrs:
                fout.write('        {}\n'.format(obj_name))

    if methods:
        fout.write('''
    **Methods**

    .. autosummary::

''')
        names, objs = list(zip(*methods))
        for obj_name, meth in sorted(methods):
            if '.'.join([classname, obj_name]) not in ignored_attrs:
                fout.write('        {}\n'.format(obj_name))
    fout.write('\n')

    def _type(obj):
        if isdatadescriptor(obj):
            return 'attribute'
        if isfunction(obj) or ismethod(obj):
            return 'method'

    if properties or methods:
        attrs = {k: v for k,v in zip(*zip(*(properties + methods)))}
        for attr_name, attr_obj in sorted(attrs.items()):
            attr_path = '.'.join([classname, attr_name])
            if attr_path not in ignored_attrs:
                t = _type(attr_obj)
                write_object(fout, attr_path, t or 'attribute')
                if t is None:
                    fout.write('    :annotation:\n')

def write_doc(data, outdir, fout=None, level=0, **opts):
    _tr = dict(fn='function', mod='module', cl='class')
    for i, row in enumerate(data):
        (key, value), = row.items()
        if key == 'topic':
            assert fout is None, 'can not nest topics.'
            opts = value[0]
            name = opts.pop('name', opts['title']).lower().replace(' ', '_')
            filename = 'tecplot.{}.rst'.format(name)
            rstfile = path.join(outdir, filename)
            with open(rstfile, 'w') as rstout:
                write_doc([{'sec': value}], outdir, rstout, level)
        elif key == 'sec':
            if level > 0:
                fout.write('\n')
            opts = value.pop(0)
            for ref in opts.get('aliases', []):
                write_ref(fout, ref)
            write_header(fout, opts['title'], level)
            if 'toc' in opts:
                write_toc(fout, opts['toc'])
            if value:
                write_doc(value, outdir, fout, level+1, **opts)
        elif key == 'class':
            if i > 0:
                fout.write('\n')
            write_class(fout, value, level)
        else:
            write_object(fout, value, _tr[key], **opts)

if len(sys.argv) != 3 or '-h' in sys.argv:
    print('usage: {} {} toc.yaml outdir'.format(sys.executable, sys.argv[0]))
    print('python version 3 (probably) required.')
    sys.exit(-1)

tocfile, outdir = sys.argv[1:]

with open(tocfile, 'r') as fin:
    data = yaml.load(fin.read())

if not path.exists(outdir):
    os.makedirs(outdir)
write_doc(data, outdir)
