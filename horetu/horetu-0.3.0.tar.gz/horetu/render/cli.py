import itertools
import textwrap
import shutil
import functools
from ..lib import Program
from ..signature import Signature, serialize_endpoint
from .doc import Doc

def _section_prefix(prog, x):
    for section in sorted(prog, key=len, reverse=True):
        if tuple(section[:len(x)]) == x:
            return x
    return tuple()

@serialize_endpoint
def _endpoints(section, s):
    signature = ''
    for x in s.positional:
        signature += ' %s' % x.name
    for x in s.keyword1:
        signature += ' [%s]' % x.name
    if s.var_positional:
        signature += ' [%s ...]' % s.var_positional.name
    return section, signature[1:]

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
        'endpoints': _endpoints(prog, section),
    }
    if p['message']:
        yield 'error: %(message)s' % p
    for i, (section, signature) in enumerate(p['endpoints']):
        q = {
            'prefix': 'usage: ' if i == 0 else '       ',
            'name': p['name'],
            'sub': (' ' + ' '.join(section)).rstrip() + ' ',
            'signature': signature,
            'sep': ' [--] ' if any(signature) else ' '
        }
        yield '%(prefix)s%(name)s%(sub)s[-help] [options]%(sep)s%(signature)s' % q

def man(name, f, h):
    columns, _ = shutil.get_terminal_size((80, 20))

    prog = Program(f)
    section = _section_prefix(prog, h.section)
    g = prog.get(section)
    fdoc = Doc(g)
    p =  {
        'name': name,
        'endpoints': _endpoints(prog, section),
        'description': fdoc.desc,
        'args': (_format_arg(' ', 2, a) for a in fdoc.args),
        'kwargs': (_format_arg('-', 2, a) for a in fdoc.kwargs),
    }

    yield 'SYNOPSIS'
    for section, signature in p['endpoints']:
        q = {
            'pointer': '  ' if section[len(h.section):] else '> ',
            'name': p['name'],
            'sub': (' ' + ' '.join(section)).rstrip() + ' ',
            'signature': signature,
            'sep': ' [--] ' if any(signature) else ' '
        }
        yield '%(pointer)s%(name)s%(sub)s[-help] [options]%(sep)s%(signature)s' % q
    if p['description']:
        yield 'DESCRIPTION'
        for line in textwrap.wrap(p['description'], columns-2):
            yield '  ' + line
    if p['args']:
        yield 'INPUTS'
        for arg in p['args']:
            yield arg
        try:
            arg
        except NameError:
            yield '  (None)'
    yield 'OPTIONS'
    for kwarg in p['kwargs']:
        yield kwarg
    yield 'DETAIL'
    yield '  Run "-help" with a particular subcommand for more help.'
