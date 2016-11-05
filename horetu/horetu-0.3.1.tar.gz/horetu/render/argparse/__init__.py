import argparse
import sys
import os
from functools import partial
from itertools import chain

from ...signature import Signature
from ..doc import Doc
from .one import one
from . import options

def update_parser(f, p):
    '''
    :param f: Function
    :param argparse.ArgumentParser p: Parser
    '''
    subcommand_dest = 'subcommands'
    defaults = {}

    p.formatter_class=argparse.RawDescriptionHelpFormatter
    if hasattr(f, '__call__'):
        if p.description is None:
            p.description = Doc(f).desc
        one(p, f)
    elif isinstance(f, (dict, list)):
        raise ValueError('Subcommands are not allowed in the argparse/django interface.')
    else:
        raise TypeError('f must be callable.')

def evaluate(f, args, options):
    args = list(args)
    kwargs = {}

    s = Signature(f, with_help=False)
    for annotation in s.positional:
        args.append(options[annotation.name])
    if s.var_positional:
        args.extend(options[s.var_positional.name])
    for annotation in s.keyword1:
        kwargs[annotation.name] = options[annotation.name]
    for annotation in s.keyword2.values():
        kwargs[annotation.name] = options[annotation.name]

    return f(*args, **kwargs)
