from .types import Input
from . import lib
from ..signature import Signature
from ..exceptions import HoretuCouldNotParse

@Input
def cli(function, argv):
    sec = lib.getsection(True, function, argv)
    kwargs = Signature(sec.func).keyword2

    mixed = iter(argv[len(sec.section):])
    positionals = []
    flags = []
    before_double_hyphen = True
    while True:
        try:
            raw_arg = next(mixed)
        except StopIteration:
            break

        arg = raw_arg[1:]
        if before_double_hyphen and _yes_hyphen(raw_arg):
            if raw_arg == '--':
                before_double_hyphen = False
            elif arg in kwargs:
                x = kwargs[arg]
                if x.takes_parameter:
                    try:
                        value = next(mixed)
                    except StopIteration:
                        raise HoretuCouldNotParse('Needs parameter -- %s' % arg)
                else:
                    value = None
                flags.append((x.name, value))
            else:
                raise HoretuCouldNotParse('Unknown option -- %s' % arg)
        else:
            positionals.append(raw_arg)

    return dict(section=sec.section, func=sec.func,
                positionals=positionals, flags=flags)

def _yes_hyphen(x):
    return x.startswith('-')

def _no_hyphen(x):
    return not x.startswith('-')
