import re
from functools import partial
import operator
from collections import Counter, ChainMap

from . import options
from ... import exceptions
from ..doc import Doc
from ...signature import Signature

FLAG = re.compile(r'^-?(-[^-]).*')
Step = options.Step

def one(parser, f):
    s = Signature(f, with_help=False)
    d = Doc(f)
    kw = partial(get_kwargs,
                 ChainMap(d.args, d.kwargs),
                 len(s.keyword2) > 0)

    for param in s.positional:
        parser.add_argument(param.name, **kw(Step.positional, param))
    if s.var_positional:
        parser.add_argument(s.var_positional.name,
                            **kw(Step.positional, s.var_positional))
    for param in s.keyword1:
        parser.add_argument(s.keyword1.name, **kw(Step.keyword1, param))
    for name, param in s.keyword2.items():
        parser.add_argument('--' + name, **kw(Step.keyword2, param))

def get_kwargs(helps, k2, step, param):
    def call(x):
        try:
            return param.call(x)
        except exceptions.HoretuCouldNotParse as e:
            raise ValueError(e.message)
    kwargs = dict(nargs=options.nargs(k2, step),
                  action=options.action(step, param),
                  type=call,
                  default=param.default,
                  help=helps.get(param.name))
    if kwargs['action'] in {'store_true', 'store_false', 'count'}:
        del(kwargs['type'])
        del(kwargs['nargs'])
    return kwargs
