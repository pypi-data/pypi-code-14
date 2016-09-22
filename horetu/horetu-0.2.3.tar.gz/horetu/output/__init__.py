import inspect
from enum import Enum
from funmap import funmap
from functools import partial
from ..lib import Program
from .defaults import Defaults
from ..signature import Signature
from ..templates import AppIter
from ..exceptions import (
    HoretuException, Error,
    HoretuShowHelp, HoretuCouldNotParse,
)

ANNOTATE_POS = 'Cannot annotate positional argument "%s"'

def Output(config_file, config_sep, function, inputs):
    '''
    :type config_file: str or None
    :param config_file: Location of the configuration file, or None
    :param str config_sep: Separator character between command and
        subcommand names in the configuration file (Default is " ".)
    :type function: dict, list, or callable
    :param function: The function or collection of functions
    :param Inputs inputs: Specification of the section,
        positional arguments, and keyword arguments
    :returns: Either the payload (iter of bytes) or a :py:class:`HoretuException`
    '''
    defaults = Defaults(config_file, config_sep)

    s = Signature(inputs.func)
    g = _with_defaults(inputs.func, defaults, s)

    fail = None
    args = reify_args(s, inputs.section, inputs.positionals)
    if isinstance(args, HoretuException):
        fail = args

    kwargs = reify_kwargs(s, inputs.flags)
    if isinstance(kwargs, HoretuShowHelp):
        fail = kwargs

    if fail == None:
        y = g(*args, **kwargs)
        return AppIter(y)
    else:
        fail.section = inputs.section
        raise fail

def reify_args(s, section, positionals):
    return _reify_args(s, positionals[max(len(section)-1,0):])

def _reify_args(s, str_args):
    '''
    :param Signature s:
    '''
    xs = iter(str_args)
    args = []
    fail = None

    vp = [s.var_positional] if s.var_positional else []
    for a in s.positional + s.keyword1 + vp:
        if not a.supports_positional:
            return TypeError(ANNOTATE_POS % a.name)

    for a in s.positional:
        try:
            x = next(xs)
        except StopIteration:
            fail = HoretuCouldNotParse(message='Not enough arguments')
        else:
            args.append(a.call(x))

    for a in s.keyword1:
        try:
            x = next(xs)
        except StopIteration:
            break
        else:
            args.append(a.call(x))

    a = s.var_positional
    if a:
        args.extend(map(a.call, xs))
    else:
        xs = list(xs)
        if xs:
            fail = HoretuCouldNotParse('Extra arguments -- %s' % ' '.join(xs))

    if fail == None:
        return args
    else:
        return fail

def reify_kwargs(s, str_kwargs):
    kwargs = {}
    for name, value in str_kwargs:
        a = s.keyword2.get(name)
        if a:
            try:
                kwargs[name] = a.call(value)
            except ValueError as e:
                return HoretuCouldNotParse(e.args[0])
            except HoretuException as e:
                return e
    return kwargs

def _with_defaults(f, defaults, sig):
    def w(*args, **kwargs):
        for key, value in defaults.items():
            if key in sig.keyword2 and key not in kwargs:
                kwargs[key] = sig.keyword2[key].call(value)
        return f(*args, **kwargs)
    return w
