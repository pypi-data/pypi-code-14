import re
from itertools import filterfalse
from funmap import funmap
from inspect import getdoc
from ..signature import Signature

@funmap('desc', 'args', 'kwargs')
def Doc(f):
    if not f:
        return {'desc': '', 'args': [], 'kwargs': []}
    lines = _doclines(f)
    colons = _read_colons(lines)
    s = Signature(f)

    _argnames = set(p.name for p in s.positional + s.keyword1)
    if s.var_positional:
        _argnames.add(s.var_positional.name)
    _kwargnames = set(p.name for p in s.keyword2.values())

    _args = []
    _kwargs = []

    for pair in colons:
        name, desc = pair
        if name in _argnames:
            _args.append(pair)
        else:
            _kwargs.append(pair)

    for name in _argnames:
        if name not in dict(_args):
            _args.append((name, 'Undocumented'))

    if not 'help' in dict(_kwargs):
        _kwargs.append(('help', 'Display this help.'))

    for name in _kwargnames:
        if name not in dict(_kwargs):
            _kwargs.append((name, 'Undocumented'))

    return {
        'desc': _desc(lines),
        'args': _args,
        'kwargs': _kwargs,
    }

COLON = re.compile(r'^[\s:]')
def _colon(line):
    return bool(re.match(COLON, line))

def _desc(lines):
    return '\n'.join(filterfalse(_colon, lines)).strip()

PARAM = re.compile(r'^:param (?:[^:]+ )?([^:]+): (.+)$')
INDENT = re.compile(r'\s+([^\s].*)')

def _read_colons(lines):
    y = []

    name = None
    for line in lines:
        if _colon(line):
            m = re.match(PARAM, line)
            n = re.match(INDENT, line)
            if m:
                # New parameter
                if name:
                    # Save the previous parameter if it exists.
                    y.append((name, desc.strip()))
                    name = None

                # Start the new description
                name, desc = m.groups()
            elif name and n:
                desc += ' ' + n.group(1)
    if name:
        # Save the last parameter
        y.append((name, desc.strip()))
    
    return y

def _doclines(f):
    d = getdoc(f)
    if not d:
        return ''
    return d.split('\n')
