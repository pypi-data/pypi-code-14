import itertools
import textwrap
import shutil
import functools
from ..lib import Program
from ..signature import Signature
from .doc import Doc

def _section_prefix(prog, x):
    for section in sorted(prog, key=len, reverse=True):
        if tuple(section[:len(x)]) == x:
            return x
    return tuple()

def _endpoints(prog, root_section):
    for section in sorted(prog):
        if section[:len(root_section)] == root_section:
            s = Signature(prog[section])

            signature = ''
            for x in s.positional:
                signature += ' %s' % x.name
            for x in s.keyword1:
                signature += ' [%s]' % x.name
            if s.var_positional:
                signature += ' [%s ...]' % s.var_positional.name
            yield section, signature[1:]

def _join(f):
    def decorator(*args, **kwargs):
        return '\n'.join(f(*args, **kwargs))
    return decorator

@_join
def _format_arg(prefix, indent, x):
    columns, _ = shutil.get_terminal_size((80, 20))
    argname, desc = x
    whitespace = ' ' * len(argname)
    n = columns - len(argname) - indent - len(prefix) - 2
    
    first = True
    for right in textwrap.wrap(desc, n):
        if first:
            left = argname + ': '
            first = False
        else:
            left = whitespace + '  '
        yield (' ' * indent) + left + right

def usage(name, f, h):
    prog = Program(f)
    section = _section_prefix(prog, h.section)
    p = {
        'name': name,
        'message': h.message,
        'endpoints': list(_endpoints(prog, section)),
    }
    if p['message']:
        yield 'error: %(message)s' % p
    for i, (section, signature) in enumerate(p['endpoints']):
        q = {
            'prefix': 'usage: ' if i == 0 else '       ',
            'name': p['name'],
            'sub': (' ' if section else '') + ' '.join(section),
            'signature': signature,
        }
        yield '%(prefix)s%(name)s%(sub)s [-help] [options] [--] %(signature)s' % q

def man(name, f, h):
    columns, _ = shutil.get_terminal_size((80, 20))

    prog = Program(f)
    section = _section_prefix(prog, h.section)
    g = prog.get(section)
    fdoc = Doc(g)
    p =  {
        'is_section': hasattr(g, 'items'),
        'is_callable': hasattr(g, '__call__'),
        'name': name,
        'endpoints': list(_endpoints(prog, section)),
        'description': fdoc.desc,
        'args': (_format_arg(' ', 2, a) for a in fdoc.args),
        'kwargs': (_format_arg('-', 2, a) for a in fdoc.kwargs),
    }

    yield 'SYNOPSIS'
    for section, signature in p['endpoints']:
        q = {
            'pointer': '> ' if p['is_section'] else '  ',
            'name': p['name'],
            'sub': ' '.join(section),
            'signature': signature,
        }
        yield '%(pointer)s %(name)s %(sub)s [-help] [options] [--] %(signature)s' % q
    if p['description']:
        yield 'DESCRIPTION'
        for line in textwrap.wrap(p['description'], columns-2):
            yield '  ' + line
    if p['is_callable']:
        yield 'INPUTS'
        for arg in p['args']:
            yield arg
    yield 'OPTIONS'
    for kwarg in p['kwargs']:
        yield kwarg
    try:
        kwarg
    except NameError:
        yield '  (None)'
    yield 'DETAIL'
    yield '  Run "-help" with a particular subcommand for more help.'
