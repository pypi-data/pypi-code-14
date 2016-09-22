from ..lib import Program
from ..signature import Signature
from .util import template
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

@template('cli-usage.txt')
def usage(name, f, h):
    prog = Program(f)
    section = _section_prefix(prog, h.section)
    return {
        'name': name,
        'message': h.message,
        'endpoints': list(_endpoints(prog, section)),
    }

@template('cli-man.txt')
def man(name, f, h):
    prog = Program(f)
    section = _section_prefix(prog, h.section)
    g = prog.get(section)
    fdoc = Doc(g)
    return {
        'is_section': hasattr(g, 'items'),
        'is_callable': hasattr(g, '__call__'),
        'name': name,
        'endpoints': list(_endpoints(prog, section)),
        'description': fdoc.desc,
        'args': fdoc.args,
        'kwargs': fdoc.kwargs,
    }
