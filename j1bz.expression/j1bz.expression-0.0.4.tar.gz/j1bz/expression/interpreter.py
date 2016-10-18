# -*- coding: utf-8 -*-

from six import raise_from

from grako.model import ModelBuilderSemantics
from grako.exceptions import ParseError as GrakoParseError

from b3j0f.utils.runtime import singleton_per_scope

from j1bz.expression.walker import Walker
from j1bz.expression.parser import get_parser
from j1bz.expression.exceptions import ParseError


def interpret(expression, **kwargs):
    """
    Wrapper for Interpreter.interpret, allowing to interpret expressions
    without having to instanciate a Interpreter class.

    An Intepreter is instantiated as a singleton (per scope).

    :param str expression: Expression to interpret
    :param dict kwargs: Given to Interpreter constructor the first time it is
      instantiated

    :return: Serialized CRUD request
    :rtype: b3j0f.requester.request.crud.{create,read,update,delete},
      depending on expression nature

    :raises j1bz.expression.exceptions.ParseError: If expression is not
      correct
    :raises j1bz.expression.ParserGenerationError: If grammar_file has been
      passed in kwargs and parser generation failed (bad grammar)
    """

    return singleton_per_scope(Interpreter, **kwargs).interpret(expression)


class Interpreter(object):
    def __init__(
            self,
            parser=None, walker=None,
            pkwargs={'rule_name': 'start'}, wkwargs={},
            grammar_file=None
    ):
        """
        Caches a parser and a walker.

        :param parser: Parser used to transform expressions to a grako AST
        :type parser: grako.parsing.Parser (or subclass) or None
        :param walker: Walker used to browse AST and serialize an object
          representing the expression
        :type walker: grako.model.Walker (or subclass) or None

        :param dict pkwargs: Additional parameters given to each parser.parse
          call (mostly for start_rule configurability)
        :param dict wkwargs: Additional parameters given to each walker.walk
          call (mostly for consistency with pkwargs)

        :param grammar_file: Grako-bnf grammar file. If None **AND** parser is
          None, uses a default parser from package sources. If string, generate
          a parser at runtime with this file.
        :type grammar_file: str or None

        :raises j1bz.expression.ParserGenerationError: If grammar_file is not
          None and parser generation failed (bad grammar)
        :raises IOError: when grammar_file cannot be read
        :raises OSError: when filename grammar_file be read
        :raises FileNotFoundError: when grammar_file does not exist
        """

        if parser:
            self.parser = parser
        else:
            self.parser = get_parser(
                grammar_file=grammar_file,
                semantics=ModelBuilderSemantics()
            )

        if walker:
            self.walker = walker
        else:
            self.walker = Walker()

        self.pkwargs = pkwargs
        self.wkwargs = wkwargs

    def interpret(self, expression):
        """
        Interpret an expression via a grako.model.NodeWalker subclass.

        :param str expression: Expression to interpret

        :return: Serialized CRUD request
        :rtype: b3j0f.requester.request.crud.{create,read,update,delete},
          depending on expression nature

        :raises j1bz.expression.exceptions.ParseError: If expression is not
          correct
        """

        try:
            model = self.parser.parse(expression, **self.pkwargs)

        except GrakoParseError as e:
            raise_from(ParseError("Failed to parse"), e)

        res = self.walker.walk(model, **self.wkwargs)

        return res
