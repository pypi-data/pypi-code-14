# -*- coding: utf-8 -*-

from sys import modules
from imp import new_module
from six import exec_, raise_from

from grako.tool import genmodel
from grako.exceptions import GrakoException
from grako.codegen.python import codegen as pythoncg

from j1bz.expression.default_parser import ExpressionParser as DefaultParser
from j1bz.expression.exceptions import ParserGenerationError


def get_parser(grammar_file=None, **kwargs):
    """
    Get a grako parser.

    :param grammar_file: Grako-bnf grammar file. If None, return a default
      parser from package sources. If string, try to generate a parser at
      runtime with this file.
    :type filename: str or None
    :param dict kwargs: Custom parameters given to parser constructor

    :return: Grako parser
    :rtype: grako.parsing.Parser

    :raises j1bz.expression.ParserGenerationError: when parser generation
      failed (bad grammar)
    :raises IOError: when filename cannot be read
    :raises OSError: when filename cannot be read
    :raises FileNotFoundError: when filename does not exist
    """

    if grammar_file is None:
        return DefaultParser(**kwargs)

    with open(grammar_file) as f:
        grammar = f.read()

        try:
            model = genmodel('Expression', grammar, filename=grammar_file)
            code = pythoncg(model)

        except GrakoException as e:
            err = ("Error trying to generate grako parser. Is your grammar {} "
                   "correct ?".format(grammar_file))
            raise_from(ParserGenerationError(err), e)

    dynamic_name = ('j1bz.expression.dynamic_parser')
    module = new_module(dynamic_name)
    exec_(code, module.__dict__)
    modules[dynamic_name] = module

    from j1bz.expression.dynamic_parser import ExpressionParser

    return ExpressionParser(**kwargs)
