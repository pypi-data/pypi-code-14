# -*- coding: utf-8 -*-

from six import raise_from

from grako.model import ModelBuilderSemantics
from grako.exceptions import ParseError as GrakoParseError

from b3j0f.utils.runtime import singleton_per_scope

from j1bz.expression.walker import Walker
from j1bz.expression.parser import get_parser
from j1bz.expression.exceptions import ParseError


def interpret(expression, **kwargs):
    return singleton_per_scope(Interpreter, **kwargs).interpret(expression)


class Interpreter(object):
    def __init__(
            self,
            parser=None, walker=None,
            pkwargs={'rule_name': 'start'}, wkwargs={},
            grammar_file=None
    ):
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
        try:
            model = self.parser.parse(expression, **self.pkwargs)
        except GrakoParseError as e:
            raise_from(ParseError("Failed to parse"), e)

        res = self.walker.walk(model, **self.wkwargs)

        return res
