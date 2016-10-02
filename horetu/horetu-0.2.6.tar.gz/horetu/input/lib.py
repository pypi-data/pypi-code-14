from funmap import funmap
from itertools import accumulate
from ..exceptions import HoretuCouldNotParse
from ..lib import Program
from . import lib

@funmap('func', 'section')
def getsection(is_cli, function, argv):
    prog = Program(function)
    for section in sorted(prog, key=len, reverse=True):
        if tuple(argv[:len(section)]) == section:
            valid = True
            break
    else:
        valid = False
    
    if valid:
        f = prog[section]
    else:
        if is_cli:
            def allow(a):
                return not a.startswith('-')
        else:
            def allow(a):
                return True
        for section in accumulate((a,) for a in argv if allow(a)):
            if section not in prog:
                break
        else:
            section = tuple()
        def f():
            if argv:
                msg = 'Bad subcommand'
            else:
                msg = 'Needs subcommand'
            raise HoretuCouldNotParse(section=section, message=msg)
    return {'func': f, 'section': section}
