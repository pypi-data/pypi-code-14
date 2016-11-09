# encoding:utf-8

"""
The :mod:`parser` module concerns itself with parsing Python source.
"""

from __future__ import absolute_import, division, print_function, unicode_literals
from functools import reduce
from .. import source, diagnostic, lexer, ast

# A few notes about our approach to parsing:
#
# Python uses an LL(1) parser generator. It's a bit weird, because
# the usual reason to choose LL(1) is to make a handwritten parser
# possible, however Python's grammar is formulated in a way that
# is much more easily recognized if you make an FSM rather than
# the usual "if accept(token)..." ladder. So in a way it is
# the worst of both worlds.
#
# We don't use a parser generator because we want to have an unified
# grammar for all Python versions, and also have grammar coverage
# analysis and nice error recovery. To make the grammar compact,
# we use combinators to compose it from predefined fragments,
# such as "sequence" or "alternation" or "Kleene star". This easily
# gives us one token of lookahead in most cases, but e.g. not
# in the following one:
#
#     argument: test | test '=' test
#
# There are two issues with this. First, in an alternation, the first
# variant will be tried (and accepted) earlier. Second, if we reverse
# them, by the point it is clear ``'='`` will not be accepted, ``test``
# has already been consumed.
#
# The way we fix this is by reordering rules so that longest match
# comes first, and adding backtracking on alternations (as well as
# plus and star, since those have a hidden alternation inside).
#
# While backtracking can in principle make asymptotical complexity
# worse, it never makes parsing syntactically correct code supralinear
# with Python's LL(1) grammar, and we could not come up with any
# pathological incorrect input as well.

# Coverage data
_all_rules = []
_all_stmts = {(12480,12483): False, (12795,12798): False, (12844,12847): False, (12960,12962): False, (13126,13130): False, (13262,13266): False, (13381,13384): False, (13434,13436): False, (13589,13592): False, (13631,13633): False, (13816,13819): False, (13858,13860): False, (13902,13904): False, (14049,14053): False, (14964,14968): False, (15042,15044): False, (15140,15144): False, (15646,15648): False, (16103,16107): False, (16545,16547): False, (16637,16641): False, (16863,16866): False, (17146,17148): False, (17193,17195): False, (17248,17250): False, (17307,17309): False, (17368,17370): False, (17429,17431): False, (17945,17948): False, (18029,18031): False, (18223,18226): False, (18393,18396): False, (18459,18461): False, (18630,18634): False, (18668,18671): False, (18722,18724): False, (18906,18910): False, (19121,19125): False, (19139,19141): False, (19288,19292): False, (19475,19478): False, (19511,19513): False, (19751,19754): False, (19882,19884): False, (20060,20063): False, (20217,20219): False, (20394,20397): False, (20732,20735): False, (20970,20972): False, (21284,21287): False, (21721,21724): False, (22374,22377): False, (22571,22573): False, (23404,23407): False, (23708,23711): False, (23894,23896): False, (24215,24218): False, (24516,24519): False, (24788,24791): False, (24836,24838): False, (25012,25016): False, (25352,25355): False, (25401,25403): False, (25531,25535): False, (25580,25582): False, (25687,25691): False, (25824,25827): False, (26218,26221): False, (26388,26391): False, (26762,26765): False, (26966,26968): False, (27205,27208): False, (27257,27259): False, (27445,27449): False, (27550,27552): False, (27635,27639): False, (28094,28097): False, (28162,28164): False, (28409,28413): False, (28685,28688): False, (28739,28742): False, (28791,28793): False, (28983,28987): False, (29347,29350): False, (29400,29402): False, (29542,29546): False, (29599,29601): False, (29714,29718): False, (31177,31180): False, (31275,31277): False, (31554,31557): False, (32727,32730): False, (32914,32917): False, (32950,32952): False, (33138,33142): False, (33242,33245): False, (33613,33615): False, (33660,33662): False, (33956,33960): False, (34109,34113): False, (34287,34291): False, (35146,35149): False, (35225,35227): False, (35510,35513): False, (35616,35618): False, (35877,35880): False, (36256,36259): False, (36672,36675): False, (37059,37062): False, (37220,37223): False, (37419,37422): False, (37538,37540): False, (37722,37725): False, (38053,38056): False, (38242,38244): False, (38344,38346): False, (38456,38458): False, (38753,38756): False, (38931,38933): False, (39028,39030): False, (39450,39453): False, (39696,39699): False, (39777,39780): False, (39913,39916): False, (40004,40006): False, (40240,40243): False, (40447,40450): False, (40714,40717): False, (41040,41043): False, (41654,41656): False, (41820,41822): False, (41883,41885): False, (42342,42345): False, (42522,42524): False, (42932,42935): False, (43181,43183): False, (43855,43858): False, (44123,44126): False, (44606,44609): False, (44819,44821): False, (44887,44889): False, (44953,44957): False, (45220,45223): False, (45655,45658): False, (45801,45803): False, (46150,46153): False, (46561,46564): False, (46818,46820): False, (46911,46914): False, (47085,47087): False, (47450,47452): False, (47683,47686): False, (48090,48092): False, (48439,48442): False, (48902,48904): False, (49277,49280): False, (49361,49364): False, (49646,49648): False, (49824,49826): False, (50306,50309): False, (50728,50731): False, (51275,51278): False, (51425,51427): False, (51662,51666): False, (52185,52188): False, (52569,52572): False, (52669,52671): False, (52902,52906): False, (53106,53109): False, (53232,53235): False, (53442,53445): False, (53721,53723): False, (53821,53823): False, (53905,53907): False, (54020,54024): False, (54374,54377): False, (55026,55029): False, (55170,55172): False, (55644,55647): False, (55684,55686): False, (56164,56167): False, (56237,56239): False, (56996,56999): False, (57082,57084): False, (57361,57365): False, (57471,57474): False, (57560,57562): False, (57840,57844): False, (57931,57934): False, (58430,58433): False, (58656,58658): False, (58898,58902): False, (58978,58981): False, (59074,59076): False, (59285,59288): False, (60986,60989): False, (61310,61313): False, (61412,61415): False, (61449,61451): False, (61575,61579): False, (61735,61737): False, (61984,61987): False, (62085,62088): False, (62233,62236): False, (62375,62378): False, (62624,62627): False, (64003,64006): False, (64125,64128): False, (64156,64158): False, (64212,64216): False, (64270,64274): False, (65231,65234): False, (65276,65278): False, (65329,65333): False, (65462,65466): False, (65619,65622): False, (65785,65788): False, (66189,66192): False, (66374,66377): False, (66415,66417): False, (66490,66494): False, (66964,66967): False, (67151,67154): False, (67515,67518): False, (68083,68086): False, (68190,68192): False, (68297,68301): False, (68734,68738): False, (68998,69001): False, (69205,69208): False, (69303,69305): False, (69367,69369): False, (69468,69470): False, (69580,69582): False, (69823,69826): False, (70487,70490): False, (70820,70823): False, (71019,71022): False, (71570,71573): False, (71619,71621): False, (71937,71941): False, (72300,72303): False, (72349,72351): False, (72471,72475): False, (73019,73022): False, (73234,73236): False, (73948,73951): False, (74266,74268): False, (75089,75092): False, (75309,75312): False, (75411,75413): False, (75478,75481): False, (75515,75517): False, (76027,76030): False, (76286,76289): False, (76517,76520): False, (77054,77057): False, (77099,77101): False, (77186,77190): False, (77452,77456): False, (77562,77565): False, (77609,77612): False, (77637,77639): False, (78091,78094): False, (78134,78137): False, (78162,78164): False, (78552,78555): False, (78958,78961): False, (79039,79042): False, (79293,79295): False, (79366,79370): False, (79438,79441): False, (79501,79504): False, (79719,79721): False, (79792,79796): False, (81329,81332): False, (81452,81454): False, (81605,81609): False, (81777,81780): False, (81880,81882): False, (82034,82038): False, (82183,82187): False, (82344,82347): False}

# Generic LL parsing combinators
class Unmatched:
    pass

unmatched = Unmatched()

def llrule(loc, expected, cases=1):
    if loc is None:
        def decorator(rule):
            rule.expected = expected
            return rule
    else:
        def decorator(inner_rule):
            if cases == 1:
                def rule(*args, **kwargs):
                    result = inner_rule(*args, **kwargs)
                    if result is not unmatched:
                        rule.covered[0] = True
                    return result
            else:
                rule = inner_rule

            rule.loc, rule.expected, rule.covered = \
                loc, expected, [False] * cases
            _all_rules.append(rule)

            return rule
    return decorator

def action(inner_rule, loc=None):
    """
    A decorator returning a function that first runs ``inner_rule`` and then, if its
    return value is not None, maps that value using ``mapper``.

    If the value being mapped is a tuple, it is expanded into multiple arguments.

    Similar to attaching semantic actions to rules in traditional parser generators.
    """
    def decorator(mapper):
        @llrule(loc, inner_rule.expected)
        def outer_rule(parser):
            result = inner_rule(parser)
            if result is unmatched:
                return result
            if isinstance(result, tuple):
                return mapper(parser, *result)
            else:
                return mapper(parser, result)
        return outer_rule
    return decorator

def Eps(value=None, loc=None):
    """A rule that accepts no tokens (epsilon) and returns ``value``."""
    @llrule(loc, lambda parser: [])
    def rule(parser):
        return value
    return rule

def Tok(kind, loc=None):
    """A rule that accepts a token of kind ``kind`` and returns it, or returns None."""
    @llrule(loc, lambda parser: [kind])
    def rule(parser):
        return parser._accept(kind)
    return rule

def Loc(kind, loc=None):
    """A rule that accepts a token of kind ``kind`` and returns its location, or returns None."""
    @llrule(loc, lambda parser: [kind])
    def rule(parser):
        result = parser._accept(kind)
        if result is unmatched:
            return result
        return result.loc
    return rule

def Rule(name, loc=None):
    """A proxy for a rule called ``name`` which may not be yet defined."""
    @llrule(loc, lambda parser: getattr(parser, name).expected(parser))
    def rule(parser):
        return getattr(parser, name)()
    return rule

def Expect(inner_rule, loc=None):
    """A rule that executes ``inner_rule`` and emits a diagnostic error if it returns None."""
    @llrule(loc, inner_rule.expected)
    def rule(parser):
        result = inner_rule(parser)
        if result is unmatched:
            expected = reduce(list.__add__, [rule.expected(parser) for rule in parser._errrules])
            expected = list(sorted(set(expected)))

            if len(expected) > 1:
                expected = " or ".join([", ".join(expected[0:-1]), expected[-1]])
            elif len(expected) == 1:
                expected = expected[0]
            else:
                expected = "(impossible)"

            error_tok = parser._tokens[parser._errindex]
            error = diagnostic.Diagnostic(
                "fatal", "unexpected {actual}: expected {expected}",
                {"actual": error_tok.kind, "expected": expected},
                error_tok.loc)
            parser.diagnostic_engine.process(error)
        return result
    return rule

def Seq(first_rule, *rest_of_rules, **kwargs):
    """
    A rule that accepts a sequence of tokens satisfying ``rules`` and returns a tuple
    containing their return values, or None if the first rule was not satisfied.
    """
    @llrule(kwargs.get("loc", None), first_rule.expected)
    def rule(parser):
        result = first_rule(parser)
        if result is unmatched:
            return result

        results = [result]
        for rule in rest_of_rules:
            result = rule(parser)
            if result is unmatched:
                return result
            results.append(result)
        return tuple(results)
    return rule

def SeqN(n, *inner_rules, **kwargs):
    """
    A rule that accepts a sequence of tokens satisfying ``rules`` and returns
    the value returned by rule number ``n``, or None if the first rule was not satisfied.
    """
    @action(Seq(*inner_rules), loc=kwargs.get("loc", None))
    def rule(parser, *values):
        return values[n]
    return rule

def Alt(*inner_rules, **kwargs):
    """
    A rule that expects a sequence of tokens satisfying one of ``rules`` in sequence
    (a rule is satisfied when it returns anything but None) and returns the return
    value of that rule, or None if no rules were satisfied.
    """
    loc = kwargs.get("loc", None)
    expected = lambda parser: reduce(list.__add__, map(lambda x: x.expected(parser), inner_rules))
    if loc is not None:
        @llrule(loc, expected, cases=len(inner_rules))
        def rule(parser):
            data = parser._save()
            for idx, inner_rule in enumerate(inner_rules):
                result = inner_rule(parser)
                if result is unmatched:
                    parser._restore(data, rule=inner_rule)
                else:
                    rule.covered[idx] = True
                    return result
            return unmatched
    else:
        @llrule(loc, expected, cases=len(inner_rules))
        def rule(parser):
            data = parser._save()
            for inner_rule in inner_rules:
                result = inner_rule(parser)
                if result is unmatched:
                    parser._restore(data, rule=inner_rule)
                else:
                    return result
            return unmatched
    return rule

def Opt(inner_rule, loc=None):
    """Shorthand for ``Alt(inner_rule, Eps())``"""
    return Alt(inner_rule, Eps(), loc=loc)

def Star(inner_rule, loc=None):
    """
    A rule that accepts a sequence of tokens satisfying ``inner_rule`` zero or more times,
    and returns the returned values in a :class:`list`.
    """
    @llrule(loc, lambda parser: [])
    def rule(parser):
        results = []
        while True:
            data = parser._save()
            result = inner_rule(parser)
            if result is unmatched:
                parser._restore(data, rule=inner_rule)
                return results
            results.append(result)
    return rule

def Plus(inner_rule, loc=None):
    """
    A rule that accepts a sequence of tokens satisfying ``inner_rule`` one or more times,
    and returns the returned values in a :class:`list`.
    """
    @llrule(loc, inner_rule.expected)
    def rule(parser):
        result = inner_rule(parser)
        if result is unmatched:
            return result

        results = [result]
        while True:
            data = parser._save()
            result = inner_rule(parser)
            if result is unmatched:
                parser._restore(data, rule=inner_rule)
                return results
            results.append(result)
    return rule

class commalist(list):
    __slots__ = ("trailing_comma",)

def List(inner_rule, separator_tok, trailing, leading=True, loc=None):
    if not trailing:
        @action(Seq(inner_rule, Star(SeqN(1, Tok(separator_tok), inner_rule))), loc=loc)
        def outer_rule(parser, first, rest):
            return [first] + rest
        return outer_rule
    else:
        # A rule like this: stmt (';' stmt)* [';']
        # This doesn't yield itself to combinators above, because disambiguating
        # another iteration of the Kleene star and the trailing separator
        # requires two lookahead tokens (naively).
        separator_rule = Tok(separator_tok)
        @llrule(loc, inner_rule.expected)
        def rule(parser):
            results = commalist()

            if leading:
                result = inner_rule(parser)
                if result is unmatched:
                    return result
                else:
                    results.append(result)

            while True:
                result = separator_rule(parser)
                if result is unmatched:
                    results.trailing_comma = None
                    return results

                result_1 = inner_rule(parser)
                if result_1 is unmatched:
                    results.trailing_comma = result
                    return results
                else:
                    results.append(result_1)
        return rule

# Python AST specific parser combinators
def Newline(loc=None):
    """A rule that accepts token of kind ``newline`` and returns an empty list."""
    @llrule(loc, lambda parser: ["newline"])
    def rule(parser):
        result = parser._accept("newline")
        if result is unmatched:
            return result
        return []
    return rule

def Oper(klass, *kinds, **kwargs):
    """
    A rule that accepts a sequence of tokens of kinds ``kinds`` and returns
    an instance of ``klass`` with ``loc`` encompassing the entire sequence
    or None if the first token is not of ``kinds[0]``.
    """
    @action(Seq(*map(Loc, kinds)), loc=kwargs.get("loc", None))
    def rule(parser, *tokens):
        return klass(loc=tokens[0].join(tokens[-1]))
    return rule

def BinOper(expr_rulename, op_rule, node=ast.BinOp, loc=None):
    @action(Seq(Rule(expr_rulename), Star(Seq(op_rule, Rule(expr_rulename)))), loc=loc)
    def rule(parser, lhs, trailers):
        for (op, rhs) in trailers:
            lhs = node(left=lhs, op=op, right=rhs,
                       loc=lhs.loc.join(rhs.loc))
        return lhs
    return rule

def BeginEnd(begin_tok, inner_rule, end_tok, empty=None, loc=None):
    @action(Seq(Loc(begin_tok), inner_rule, Loc(end_tok)), loc=loc)
    def rule(parser, begin_loc, node, end_loc):
        if node is None:
            node = empty(parser)

        # Collection nodes don't have loc yet. If a node has loc at this
        # point, it means it's an expression passed in parentheses.
        if node.loc is None and type(node) in [
                ast.List, ast.ListComp,
                ast.Dict, ast.DictComp,
                ast.Set, ast.SetComp,
                ast.GeneratorExp,
                ast.Tuple, ast.Repr,
                ast.Call, ast.Subscript,
                ast.arguments]:
            node.begin_loc, node.end_loc, node.loc = \
                begin_loc, end_loc, begin_loc.join(end_loc)
        return node
    return rule

class Parser:

    # Generic LL parsing methods
    def __init__(self, lexer, version, diagnostic_engine):
        _all_stmts[(12480,12483)] = True
        self._init_version(version)
        self.diagnostic_engine = diagnostic_engine

        self.lexer     = lexer
        self._tokens   = []
        self._index    = -1
        self._errindex = -1
        self._errrules = []
        self._advance()

    def _save(self):
        _all_stmts[(12795,12798)] = True
        return self._index

    def _restore(self, data, rule):
        _all_stmts[(12844,12847)] = True
        self._index = data
        self._token = self._tokens[self._index]

        if self._index > self._errindex:
            # We have advanced since last error
            _all_stmts[(12960,12962)] = True
            self._errindex = self._index
            self._errrules = [rule]
        elif self._index == self._errindex:
            # We're at the same place as last error
            _all_stmts[(13126,13130)] = True
            self._errrules.append(rule)
        else:
            # We've backtracked far and are now just failing the
            # whole parse
            _all_stmts[(13262,13266)] = True
            pass

    def _advance(self):
        _all_stmts[(13381,13384)] = True
        self._index += 1
        if self._index == len(self._tokens):
            _all_stmts[(13434,13436)] = True
            self._tokens.append(self.lexer.next(eof_token=True))
        self._token = self._tokens[self._index]

    def _accept(self, expected_kind):
        _all_stmts[(13589,13592)] = True
        if self._token.kind == expected_kind:
            _all_stmts[(13631,13633)] = True
            result = self._token
            self._advance()
            return result
        return unmatched

    # Python-specific methods
    def _init_version(self, version):
        _all_stmts[(13816,13819)] = True
        if version in ((2, 6), (2, 7)):
            _all_stmts[(13858,13860)] = True
            if version == (2, 6):
                _all_stmts[(13902,13904)] = True
                self.with_stmt       = self.with_stmt__26
                self.atom_6          = self.atom_6__26
            else:
                _all_stmts[(14049,14053)] = True
                self.with_stmt       = self.with_stmt__27
                self.atom_6          = self.atom_6__27
            self.except_clause_1 = self.except_clause_1__26
            self.classdef        = self.classdef__26
            self.subscript       = self.subscript__26
            self.raise_stmt      = self.raise_stmt__26
            self.comp_if         = self.comp_if__26
            self.atom            = self.atom__26
            self.funcdef         = self.funcdef__26
            self.parameters      = self.parameters__26
            self.varargslist     = self.varargslist__26
            self.comparison_1    = self.comparison_1__26
            self.exprlist_1      = self.exprlist_1__26
            self.testlist_comp_1 = self.testlist_comp_1__26
            self.expr_stmt_1     = self.expr_stmt_1__26
            self.yield_expr      = self.yield_expr__26
            return
        elif version in ((3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5)):
            _all_stmts[(14964,14968)] = True
            if version == (3, 0):
                _all_stmts[(15042,15044)] = True
                self.with_stmt       = self.with_stmt__26 # lol
            else:
                _all_stmts[(15140,15144)] = True
                self.with_stmt       = self.with_stmt__27
            self.except_clause_1 = self.except_clause_1__30
            self.classdef        = self.classdef__30
            self.subscript       = self.subscript__30
            self.raise_stmt      = self.raise_stmt__30
            self.comp_if         = self.comp_if__30
            self.atom            = self.atom__30
            self.funcdef         = self.funcdef__30
            self.parameters      = self.parameters__30
            if version < (3, 2):
                _all_stmts[(15646,15648)] = True
                self.varargslist     = self.varargslist__30
                self.typedargslist   = self.typedargslist__30
                self.comparison_1    = self.comparison_1__30
                self.star_expr       = self.star_expr__30
                self.exprlist_1      = self.exprlist_1__30
                self.testlist_comp_1 = self.testlist_comp_1__26
                self.expr_stmt_1     = self.expr_stmt_1__26
            else:
                _all_stmts[(16103,16107)] = True
                self.varargslist     = self.varargslist__32
                self.typedargslist   = self.typedargslist__32
                self.comparison_1    = self.comparison_1__32
                self.star_expr       = self.star_expr__32
                self.exprlist_1      = self.exprlist_1__32
                self.testlist_comp_1 = self.testlist_comp_1__32
                self.expr_stmt_1     = self.expr_stmt_1__32
            if version < (3, 3):
                _all_stmts[(16545,16547)] = True
                self.yield_expr      = self.yield_expr__26
            else:
                _all_stmts[(16637,16641)] = True
                self.yield_expr      = self.yield_expr__33
            return

        raise NotImplementedError("pythonparser.parser.Parser cannot parse Python %s" %
                                  str(version))

    def _arguments(self, args=None, defaults=None, kwonlyargs=None, kw_defaults=None,
                   vararg=None, kwarg=None,
                   star_loc=None, dstar_loc=None, begin_loc=None, end_loc=None,
                   equals_locs=None, kw_equals_locs=None, loc=None):
        _all_stmts[(16863,16866)] = True
        if args is None:
            _all_stmts[(17146,17148)] = True
            args = []
        if defaults is None:
            _all_stmts[(17193,17195)] = True
            defaults = []
        if kwonlyargs is None:
            _all_stmts[(17248,17250)] = True
            kwonlyargs = []
        if kw_defaults is None:
            _all_stmts[(17307,17309)] = True
            kw_defaults = []
        if equals_locs is None:
            _all_stmts[(17368,17370)] = True
            equals_locs = []
        if kw_equals_locs is None:
            _all_stmts[(17429,17431)] = True
            kw_equals_locs = []
        return ast.arguments(args=args, defaults=defaults,
                             kwonlyargs=kwonlyargs, kw_defaults=kw_defaults,
                             vararg=vararg, kwarg=kwarg,
                             star_loc=star_loc, dstar_loc=dstar_loc,
                             begin_loc=begin_loc, end_loc=end_loc,
                             equals_locs=equals_locs, kw_equals_locs=kw_equals_locs,
                             loc=loc)

    def _arg(self, tok, colon_loc=None, annotation=None):
        _all_stmts[(17945,17948)] = True
        loc = tok.loc
        if annotation:
            _all_stmts[(18029,18031)] = True
            loc = loc.join(annotation.loc)
        return ast.arg(arg=tok.value, annotation=annotation,
                       arg_loc=tok.loc, colon_loc=colon_loc, loc=loc)

    def _empty_arglist(self):
        _all_stmts[(18223,18226)] = True
        return ast.Call(args=[], keywords=[], starargs=None, kwargs=None,
                        star_loc=None, dstar_loc=None, loc=None)

    def _wrap_tuple(self, elts):
        _all_stmts[(18393,18396)] = True
        assert len(elts) > 0
        if len(elts) > 1:
            _all_stmts[(18459,18461)] = True
            return ast.Tuple(ctx=None, elts=elts,
                             loc=elts[0].loc.join(elts[-1].loc), begin_loc=None, end_loc=None)
        else:
            _all_stmts[(18630,18634)] = True
            return elts[0]

    def _assignable(self, node, is_delete=False):
        _all_stmts[(18668,18671)] = True
        if isinstance(node, ast.Name) or isinstance(node, ast.Subscript) or \
                isinstance(node, ast.Attribute) or isinstance(node, ast.Starred):
            _all_stmts[(18722,18724)] = True
            return node
        elif (isinstance(node, ast.List) or isinstance(node, ast.Tuple)) and \
                any(node.elts):
            _all_stmts[(18906,18910)] = True
            node.elts = [self._assignable(elt, is_delete) for elt in node.elts]
            return node
        else:
            _all_stmts[(19121,19125)] = True
            if is_delete:
                _all_stmts[(19139,19141)] = True
                error = diagnostic.Diagnostic(
                    "fatal", "cannot delete this expression", {}, node.loc)
            else:
                _all_stmts[(19288,19292)] = True
                error = diagnostic.Diagnostic(
                    "fatal", "cannot assign to this expression", {}, node.loc)
            self.diagnostic_engine.process(error)

    def add_flags(self, flags):
        _all_stmts[(19475,19478)] = True
        if "print_function" in flags:
            _all_stmts[(19511,19513)] = True
            self.lexer.print_function = True

    # Grammar
    @action(Expect(Alt(Newline(loc=(19624,19631)),
                       Rule("simple_stmt", loc=(19658,19662)),
                       SeqN(0, Rule("compound_stmt", loc=(19710,19714)), Newline(loc=(19733,19740)), loc=(19702,19706)), loc=(19620,19623)), loc=(19613,19619)), loc=(19606,19612))
    def single_input(self, body):
        _all_stmts[(19751,19754)] = True
        """single_input: NEWLINE | simple_stmt | compound_stmt NEWLINE"""
        loc = None
        if body != []:
            _all_stmts[(19882,19884)] = True
            loc = body[0].loc
        return ast.Interactive(body=body, loc=loc)

    @action(Expect(SeqN(0, Star(Alt(Newline(loc=(20015,20022)), Rule("stmt", loc=(20026,20030)), loc=(20011,20014)), loc=(20006,20010)), Tok("eof", loc=(20042,20045)), loc=(19998,20002)), loc=(19991,19997)), loc=(19984,19990))
    def file_input(parser, body):
        _all_stmts[(20060,20063)] = True
        """file_input: (NEWLINE | stmt)* ENDMARKER"""
        body = reduce(list.__add__, body, [])
        loc = None
        if body != []:
            _all_stmts[(20217,20219)] = True
            loc = body[0].loc
        return ast.Module(body=body, loc=loc)

    @action(Expect(SeqN(0, Rule("testlist", loc=(20336,20340)), Star(Tok("newline", loc=(20359,20362)), loc=(20354,20358)), Tok("eof", loc=(20376,20379)), loc=(20328,20332)), loc=(20321,20327)), loc=(20314,20320))
    def eval_input(self, expr):
        _all_stmts[(20394,20397)] = True
        """eval_input: testlist NEWLINE* ENDMARKER"""
        return ast.Expression(body=[expr], loc=expr.loc)

    @action(Seq(Loc("@", loc=(20550,20553)), Rule("dotted_name", loc=(20560,20564)),
                Opt(BeginEnd("(", Opt(Rule("arglist", loc=(20619,20623)), loc=(20615,20618)), ")",
                             empty=_empty_arglist, loc=(20601,20609)), loc=(20597,20600)),
                Loc("newline", loc=(20711,20714)), loc=(20546,20549)), loc=(20539,20545))
    def decorator(self, at_loc, dotted_name, call_opt, newline_loc):
        _all_stmts[(20732,20735)] = True
        """decorator: '@' dotted_name [ '(' [arglist] ')' ] NEWLINE"""
        name_loc, name = dotted_name
        expr = ast.Name(id=name, ctx=None, loc=name_loc)
        if call_opt:
            _all_stmts[(20970,20972)] = True
            call_opt.func = expr
            call_opt.loc = name_loc.join(call_opt.loc)
            expr = call_opt
        return at_loc, expr

    decorators = Plus(Rule("decorator", loc=(21150,21154)), loc=(21145,21149))
    """decorators: decorator+"""

    @action(Seq(Rule("decorators", loc=(21219,21223)), Alt(Rule("classdef", loc=(21243,21247)), Rule("funcdef", loc=(21261,21265)), loc=(21239,21242)), loc=(21215,21218)), loc=(21208,21214))
    def decorated(self, decorators, classfuncdef):
        _all_stmts[(21284,21287)] = True
        """decorated: decorators (classdef | funcdef)"""
        classfuncdef.at_locs = list(map(lambda x: x[0], decorators))
        classfuncdef.decorator_list = list(map(lambda x: x[1], decorators))
        classfuncdef.loc = classfuncdef.loc.join(decorators[0][0])
        return classfuncdef

    @action(Seq(Loc("def", loc=(21645,21648)), Tok("ident", loc=(21657,21660)), Rule("parameters", loc=(21671,21675)), Loc(":", loc=(21691,21694)), Rule("suite", loc=(21701,21705)), loc=(21641,21644)), loc=(21634,21640))
    def funcdef__26(self, def_loc, ident_tok, args, colon_loc, suite):
        _all_stmts[(21721,21724)] = True
        """(2.6, 2.7) funcdef: 'def' NAME parameters ':' suite"""
        return ast.FunctionDef(name=ident_tok.value, args=args, returns=None,
                               body=suite, decorator_list=[],
                               at_locs=[], keyword_loc=def_loc, name_loc=ident_tok.loc,
                               colon_loc=colon_loc, arrow_loc=None,
                               loc=def_loc.join(suite[-1].loc))

    @action(Seq(Loc("def", loc=(22231,22234)), Tok("ident", loc=(22243,22246)), Rule("parameters", loc=(22257,22261)),
                Opt(Seq(Loc("->", loc=(22301,22304)), Rule("test", loc=(22312,22316)), loc=(22297,22300)), loc=(22293,22296)),
                Loc(":", loc=(22344,22347)), Rule("suite", loc=(22354,22358)), loc=(22227,22230)), loc=(22220,22226))
    def funcdef__30(self, def_loc, ident_tok, args, returns_opt, colon_loc, suite):
        _all_stmts[(22374,22377)] = True
        """(3.0-) funcdef: 'def' NAME parameters ['->' test] ':' suite"""
        arrow_loc = returns = None
        if returns_opt:
            _all_stmts[(22571,22573)] = True
            arrow_loc, returns = returns_opt
        return ast.FunctionDef(name=ident_tok.value, args=args, returns=returns,
                               body=suite, decorator_list=[],
                               at_locs=[], keyword_loc=def_loc, name_loc=ident_tok.loc,
                               colon_loc=colon_loc, arrow_loc=arrow_loc,
                               loc=def_loc.join(suite[-1].loc))

    parameters__26 = BeginEnd("(", Opt(Rule("varargslist", loc=(23040,23044)), loc=(23036,23039)), ")", empty=_arguments, loc=(23022,23030))
    """(2.6, 2.7) parameters: '(' [varargslist] ')'"""

    parameters__30 = BeginEnd("(", Opt(Rule("typedargslist", loc=(23180,23184)), loc=(23176,23179)), ")", empty=_arguments, loc=(23162,23170))
    """(3.0) parameters: '(' [typedargslist] ')'"""

    varargslist__26_1 = Seq(Rule("fpdef", loc=(23308,23312)), Opt(Seq(Loc("=", loc=(23331,23334)), Rule("test", loc=(23341,23345)), loc=(23327,23330)), loc=(23323,23326)), loc=(23304,23307))

    @action(Seq(Loc("**", loc=(23374,23377)), Tok("ident", loc=(23385,23388)), loc=(23370,23373)), loc=(23363,23369))
    def varargslist__26_2(self, dstar_loc, kwarg_tok):
        _all_stmts[(23404,23407)] = True
        return self._arguments(kwarg=self._arg(kwarg_tok),
                               dstar_loc=dstar_loc, loc=dstar_loc.join(kwarg_tok.loc))

    @action(Seq(Loc("*", loc=(23618,23621)), Tok("ident", loc=(23628,23631)),
                Opt(Seq(Tok(",", loc=(23666,23669)), Loc("**", loc=(23676,23679)), Tok("ident", loc=(23687,23690)), loc=(23662,23665)), loc=(23658,23661)), loc=(23614,23617)), loc=(23607,23613))
    def varargslist__26_3(self, star_loc, vararg_tok, kwarg_opt):
        _all_stmts[(23708,23711)] = True
        dstar_loc = kwarg = None
        loc = star_loc.join(vararg_tok.loc)
        vararg = self._arg(vararg_tok)
        if kwarg_opt:
            _all_stmts[(23894,23896)] = True
            _, dstar_loc, kwarg_tok = kwarg_opt
            kwarg = self._arg(kwarg_tok)
            loc = star_loc.join(kwarg_tok.loc)
        return self._arguments(vararg=vararg, kwarg=kwarg,
                               star_loc=star_loc, dstar_loc=dstar_loc, loc=loc)

    @action(Eps(value=(), loc=(24196,24199)), loc=(24189,24195))
    def varargslist__26_4(self):
        _all_stmts[(24215,24218)] = True
        return self._arguments()

    @action(Alt(Seq(Star(SeqN(0, varargslist__26_1, Tok(",", loc=(24330,24333)), loc=(24303,24307)), loc=(24298,24302)),
                    Alt(varargslist__26_2, varargslist__26_3, loc=(24362,24365)), loc=(24294,24297)),
                Seq(List(varargslist__26_1, ",", trailing=True, loc=(24426,24430)),
                    varargslist__26_4, loc=(24422,24425)), loc=(24290,24293)), loc=(24283,24289))
    def varargslist__26(self, fparams, args):
        _all_stmts[(24516,24519)] = True
        """
        (2.6, 2.7)
        varargslist: ((fpdef ['=' test] ',')*
                      ('*' NAME [',' '**' NAME] | '**' NAME) |
                      fpdef ['=' test] (',' fpdef ['=' test])* [','])
        """
        for fparam, default_opt in fparams:
            _all_stmts[(24788,24791)] = True
            if default_opt:
                _all_stmts[(24836,24838)] = True
                equals_loc, default = default_opt
                args.equals_locs.append(equals_loc)
                args.defaults.append(default)
            elif len(args.defaults) > 0:
                _all_stmts[(25012,25016)] = True
                error = diagnostic.Diagnostic(
                    "fatal", "non-default argument follows default argument", {},
                    fparam.loc, [args.args[-1].loc.join(args.defaults[-1].loc)])
                self.diagnostic_engine.process(error)

            args.args.append(fparam)

        def fparam_loc(fparam, default_opt):
            _all_stmts[(25352,25355)] = True
            if default_opt:
                _all_stmts[(25401,25403)] = True
                equals_loc, default = default_opt
                return fparam.loc.join(default.loc)
            else:
                _all_stmts[(25531,25535)] = True
                return fparam.loc

        if args.loc is None:
            _all_stmts[(25580,25582)] = True
            args.loc = fparam_loc(*fparams[0]).join(fparam_loc(*fparams[-1]))
        elif len(fparams) > 0:
            _all_stmts[(25687,25691)] = True
            args.loc = args.loc.join(fparam_loc(*fparams[0]))

        return args

    @action(Tok("ident", loc=(25806,25809)), loc=(25799,25805))
    def fpdef_1(self, ident_tok):
        _all_stmts[(25824,25827)] = True
        return ast.arg(arg=ident_tok.value, annotation=None,
                       arg_loc=ident_tok.loc, colon_loc=None,
                       loc=ident_tok.loc)

    fpdef = Alt(fpdef_1, BeginEnd("(", Rule("fplist", loc=(26059,26063)), ")",
                                  empty=lambda self: ast.Tuple(elts=[], ctx=None, loc=None), loc=(26045,26053)), loc=(26032,26035))
    """fpdef: NAME | '(' fplist ')'"""

    def _argslist(fpdef_rule, old_style=False):
        _all_stmts[(26218,26221)] = True
        argslist_1 = Seq(fpdef_rule, Opt(Seq(Loc("=", loc=(26307,26310)), Rule("test", loc=(26317,26321)), loc=(26303,26306)), loc=(26299,26302)), loc=(26283,26286))

        @action(Seq(Loc("**", loc=(26354,26357)), Tok("ident", loc=(26365,26368)), loc=(26350,26353)), loc=(26343,26349))
        def argslist_2(self, dstar_loc, kwarg_tok):
            _all_stmts[(26388,26391)] = True
            return self._arguments(kwarg=self._arg(kwarg_tok),
                                   dstar_loc=dstar_loc, loc=dstar_loc.join(kwarg_tok.loc))

        @action(Seq(Loc("*", loc=(26607,26610)), Tok("ident", loc=(26617,26620)),
                    Star(SeqN(1, Tok(",", loc=(26664,26667)), argslist_1, loc=(26656,26660)), loc=(26651,26655)),
                    Opt(Seq(Tok(",", loc=(26716,26719)), Loc("**", loc=(26726,26729)), Tok("ident", loc=(26737,26740)), loc=(26712,26715)), loc=(26708,26711)), loc=(26603,26606)), loc=(26596,26602))
        def argslist_3(self, star_loc, vararg_tok, fparams, kwarg_opt):
            _all_stmts[(26762,26765)] = True
            dstar_loc = kwarg = None
            loc = star_loc.join(vararg_tok.loc)
            vararg = self._arg(vararg_tok)
            if kwarg_opt:
                _all_stmts[(26966,26968)] = True
                _, dstar_loc, kwarg_tok = kwarg_opt
                kwarg = self._arg(kwarg_tok)
                loc = star_loc.join(kwarg_tok.loc)
            kwonlyargs, kw_defaults, kw_equals_locs = [], [], []
            for fparam, default_opt in fparams:
                _all_stmts[(27205,27208)] = True
                if default_opt:
                    _all_stmts[(27257,27259)] = True
                    equals_loc, default = default_opt
                    kw_equals_locs.append(equals_loc)
                    kw_defaults.append(default)
                else:
                    _all_stmts[(27445,27449)] = True
                    kw_defaults.append(None)
                kwonlyargs.append(fparam)
            if any(kw_defaults):
                _all_stmts[(27550,27552)] = True
                loc = loc.join(kw_defaults[-1].loc)
            elif any(kwonlyargs):
                _all_stmts[(27635,27639)] = True
                loc = loc.join(kwonlyargs[-1].loc)
            return self._arguments(vararg=vararg, kwarg=kwarg,
                                   kwonlyargs=kwonlyargs, kw_defaults=kw_defaults,
                                   star_loc=star_loc, dstar_loc=dstar_loc,
                                   kw_equals_locs=kw_equals_locs, loc=loc)

        argslist_4 = Alt(argslist_2, argslist_3, loc=(28026,28029))

        @action(Eps(value=(), loc=(28071,28074)), loc=(28064,28070))
        def argslist_5(self):
            _all_stmts[(28094,28097)] = True
            return self._arguments()

        if old_style:
            _all_stmts[(28162,28164)] = True
            argslist = Alt(Seq(Star(SeqN(0, argslist_1, Tok(",", loc=(28232,28235)), loc=(28212,28216)), loc=(28207,28211)),
                               argslist_4, loc=(28203,28206)),
                           Seq(List(argslist_1, ",", trailing=True, loc=(28319,28323)),
                               argslist_5, loc=(28315,28318)), loc=(28199,28202))
        else:
            _all_stmts[(28409,28413)] = True
            argslist = Alt(Seq(Eps(value=[], loc=(28446,28449)), argslist_4, loc=(28442,28445)),
                           Seq(List(argslist_1, ",", trailing=False, loc=(28505,28509)),
                               Alt(SeqN(1, Tok(",", loc=(28587,28590)), Alt(argslist_4, argslist_5, loc=(28597,28600)), loc=(28579,28583)),
                                   argslist_5, loc=(28575,28578)), loc=(28501,28504)), loc=(28438,28441))

        def argslist_action(self, fparams, args):
            _all_stmts[(28685,28688)] = True
            for fparam, default_opt in fparams:
                _all_stmts[(28739,28742)] = True
                if default_opt:
                    _all_stmts[(28791,28793)] = True
                    equals_loc, default = default_opt
                    args.equals_locs.append(equals_loc)
                    args.defaults.append(default)
                elif len(args.defaults) > 0:
                    _all_stmts[(28983,28987)] = True
                    error = diagnostic.Diagnostic(
                        "fatal", "non-default argument follows default argument", {},
                        fparam.loc, [args.args[-1].loc.join(args.defaults[-1].loc)])
                    self.diagnostic_engine.process(error)

                args.args.append(fparam)

            def fparam_loc(fparam, default_opt):
                _all_stmts[(29347,29350)] = True
                if default_opt:
                    _all_stmts[(29400,29402)] = True
                    equals_loc, default = default_opt
                    return fparam.loc.join(default.loc)
                else:
                    _all_stmts[(29542,29546)] = True
                    return fparam.loc

            if args.loc is None:
                _all_stmts[(29599,29601)] = True
                args.loc = fparam_loc(*fparams[0]).join(fparam_loc(*fparams[-1]))
            elif len(fparams) > 0:
                _all_stmts[(29714,29718)] = True
                args.loc = args.loc.join(fparam_loc(*fparams[0]))

            return args

        return action(argslist, loc=(29844,29850))(argslist_action)

    typedargslist__30 = _argslist(Rule("tfpdef", loc=(29913,29917)), old_style=True)
    """
    (3.0, 3.1)
    typedargslist: ((tfpdef ['=' test] ',')*
                    ('*' [tfpdef] (',' tfpdef ['=' test])* [',' '**' tfpdef] | '**' tfpdef)
                    | tfpdef ['=' test] (',' tfpdef ['=' test])* [','])
    """

    typedargslist__32 = _argslist(Rule("tfpdef", loc=(30220,30224)))
    """
    (3.2-)
    typedargslist: (tfpdef ['=' test] (',' tfpdef ['=' test])* [','
           ['*' [tfpdef] (',' tfpdef ['=' test])* [',' '**' tfpdef] | '**' tfpdef]]
         |  '*' [tfpdef] (',' tfpdef ['=' test])* [',' '**' tfpdef] | '**' tfpdef)
    """

    varargslist__30 = _argslist(Rule("vfpdef", loc=(30531,30535)), old_style=True)
    """
    (3.0, 3.1)
    varargslist: ((vfpdef ['=' test] ',')*
                  ('*' [vfpdef] (',' vfpdef ['=' test])*  [',' '**' vfpdef] | '**' vfpdef)
                  | vfpdef ['=' test] (',' vfpdef ['=' test])* [','])
    """

    varargslist__32 = _argslist(Rule("vfpdef", loc=(30831,30835)))
    """
    (3.2-)
    varargslist: (vfpdef ['=' test] (',' vfpdef ['=' test])* [','
           ['*' [vfpdef] (',' vfpdef ['=' test])* [',' '**' vfpdef] | '**' vfpdef]]
         |  '*' [vfpdef] (',' vfpdef ['=' test])* [',' '**' vfpdef] | '**' vfpdef)
    """

    @action(Seq(Tok("ident", loc=(31124,31127)), Opt(Seq(Loc(":", loc=(31146,31149)), Rule("test", loc=(31156,31160)), loc=(31142,31145)), loc=(31138,31141)), loc=(31120,31123)), loc=(31113,31119))
    def tfpdef(self, ident_tok, annotation_opt):
        _all_stmts[(31177,31180)] = True
        """(3.0-) tfpdef: NAME [':' test]"""
        if annotation_opt:
            _all_stmts[(31275,31277)] = True
            colon_loc, annotation = annotation_opt
            return self._arg(ident_tok, colon_loc, annotation)
        return self._arg(ident_tok)

    vfpdef = fpdef_1
    """(3.0-) vfpdef: NAME"""

    @action(List(Rule("fpdef", loc=(31514,31518)), ",", trailing=True, loc=(31509,31513)), loc=(31502,31508))
    def fplist(self, elts):
        _all_stmts[(31554,31557)] = True
        """fplist: fpdef (',' fpdef)* [',']"""
        return ast.Tuple(elts=elts, ctx=None, loc=None)

    stmt = Alt(Rule("simple_stmt", loc=(31697,31701)), Rule("compound_stmt", loc=(31718,31722)), loc=(31693,31696))
    """stmt: simple_stmt | compound_stmt"""

    simple_stmt = SeqN(0, List(Rule("small_stmt", loc=(31817,31821)), ";", trailing=True, loc=(31812,31816)), Tok("newline", loc=(31858,31861)), loc=(31804,31808))
    """simple_stmt: small_stmt (';' small_stmt)* [';'] NEWLINE"""

    small_stmt = Alt(Rule("expr_stmt", loc=(31962,31966)), Rule("print_stmt", loc=(31981,31985)),  Rule("del_stmt", loc=(32002,32006)),
                     Rule("pass_stmt", loc=(32041,32045)), Rule("flow_stmt", loc=(32060,32064)), Rule("import_stmt", loc=(32079,32083)),
                     Rule("global_stmt", loc=(32121,32125)), Rule("nonlocal_stmt", loc=(32142,32146)), Rule("exec_stmt", loc=(32165,32169)),
                     Rule("assert_stmt", loc=(32205,32209)), loc=(31958,31961))
    """
    (2.6, 2.7)
    small_stmt: (expr_stmt | print_stmt  | del_stmt | pass_stmt | flow_stmt |
                 import_stmt | global_stmt | exec_stmt | assert_stmt)
    (3.0-)
    small_stmt: (expr_stmt | del_stmt | pass_stmt | flow_stmt |
                 import_stmt | global_stmt | nonlocal_stmt | assert_stmt)
    """

    expr_stmt_1__26 = Rule("testlist", loc=(32577,32581))
    expr_stmt_1__32 = Rule("testlist_star_expr", loc=(32616,32620))

    @action(Seq(Rule("augassign", loc=(32660,32664)), Alt(Rule("yield_expr", loc=(32683,32687)), Rule("testlist", loc=(32703,32707)), loc=(32679,32682)), loc=(32656,32659)), loc=(32649,32655))
    def expr_stmt_2(self, augassign, rhs_expr):
        _all_stmts[(32727,32730)] = True
        return ast.AugAssign(op=augassign, value=rhs_expr)

    @action(Star(Seq(Loc("=", loc=(32852,32855)), Alt(Rule("yield_expr", loc=(32866,32870)), Rule("expr_stmt_1", loc=(32886,32890)), loc=(32862,32865)), loc=(32848,32851)), loc=(32843,32847)), loc=(32836,32842))
    def expr_stmt_3(self, seq):
        _all_stmts[(32914,32917)] = True
        if len(seq) > 0:
            _all_stmts[(32950,32952)] = True
            return ast.Assign(targets=list(map(lambda x: x[1], seq[:-1])), value=seq[-1][1],
                              op_locs=list(map(lambda x: x[0], seq)))
        else:
            _all_stmts[(33138,33142)] = True
            return None

    @action(Seq(Rule("expr_stmt_1", loc=(33185,33189)), Alt(expr_stmt_2, expr_stmt_3, loc=(33206,33209)), loc=(33181,33184)), loc=(33174,33180))
    def expr_stmt(self, lhs, rhs):
        _all_stmts[(33242,33245)] = True
        """
        (2.6, 2.7, 3.0, 3.1)
        expr_stmt: testlist (augassign (yield_expr|testlist) |
                             ('=' (yield_expr|testlist))*)
        (3.2-)
        expr_stmt: testlist_star_expr (augassign (yield_expr|testlist) |
                             ('=' (yield_expr|testlist_star_expr))*)
        """
        if isinstance(rhs, ast.AugAssign):
            _all_stmts[(33613,33615)] = True
            if isinstance(lhs, ast.Tuple) or isinstance(lhs, ast.List):
                _all_stmts[(33660,33662)] = True
                error = diagnostic.Diagnostic(
                    "fatal", "illegal expression for augmented assignment", {},
                    rhs.op.loc, [lhs.loc])
                self.diagnostic_engine.process(error)
            else:
                _all_stmts[(33956,33960)] = True
                rhs.target = self._assignable(lhs)
                rhs.loc = rhs.target.loc.join(rhs.value.loc)
                return rhs
        elif rhs is not None:
            _all_stmts[(34109,34113)] = True
            rhs.targets = list(map(self._assignable, [lhs] + rhs.targets))
            rhs.loc = lhs.loc.join(rhs.value.loc)
            return rhs
        else:
            _all_stmts[(34287,34291)] = True
            return ast.Expr(value=lhs, loc=lhs.loc)

    testlist_star_expr = action(
        List(Alt(Rule("test", loc=(34396,34400)), Rule("star_expr", loc=(34410,34414)), loc=(34392,34395)), ",", trailing=True, loc=(34387,34391)), loc=(34371,34377)) \
        (_wrap_tuple)
    """(3.2-) testlist_star_expr: (test|star_expr) (',' (test|star_expr))* [',']"""

    augassign = Alt(Oper(ast.Add, "+=", loc=(34580,34584)), Oper(ast.Sub, "-=", loc=(34601,34605)), Oper(ast.MatMult, "@=", loc=(34622,34626)),
                    Oper(ast.Mult, "*=", loc=(34667,34671)), Oper(ast.Div, "/=", loc=(34689,34693)), Oper(ast.Mod, "%=", loc=(34710,34714)),
                    Oper(ast.BitAnd, "&=", loc=(34751,34755)), Oper(ast.BitOr, "|=", loc=(34775,34779)), Oper(ast.BitXor, "^=", loc=(34798,34802)),
                    Oper(ast.LShift, "<<=", loc=(34842,34846)), Oper(ast.RShift, ">>=", loc=(34867,34871)),
                    Oper(ast.Pow, "**=", loc=(34912,34916)), Oper(ast.FloorDiv, "//=", loc=(34934,34938)), loc=(34576,34579))
    """augassign: ('+=' | '-=' | '*=' | '/=' | '%=' | '&=' | '|=' | '^=' |
                   '<<=' | '>>=' | '**=' | '//=')"""

    @action(List(Rule("test", loc=(35107,35111)), ",", trailing=True, loc=(35102,35106)), loc=(35095,35101))
    def print_stmt_1(self, values):
        _all_stmts[(35146,35149)] = True
        nl, loc = True, values[-1].loc
        if values.trailing_comma:
            _all_stmts[(35225,35227)] = True
            nl, loc = False, values.trailing_comma.loc
        return ast.Print(dest=None, values=values, nl=nl,
                         dest_loc=None, loc=loc)

    @action(Seq(Loc(">>", loc=(35430,35433)), Rule("test", loc=(35441,35445)), Tok(",", loc=(35455,35458)), List(Rule("test", loc=(35470,35474)), ",", trailing=True, loc=(35465,35469)), loc=(35426,35429)), loc=(35419,35425))
    def print_stmt_2(self, dest_loc, dest, comma_tok, values):
        _all_stmts[(35510,35513)] = True
        nl, loc = True, values[-1].loc
        if values.trailing_comma:
            _all_stmts[(35616,35618)] = True
            nl, loc = False, values.trailing_comma.loc
        return ast.Print(dest=dest, values=values, nl=nl,
                         dest_loc=dest_loc, loc=loc)

    @action(Seq(Loc("print", loc=(35825,35828)), Alt(print_stmt_1, print_stmt_2, loc=(35839,35842)), loc=(35821,35824)), loc=(35814,35820))
    def print_stmt(self, print_loc, stmt):
        _all_stmts[(35877,35880)] = True
        """
        (2.6-2.7)
        print_stmt: 'print' ( [ test (',' test)* [','] ] |
                              '>>' test [ (',' test)+ [','] ] )
        """
        stmt.keyword_loc = print_loc
        stmt.loc = print_loc.join(stmt.loc)
        return stmt

    @action(Seq(Loc("del", loc=(36199,36202)), List(Rule("expr", loc=(36216,36220)), ",", trailing=True, loc=(36211,36215)), loc=(36195,36198)), loc=(36188,36194))
    def del_stmt(self, stmt_loc, exprs):
        # Python uses exprlist here, but does *not* obey the usual
        # tuple-wrapping semantics, so we embed the rule directly.
        _all_stmts[(36256,36259)] = True
        """del_stmt: 'del' exprlist"""
        return ast.Delete(targets=[self._assignable(expr, is_delete=True) for expr in exprs],
                          loc=stmt_loc.join(exprs[-1].loc), keyword_loc=stmt_loc)

    @action(Loc("pass", loc=(36655,36658)), loc=(36648,36654))
    def pass_stmt(self, stmt_loc):
        _all_stmts[(36672,36675)] = True
        """pass_stmt: 'pass'"""
        return ast.Pass(loc=stmt_loc, keyword_loc=stmt_loc)

    flow_stmt = Alt(Rule("break_stmt", loc=(36816,36820)), Rule("continue_stmt", loc=(36836,36840)), Rule("return_stmt", loc=(36859,36863)),
                    Rule("raise_stmt", loc=(36900,36904)), Rule("yield_stmt", loc=(36920,36924)), loc=(36812,36815))
    """flow_stmt: break_stmt | continue_stmt | return_stmt | raise_stmt | yield_stmt"""

    @action(Loc("break", loc=(37041,37044)), loc=(37034,37040))
    def break_stmt(self, stmt_loc):
        _all_stmts[(37059,37062)] = True
        """break_stmt: 'break'"""
        return ast.Break(loc=stmt_loc, keyword_loc=stmt_loc)

    @action(Loc("continue", loc=(37199,37202)), loc=(37192,37198))
    def continue_stmt(self, stmt_loc):
        _all_stmts[(37220,37223)] = True
        """continue_stmt: 'continue'"""
        return ast.Continue(loc=stmt_loc, keyword_loc=stmt_loc)

    @action(Seq(Loc("return", loc=(37376,37379)), Opt(Rule("testlist", loc=(37395,37399)), loc=(37391,37394)), loc=(37372,37375)), loc=(37365,37371))
    def return_stmt(self, stmt_loc, values):
        _all_stmts[(37419,37422)] = True
        """return_stmt: 'return' [testlist]"""
        loc = stmt_loc
        if values:
            _all_stmts[(37538,37540)] = True
            loc = loc.join(values.loc)
        return ast.Return(value=values,
                          loc=loc, keyword_loc=stmt_loc)

    @action(Rule("yield_expr", loc=(37698,37702)), loc=(37691,37697))
    def yield_stmt(self, expr):
        _all_stmts[(37722,37725)] = True
        """yield_stmt: yield_expr"""
        return ast.Expr(value=expr, loc=expr.loc)

    @action(Seq(Loc("raise", loc=(37854,37857)), Opt(Seq(Rule("test", loc=(37876,37880)),
                                      Opt(Seq(Tok(",", loc=(37936,37939)), Rule("test", loc=(37946,37950)),
                                              Opt(SeqN(1, Tok(",", loc=(38018,38021)), Rule("test", loc=(38028,38032)), loc=(38010,38014)), loc=(38006,38009)), loc=(37932,37935)), loc=(37928,37931)), loc=(37872,37875)), loc=(37868,37871)), loc=(37850,37853)), loc=(37843,37849))
    def raise_stmt__26(self, raise_loc, type_opt):
        _all_stmts[(38053,38056)] = True
        """(2.6, 2.7) raise_stmt: 'raise' [test [',' test [',' test]]]"""
        type_ = inst = tback = None
        loc = raise_loc
        if type_opt:
            _all_stmts[(38242,38244)] = True
            type_, inst_opt = type_opt
            loc = loc.join(type_.loc)
            if inst_opt:
                _all_stmts[(38344,38346)] = True
                _, inst, tback = inst_opt
                loc = loc.join(inst.loc)
                if tback:
                    _all_stmts[(38456,38458)] = True
                    loc = loc.join(tback.loc)
        return ast.Raise(exc=type_, inst=inst, tback=tback, cause=None,
                         keyword_loc=raise_loc, from_loc=None, loc=loc)

    @action(Seq(Loc("raise", loc=(38673,38676)), Opt(Seq(Rule("test", loc=(38695,38699)), Opt(Seq(Loc("from", loc=(38717,38720)), Rule("test", loc=(38730,38734)), loc=(38713,38716)), loc=(38709,38712)), loc=(38691,38694)), loc=(38687,38690)), loc=(38669,38672)), loc=(38662,38668))
    def raise_stmt__30(self, raise_loc, exc_opt):
        _all_stmts[(38753,38756)] = True
        """(3.0-) raise_stmt: 'raise' [test ['from' test]]"""
        exc = from_loc = cause = None
        loc = raise_loc
        if exc_opt:
            _all_stmts[(38931,38933)] = True
            exc, cause_opt = exc_opt
            loc = loc.join(exc.loc)
            if cause_opt:
                _all_stmts[(39028,39030)] = True
                from_loc, cause = cause_opt
                loc = loc.join(cause.loc)
        return ast.Raise(exc=exc, inst=None, tback=None, cause=cause,
                         keyword_loc=raise_loc, from_loc=from_loc, loc=loc)

    import_stmt = Alt(Rule("import_name", loc=(39297,39301)), Rule("import_from", loc=(39318,39322)), loc=(39293,39296))
    """import_stmt: import_name | import_from"""

    @action(Seq(Loc("import", loc=(39405,39408)), Rule("dotted_as_names", loc=(39420,39424)), loc=(39401,39404)), loc=(39394,39400))
    def import_name(self, import_loc, names):
        _all_stmts[(39450,39453)] = True
        """import_name: 'import' dotted_as_names"""
        return ast.Import(names=names,
                          keyword_loc=import_loc, loc=import_loc.join(names[-1].loc))

    @action(Loc(".", loc=(39682,39685)), loc=(39675,39681))
    def import_from_1(self, loc):
        _all_stmts[(39696,39699)] = True
        return 1, loc

    @action(Loc("...", loc=(39761,39764)), loc=(39754,39760))
    def import_from_2(self, loc):
        _all_stmts[(39777,39780)] = True
        return 3, loc

    @action(Seq(Star(Alt(import_from_1, import_from_2, loc=(39851,39854)), loc=(39846,39850)), Rule("dotted_name", loc=(39887,39891)), loc=(39842,39845)), loc=(39835,39841))
    def import_from_3(self, dots, dotted_name):
        _all_stmts[(39913,39916)] = True
        dots_loc, dots_count = None, 0
        if any(dots):
            _all_stmts[(40004,40006)] = True
            dots_loc = dots[0][1].join(dots[-1][1])
            dots_count = sum([count for count, loc in dots])
        return (dots_loc, dots_count), dotted_name

    @action(Plus(Alt(import_from_1, import_from_2, loc=(40200,40203)), loc=(40195,40199)), loc=(40188,40194))
    def import_from_4(self, dots):
        _all_stmts[(40240,40243)] = True
        dots_loc = dots[0][1].join(dots[-1][1])
        dots_count = sum([count for count, loc in dots])
        return (dots_loc, dots_count), None

    @action(Loc("*", loc=(40433,40436)), loc=(40426,40432))
    def import_from_5(self, star_loc):
        _all_stmts[(40447,40450)] = True
        return (None, 0), \
               [ast.alias(name="*", asname=None,
                          name_loc=star_loc, as_loc=None, asname_loc=None, loc=star_loc)], \
               None

    @action(Rule("import_as_names", loc=(40685,40689)), loc=(40678,40684))
    def import_from_6(self, names):
        _all_stmts[(40714,40717)] = True
        return (None, 0), names, None

    @action(Seq(Loc("from", loc=(40801,40804)), Alt(import_from_3, import_from_4, loc=(40814,40817)),
                Loc("import", loc=(40865,40868)), Alt(import_from_5,
                                   Seq(Loc("(", loc=(40938,40941)), Rule("import_as_names", loc=(40948,40952)), Loc(")", loc=(40973,40976)), loc=(40934,40937)),
                                   import_from_6, loc=(40880,40883)), loc=(40797,40800)), loc=(40790,40796))
    def import_from(self, from_loc, module_name, import_loc, names):
        _all_stmts[(41040,41043)] = True
        """
        (2.6, 2.7)
        import_from: ('from' ('.'* dotted_name | '.'+)
                      'import' ('*' | '(' import_as_names ')' | import_as_names))
        (3.0-)
        # note below: the ('.' | '...') is necessary because '...' is tokenized as ELLIPSIS
        import_from: ('from' (('.' | '...')* dotted_name | ('.' | '...')+)
                      'import' ('*' | '(' import_as_names ')' | import_as_names))
        """
        (dots_loc, dots_count), dotted_name_opt = module_name
        module_loc = module = None
        if dotted_name_opt:
            _all_stmts[(41654,41656)] = True
            module_loc, module = dotted_name_opt
        lparen_loc, names, rparen_loc = names
        loc = from_loc.join(names[-1].loc)
        if rparen_loc:
            _all_stmts[(41820,41822)] = True
            loc = loc.join(rparen_loc)

        if module == "__future__":
            _all_stmts[(41883,41885)] = True
            self.add_flags([x.name for x in names])

        return ast.ImportFrom(names=names, module=module, level=dots_count,
                              keyword_loc=from_loc, dots_loc=dots_loc, module_loc=module_loc,
                              import_loc=import_loc, lparen_loc=lparen_loc, rparen_loc=rparen_loc,
                              loc=loc)

    @action(Seq(Tok("ident", loc=(42288,42291)), Opt(Seq(Loc("as", loc=(42310,42313)), Tok("ident", loc=(42321,42324)), loc=(42306,42309)), loc=(42302,42305)), loc=(42284,42287)), loc=(42277,42283))
    def import_as_name(self, name_tok, as_name_opt):
        _all_stmts[(42342,42345)] = True
        """import_as_name: NAME ['as' NAME]"""
        asname_name = asname_loc = as_loc = None
        loc = name_tok.loc
        if as_name_opt:
            _all_stmts[(42522,42524)] = True
            as_loc, asname = as_name_opt
            asname_name = asname.value
            asname_loc = asname.loc
            loc = loc.join(asname.loc)
        return ast.alias(name=name_tok.value, asname=asname_name,
                         loc=loc, name_loc=name_tok.loc, as_loc=as_loc, asname_loc=asname_loc)

    @action(Seq(Rule("dotted_name", loc=(42871,42875)), Opt(Seq(Loc("as", loc=(42900,42903)), Tok("ident", loc=(42911,42914)), loc=(42896,42899)), loc=(42892,42895)), loc=(42867,42870)), loc=(42860,42866))
    def dotted_as_name(self, dotted_name, as_name_opt):
        _all_stmts[(42932,42935)] = True
        """dotted_as_name: dotted_name ['as' NAME]"""
        asname_name = asname_loc = as_loc = None
        dotted_name_loc, dotted_name_name = dotted_name
        loc = dotted_name_loc
        if as_name_opt:
            _all_stmts[(43181,43183)] = True
            as_loc, asname = as_name_opt
            asname_name = asname.value
            asname_loc = asname.loc
            loc = loc.join(asname.loc)
        return ast.alias(name=dotted_name_name, asname=asname_name,
                         loc=loc, name_loc=dotted_name_loc, as_loc=as_loc, asname_loc=asname_loc)

    import_as_names = List(Rule("import_as_name", loc=(43546,43550)), ",", trailing=True, loc=(43541,43545))
    """import_as_names: import_as_name (',' import_as_name)* [',']"""

    dotted_as_names = List(Rule("dotted_as_name", loc=(43688,43692)), ",", trailing=False, loc=(43683,43687))
    """dotted_as_names: dotted_as_name (',' dotted_as_name)*"""

    @action(List(Tok("ident", loc=(43815,43818)), ".", trailing=False, loc=(43810,43814)), loc=(43803,43809))
    def dotted_name(self, idents):
        _all_stmts[(43855,43858)] = True
        """dotted_name: NAME ('.' NAME)*"""
        return idents[0].loc.join(idents[-1].loc), \
               ".".join(list(map(lambda x: x.value, idents)))

    @action(Seq(Loc("global", loc=(44062,44065)), List(Tok("ident", loc=(44082,44085)), ",", trailing=False, loc=(44077,44081)), loc=(44058,44061)), loc=(44051,44057))
    def global_stmt(self, global_loc, names):
        _all_stmts[(44123,44126)] = True
        """global_stmt: 'global' NAME (',' NAME)*"""
        return ast.Global(names=list(map(lambda x: x.value, names)),
                          name_locs=list(map(lambda x: x.loc, names)),
                          keyword_loc=global_loc, loc=global_loc.join(names[-1].loc))

    @action(Seq(Loc("exec", loc=(44461,44464)), Rule("expr", loc=(44474,44478)),
                Opt(Seq(Loc("in", loc=(44512,44515)), Rule("test", loc=(44523,44527)),
                        Opt(SeqN(1, Loc(",", loc=(44573,44576)), Rule("test", loc=(44583,44587)), loc=(44565,44569)), loc=(44561,44564)), loc=(44508,44511)), loc=(44504,44507)), loc=(44457,44460)), loc=(44450,44456))
    def exec_stmt(self, exec_loc, body, in_opt):
        _all_stmts[(44606,44609)] = True
        """(2.6, 2.7) exec_stmt: 'exec' expr ['in' test [',' test]]"""
        in_loc, globals, locals = None, None, None
        loc = exec_loc.join(body.loc)
        if in_opt:
            _all_stmts[(44819,44821)] = True
            in_loc, globals, locals = in_opt
            if locals:
                _all_stmts[(44887,44889)] = True
                loc = loc.join(locals.loc)
            else:
                _all_stmts[(44953,44957)] = True
                loc = loc.join(globals.loc)
        return ast.Exec(body=body, locals=locals, globals=globals,
                        loc=loc, keyword_loc=exec_loc, in_loc=in_loc)

    @action(Seq(Loc("nonlocal", loc=(45157,45160)), List(Tok("ident", loc=(45179,45182)), ",", trailing=False, loc=(45174,45178)), loc=(45153,45156)), loc=(45146,45152))
    def nonlocal_stmt(self, nonlocal_loc, names):
        _all_stmts[(45220,45223)] = True
        """(3.0-) nonlocal_stmt: 'nonlocal' NAME (',' NAME)*"""
        return ast.Nonlocal(names=list(map(lambda x: x.value, names)),
                            name_locs=list(map(lambda x: x.loc, names)),
                            keyword_loc=nonlocal_loc, loc=nonlocal_loc.join(names[-1].loc))

    @action(Seq(Loc("assert", loc=(45583,45586)), Rule("test", loc=(45598,45602)), Opt(SeqN(1, Tok(",", loc=(45624,45627)), Rule("test", loc=(45634,45638)), loc=(45616,45620)), loc=(45612,45615)), loc=(45579,45582)), loc=(45572,45578))
    def assert_stmt(self, assert_loc, test, msg):
        _all_stmts[(45655,45658)] = True
        """assert_stmt: 'assert' test [',' test]"""
        loc = assert_loc.join(test.loc)
        if msg:
            _all_stmts[(45801,45803)] = True
            loc = loc.join(msg.loc)
        return ast.Assert(test=test, msg=msg,
                          loc=loc, keyword_loc=assert_loc)

    @action(Alt(Rule("if_stmt", loc=(45967,45971)), Rule("while_stmt", loc=(45984,45988)), Rule("for_stmt", loc=(46004,46008)),
                Rule("try_stmt", loc=(46038,46042)), Rule("with_stmt", loc=(46056,46060)), Rule("funcdef", loc=(46075,46079)),
                Rule("classdef", loc=(46108,46112)), Rule("decorated", loc=(46126,46130)), loc=(45963,45966)), loc=(45956,45962))
    def compound_stmt(self, stmt):
        _all_stmts[(46150,46153)] = True
        """compound_stmt: if_stmt | while_stmt | for_stmt | try_stmt | with_stmt |
                          funcdef | classdef | decorated"""
        return [stmt]

    @action(Seq(Loc("if", loc=(46363,46366)), Rule("test", loc=(46374,46378)), Loc(":", loc=(46388,46391)), Rule("suite", loc=(46398,46402)),
                Star(Seq(Loc("elif", loc=(46438,46441)), Rule("test", loc=(46451,46455)), Loc(":", loc=(46465,46468)), Rule("suite", loc=(46475,46479)), loc=(46434,46437)), loc=(46429,46433)),
                Opt(Seq(Loc("else", loc=(46516,46519)), Loc(":", loc=(46529,46532)), Rule("suite", loc=(46539,46543)), loc=(46512,46515)), loc=(46508,46511)), loc=(46359,46362)), loc=(46352,46358))
    def if_stmt(self, if_loc, test, if_colon_loc, body, elifs, else_opt):
        _all_stmts[(46561,46564)] = True
        """if_stmt: 'if' test ':' suite ('elif' test ':' suite)* ['else' ':' suite]"""
        stmt = ast.If(orelse=[],
                      else_loc=None, else_colon_loc=None)

        if else_opt:
            _all_stmts[(46818,46820)] = True
            stmt.else_loc, stmt.else_colon_loc, stmt.orelse = else_opt

        for elif_ in elifs:
            _all_stmts[(46911,46914)] = True
            stmt.keyword_loc, stmt.test, stmt.if_colon_loc, stmt.body = elif_
            stmt.loc = stmt.keyword_loc.join(stmt.body[-1].loc)
            if stmt.orelse:
                _all_stmts[(47085,47087)] = True
                stmt.loc = stmt.loc.join(stmt.orelse[-1].loc)
            stmt = ast.If(orelse=[stmt],
                          else_loc=None, else_colon_loc=None)

        stmt.keyword_loc, stmt.test, stmt.if_colon_loc, stmt.body = \
            if_loc, test, if_colon_loc, body
        stmt.loc = stmt.keyword_loc.join(stmt.body[-1].loc)
        if stmt.orelse:
            _all_stmts[(47450,47452)] = True
            stmt.loc = stmt.loc.join(stmt.orelse[-1].loc)
        return stmt

    @action(Seq(Loc("while", loc=(47561,47564)), Rule("test", loc=(47575,47579)), Loc(":", loc=(47589,47592)), Rule("suite", loc=(47599,47603)),
                Opt(Seq(Loc("else", loc=(47638,47641)), Loc(":", loc=(47651,47654)), Rule("suite", loc=(47661,47665)), loc=(47634,47637)), loc=(47630,47633)), loc=(47557,47560)), loc=(47550,47556))
    def while_stmt(self, while_loc, test, while_colon_loc, body, else_opt):
        _all_stmts[(47683,47686)] = True
        """while_stmt: 'while' test ':' suite ['else' ':' suite]"""
        stmt = ast.While(test=test, body=body, orelse=[],
                         keyword_loc=while_loc, while_colon_loc=while_colon_loc,
                         else_loc=None, else_colon_loc=None,
                         loc=while_loc.join(body[-1].loc))
        if else_opt:
            _all_stmts[(48090,48092)] = True
            stmt.else_loc, stmt.else_colon_loc, stmt.orelse = else_opt
            stmt.loc = stmt.loc.join(stmt.orelse[-1].loc)

        return stmt

    @action(Seq(Loc("for", loc=(48270,48273)), Rule("exprlist", loc=(48282,48286)), Loc("in", loc=(48300,48303)), Rule("testlist", loc=(48311,48315)),
                Loc(":", loc=(48345,48348)), Rule("suite", loc=(48355,48359)),
                Opt(Seq(Loc("else", loc=(48394,48397)), Loc(":", loc=(48407,48410)), Rule("suite", loc=(48417,48421)), loc=(48390,48393)), loc=(48386,48389)), loc=(48266,48269)), loc=(48259,48265))
    def for_stmt(self, for_loc, target, in_loc, iter, for_colon_loc, body, else_opt):
        _all_stmts[(48439,48442)] = True
        """for_stmt: 'for' exprlist 'in' testlist ':' suite ['else' ':' suite]"""
        stmt = ast.For(target=self._assignable(target), iter=iter, body=body, orelse=[],
                       keyword_loc=for_loc, in_loc=in_loc, for_colon_loc=for_colon_loc,
                       else_loc=None, else_colon_loc=None,
                       loc=for_loc.join(body[-1].loc))
        if else_opt:
            _all_stmts[(48902,48904)] = True
            stmt.else_loc, stmt.else_colon_loc, stmt.orelse = else_opt
            stmt.loc = stmt.loc.join(stmt.orelse[-1].loc)

        return stmt

    @action(Seq(Plus(Seq(Rule("except_clause", loc=(49091,49095)), Loc(":", loc=(49114,49117)), Rule("suite", loc=(49124,49128)), loc=(49087,49090)), loc=(49082,49086)),
                Opt(Seq(Loc("else", loc=(49165,49168)), Loc(":", loc=(49178,49181)), Rule("suite", loc=(49188,49192)), loc=(49161,49164)), loc=(49157,49160)),
                Opt(Seq(Loc("finally", loc=(49229,49232)), Loc(":", loc=(49245,49248)), Rule("suite", loc=(49255,49259)), loc=(49225,49228)), loc=(49221,49224)), loc=(49078,49081)), loc=(49071,49077))
    def try_stmt_1(self, clauses, else_opt, finally_opt):
        _all_stmts[(49277,49280)] = True
        handlers = []
        for clause in clauses:
            _all_stmts[(49361,49364)] = True
            handler, handler.colon_loc, handler.body = clause
            handler.loc = handler.loc.join(handler.body[-1].loc)
            handlers.append(handler)

        else_loc, else_colon_loc, orelse = None, None, []
        loc = handlers[-1].loc
        if else_opt:
            _all_stmts[(49646,49648)] = True
            else_loc, else_colon_loc, orelse = else_opt
            loc = orelse[-1].loc

        finally_loc, finally_colon_loc, finalbody = None, None, []
        if finally_opt:
            _all_stmts[(49824,49826)] = True
            finally_loc, finally_colon_loc, finalbody = finally_opt
            loc = finalbody[-1].loc
        stmt = ast.Try(body=None, handlers=handlers, orelse=orelse, finalbody=finalbody,
                       else_loc=else_loc, else_colon_loc=else_colon_loc,
                       finally_loc=finally_loc, finally_colon_loc=finally_colon_loc,
                       loc=loc)
        return stmt

    @action(Seq(Loc("finally", loc=(50260,50263)), Loc(":", loc=(50276,50279)), Rule("suite", loc=(50286,50290)), loc=(50256,50259)), loc=(50249,50255))
    def try_stmt_2(self, finally_loc, finally_colon_loc, finalbody):
        _all_stmts[(50306,50309)] = True
        return ast.Try(body=None, handlers=[], orelse=[], finalbody=finalbody,
                       else_loc=None, else_colon_loc=None,
                       finally_loc=finally_loc, finally_colon_loc=finally_colon_loc,
                       loc=finalbody[-1].loc)

    @action(Seq(Loc("try", loc=(50657,50660)), Loc(":", loc=(50669,50672)), Rule("suite", loc=(50679,50683)), Alt(try_stmt_1, try_stmt_2, loc=(50694,50697)), loc=(50653,50656)), loc=(50646,50652))
    def try_stmt(self, try_loc, try_colon_loc, body, stmt):
        _all_stmts[(50728,50731)] = True
        """
        try_stmt: ('try' ':' suite
                   ((except_clause ':' suite)+
                    ['else' ':' suite]
                    ['finally' ':' suite] |
                    'finally' ':' suite))
        """
        stmt.keyword_loc, stmt.try_colon_loc, stmt.body = \
            try_loc, try_colon_loc, body
        stmt.loc = stmt.loc.join(try_loc)
        return stmt

    @action(Seq(Loc("with", loc=(51195,51198)), Rule("test", loc=(51208,51212)), Opt(Rule("with_var", loc=(51226,51230)), loc=(51222,51225)), Loc(":", loc=(51245,51248)), Rule("suite", loc=(51255,51259)), loc=(51191,51194)), loc=(51184,51190))
    def with_stmt__26(self, with_loc, context, with_var, colon_loc, body):
        _all_stmts[(51275,51278)] = True
        """(2.6, 3.0) with_stmt: 'with' test [ with_var ] ':' suite"""
        if with_var:
            _all_stmts[(51425,51427)] = True
            as_loc, optional_vars = with_var
            item = ast.withitem(context_expr=context, optional_vars=optional_vars,
                                as_loc=as_loc, loc=context.loc.join(optional_vars.loc))
        else:
            _all_stmts[(51662,51666)] = True
            item = ast.withitem(context_expr=context, optional_vars=None,
                                as_loc=None, loc=context.loc)
        return ast.With(items=[item], body=body,
                        keyword_loc=with_loc, colon_loc=colon_loc,
                        loc=with_loc.join(body[-1].loc))

    with_var = Seq(Loc("as", loc=(51997,52000)), Rule("expr", loc=(52008,52012)), loc=(51993,51996))
    """(2.6, 3.0) with_var: 'as' expr"""

    @action(Seq(Loc("with", loc=(52080,52083)), List(Rule("with_item", loc=(52098,52102)), ",", trailing=False, loc=(52093,52097)), Loc(":", loc=(52139,52142)),
                Rule("suite", loc=(52165,52169)), loc=(52076,52079)), loc=(52069,52075))
    def with_stmt__27(self, with_loc, items, colon_loc, body):
        _all_stmts[(52185,52188)] = True
        """(2.7, 3.1-) with_stmt: 'with' with_item (',' with_item)*  ':' suite"""
        return ast.With(items=items, body=body,
                        keyword_loc=with_loc, colon_loc=colon_loc,
                        loc=with_loc.join(body[-1].loc))

    @action(Seq(Rule("test", loc=(52515,52519)), Opt(Seq(Loc("as", loc=(52537,52540)), Rule("expr", loc=(52548,52552)), loc=(52533,52536)), loc=(52529,52532)), loc=(52511,52514)), loc=(52504,52510))
    def with_item(self, context, as_opt):
        _all_stmts[(52569,52572)] = True
        """(2.7, 3.1-) with_item: test ['as' expr]"""
        if as_opt:
            _all_stmts[(52669,52671)] = True
            as_loc, optional_vars = as_opt
            return ast.withitem(context_expr=context, optional_vars=optional_vars,
                                as_loc=as_loc, loc=context.loc.join(optional_vars.loc))
        else:
            _all_stmts[(52902,52906)] = True
            return ast.withitem(context_expr=context, optional_vars=None,
                                as_loc=None, loc=context.loc)

    @action(Seq(Alt(Loc("as", loc=(53065,53068)), Loc(",", loc=(53076,53079)), loc=(53061,53064)), Rule("test", loc=(53087,53091)), loc=(53057,53060)), loc=(53050,53056))
    def except_clause_1__26(self, as_loc, name):
        _all_stmts[(53106,53109)] = True
        return as_loc, None, name

    @action(Seq(Loc("as", loc=(53202,53205)), Tok("ident", loc=(53213,53216)), loc=(53198,53201)), loc=(53191,53197))
    def except_clause_1__30(self, as_loc, name):
        _all_stmts[(53232,53235)] = True
        return as_loc, name, None

    @action(Seq(Loc("except", loc=(53328,53331)),
                Opt(Seq(Rule("test", loc=(53367,53371)),
                        Opt(Rule("except_clause_1", loc=(53409,53413)), loc=(53405,53408)), loc=(53363,53366)), loc=(53359,53362)), loc=(53324,53327)), loc=(53317,53323))
    def except_clause(self, except_loc, exc_opt):
        _all_stmts[(53442,53445)] = True
        """
        (2.6, 2.7) except_clause: 'except' [test [('as' | ',') test]]
        (3.0-) except_clause: 'except' [test ['as' NAME]]
        """
        type_ = name = as_loc = name_loc = None
        loc = except_loc
        if exc_opt:
            _all_stmts[(53721,53723)] = True
            type_, name_opt = exc_opt
            loc = loc.join(type_.loc)
            if name_opt:
                _all_stmts[(53821,53823)] = True
                as_loc, name_tok, name_node = name_opt
                if name_tok:
                    _all_stmts[(53905,53907)] = True
                    name = name_tok.value
                    name_loc = name_tok.loc
                else:
                    _all_stmts[(54020,54024)] = True
                    name = name_node
                    name_loc = name_node.loc
                loc = loc.join(name_loc)
        return ast.ExceptHandler(type=type_, name=name,
                                 except_loc=except_loc, as_loc=as_loc, name_loc=name_loc,
                                 loc=loc)

    @action(Plus(Rule("stmt", loc=(54355,54359)), loc=(54350,54354)), loc=(54343,54349))
    def suite_1(self, stmts):
        _all_stmts[(54374,54377)] = True
        return reduce(list.__add__, stmts, [])

    suite = Alt(Rule("simple_stmt", loc=(54464,54468)),
                SeqN(2, Tok("newline", loc=(54509,54512)), Tok("indent", loc=(54525,54528)), suite_1, Tok("dedent", loc=(54549,54552)), loc=(54501,54505)), loc=(54460,54463))
    """suite: simple_stmt | NEWLINE INDENT stmt+ DEDENT"""

    # 2.x-only backwards compatibility start
    testlist_safe = action(List(Rule("old_test", loc=(54702,54706)), ",", trailing=False, loc=(54697,54701)), loc=(54690,54696))(_wrap_tuple)
    """(2.6, 2.7) testlist_safe: old_test [(',' old_test)+ [',']]"""

    old_test = Alt(Rule("or_test", loc=(54844,54848)), Rule("old_lambdef", loc=(54861,54865)), loc=(54840,54843))
    """(2.6, 2.7) old_test: or_test | old_lambdef"""

    @action(Seq(Loc("lambda", loc=(54952,54955)), Opt(Rule("varargslist", loc=(54971,54975)), loc=(54967,54970)), Loc(":", loc=(54993,54996)), Rule("old_test", loc=(55003,55007)), loc=(54948,54951)), loc=(54941,54947))
    def old_lambdef(self, lambda_loc, args_opt, colon_loc, body):
        _all_stmts[(55026,55029)] = True
        """(2.6, 2.7) old_lambdef: 'lambda' [varargslist] ':' old_test"""
        if args_opt is None:
            _all_stmts[(55170,55172)] = True
            args_opt = self._arguments()
            args_opt.loc = colon_loc.begin()
        return ast.Lambda(args=args_opt, body=body,
                          lambda_loc=lambda_loc, colon_loc=colon_loc,
                          loc=lambda_loc.join(body.loc))
    # 2.x-only backwards compatibility end

    @action(Seq(Rule("or_test", loc=(55516,55520)), Opt(Seq(Loc("if", loc=(55541,55544)), Rule("or_test", loc=(55552,55556)),
                                         Loc("else", loc=(55610,55613)), Rule("test", loc=(55623,55627)), loc=(55537,55540)), loc=(55533,55536)), loc=(55512,55515)), loc=(55505,55511))
    def test_1(self, lhs, rhs_opt):
        _all_stmts[(55644,55647)] = True
        if rhs_opt is not None:
            _all_stmts[(55684,55686)] = True
            if_loc, test, else_loc, orelse = rhs_opt
            return ast.IfExp(test=test, body=lhs, orelse=orelse,
                             if_loc=if_loc, else_loc=else_loc, loc=lhs.loc.join(orelse.loc))
        return lhs

    test = Alt(test_1, Rule("lambdef", loc=(55962,55966)), loc=(55950,55953))
    """test: or_test ['if' or_test 'else' test] | lambdef"""

    test_nocond = Alt(Rule("or_test", loc=(56063,56067)), Rule("lambdef_nocond", loc=(56080,56084)), loc=(56059,56062))
    """(3.0-) test_nocond: or_test | lambdef_nocond"""

    def lambdef_action(self, lambda_loc, args_opt, colon_loc, body):
        _all_stmts[(56164,56167)] = True
        if args_opt is None:
            _all_stmts[(56237,56239)] = True
            args_opt = self._arguments()
            args_opt.loc = colon_loc.begin()
        return ast.Lambda(args=args_opt, body=body,
                          lambda_loc=lambda_loc, colon_loc=colon_loc,
                          loc=lambda_loc.join(body.loc))

    lambdef = action(
        Seq(Loc("lambda", loc=(56558,56561)), Opt(Rule("varargslist", loc=(56577,56581)), loc=(56573,56576)), Loc(":", loc=(56599,56602)), Rule("test", loc=(56609,56613)), loc=(56554,56557)), loc=(56538,56544)) \
        (lambdef_action)
    """lambdef: 'lambda' [varargslist] ':' test"""

    lambdef_nocond = action(
        Seq(Loc("lambda", loc=(56744,56747)), Opt(Rule("varargslist", loc=(56763,56767)), loc=(56759,56762)), Loc(":", loc=(56785,56788)), Rule("test_nocond", loc=(56795,56799)), loc=(56740,56743)), loc=(56724,56730)) \
        (lambdef_action)
    """(3.0-) lambdef_nocond: 'lambda' [varargslist] ':' test_nocond"""

    @action(Seq(Rule("and_test", loc=(56933,56937)), Star(Seq(Loc("or", loc=(56960,56963)), Rule("and_test", loc=(56971,56975)), loc=(56956,56959)), loc=(56951,56955)), loc=(56929,56932)), loc=(56922,56928))
    def or_test(self, lhs, rhs):
        _all_stmts[(56996,56999)] = True
        """or_test: and_test ('or' and_test)*"""
        if len(rhs) > 0:
            _all_stmts[(57082,57084)] = True
            return ast.BoolOp(op=ast.Or(),
                              values=[lhs] + list(map(lambda x: x[1], rhs)),
                              loc=lhs.loc.join(rhs[-1][1].loc),
                              op_locs=list(map(lambda x: x[0], rhs)))
        else:
            _all_stmts[(57361,57365)] = True
            return lhs

    @action(Seq(Rule("not_test", loc=(57407,57411)), Star(Seq(Loc("and", loc=(57434,57437)), Rule("not_test", loc=(57446,57450)), loc=(57430,57433)), loc=(57425,57429)), loc=(57403,57406)), loc=(57396,57402))
    def and_test(self, lhs, rhs):
        _all_stmts[(57471,57474)] = True
        """and_test: not_test ('and' not_test)*"""
        if len(rhs) > 0:
            _all_stmts[(57560,57562)] = True
            return ast.BoolOp(op=ast.And(),
                              values=[lhs] + list(map(lambda x: x[1], rhs)),
                              loc=lhs.loc.join(rhs[-1][1].loc),
                              op_locs=list(map(lambda x: x[0], rhs)))
        else:
            _all_stmts[(57840,57844)] = True
            return lhs

    @action(Seq(Oper(ast.Not, "not", loc=(57886,57890)), Rule("not_test", loc=(57908,57912)), loc=(57882,57885)), loc=(57875,57881))
    def not_test_1(self, op, operand):
        _all_stmts[(57931,57934)] = True
        return ast.UnaryOp(op=op, operand=operand,
                           loc=op.loc.join(operand.loc))

    not_test = Alt(not_test_1, Rule("comparison", loc=(58106,58110)), loc=(58090,58093))
    """not_test: 'not' not_test | comparison"""

    comparison_1__26 = Seq(Rule("expr", loc=(58202,58206)), Star(Seq(Rule("comp_op", loc=(58225,58229)), Rule("expr", loc=(58242,58246)), loc=(58221,58224)), loc=(58216,58220)), loc=(58198,58201))
    comparison_1__30 = Seq(Rule("star_expr", loc=(58285,58289)), Star(Seq(Rule("comp_op", loc=(58313,58317)), Rule("star_expr", loc=(58330,58334)), loc=(58309,58312)), loc=(58304,58308)), loc=(58281,58284))
    comparison_1__32 = comparison_1__26

    @action(Rule("comparison_1", loc=(58404,58408)), loc=(58397,58403))
    def comparison(self, lhs, rhs):
        _all_stmts[(58430,58433)] = True
        """
        (2.6, 2.7) comparison: expr (comp_op expr)*
        (3.0, 3.1) comparison: star_expr (comp_op star_expr)*
        (3.2-) comparison: expr (comp_op expr)*
        """
        if len(rhs) > 0:
            _all_stmts[(58656,58658)] = True
            return ast.Compare(left=lhs, ops=list(map(lambda x: x[0], rhs)),
                               comparators=list(map(lambda x: x[1], rhs)),
                               loc=lhs.loc.join(rhs[-1][1].loc))
        else:
            _all_stmts[(58898,58902)] = True
            return lhs

    @action(Seq(Opt(Loc("*", loc=(58948,58951)), loc=(58944,58947)), Rule("expr", loc=(58959,58963)), loc=(58940,58943)), loc=(58933,58939))
    def star_expr__30(self, star_opt, expr):
        _all_stmts[(58978,58981)] = True
        """(3.0, 3.1) star_expr: ['*'] expr"""
        if star_opt:
            _all_stmts[(59074,59076)] = True
            return ast.Starred(value=expr, ctx=None,
                               star_loc=star_opt, loc=expr.loc.join(star_opt))
        return expr

    @action(Seq(Loc("*", loc=(59256,59259)), Rule("expr", loc=(59266,59270)), loc=(59252,59255)), loc=(59245,59251))
    def star_expr__32(self, star_loc, expr):
        _all_stmts[(59285,59288)] = True
        """(3.0-) star_expr: '*' expr"""
        return ast.Starred(value=expr, ctx=None,
                           star_loc=star_loc, loc=expr.loc.join(star_loc))

    comp_op = Alt(Oper(ast.Lt, "<", loc=(59510,59514)), Oper(ast.Gt, ">", loc=(59529,59533)), Oper(ast.Eq, "==", loc=(59548,59552)),
                  Oper(ast.GtE, ">=", loc=(59586,59590)), Oper(ast.LtE, "<=", loc=(59607,59611)), Oper(ast.NotEq, "<>", loc=(59628,59632)),
                  Oper(ast.NotEq, "!=", loc=(59669,59673)),
                  Oper(ast.In, "in", loc=(59710,59714)), Oper(ast.NotIn, "not", "in", loc=(59730,59734)),
                  Oper(ast.IsNot, "is", "not", loc=(59778,59782)), Oper(ast.Is, "is", loc=(59808,59812)), loc=(59506,59509))
    """
    (2.6, 2.7) comp_op: '<'|'>'|'=='|'>='|'<='|'<>'|'!='|'in'|'not' 'in'|'is'|'is' 'not'
    (3.0-) comp_op: '<'|'>'|'=='|'>='|'<='|'!='|'in'|'not' 'in'|'is'|'is' 'not'
    """

    expr = BinOper("xor_expr", Oper(ast.BitOr, "|", loc=(60045,60049)), loc=(60025,60032))
    """expr: xor_expr ('|' xor_expr)*"""

    xor_expr = BinOper("and_expr", Oper(ast.BitXor, "^", loc=(60144,60148)), loc=(60124,60131))
    """xor_expr: and_expr ('^' and_expr)*"""

    and_expr = BinOper("shift_expr", Oper(ast.BitAnd, "&", loc=(60250,60254)), loc=(60228,60235))
    """and_expr: shift_expr ('&' shift_expr)*"""

    shift_expr = BinOper("arith_expr", Alt(Oper(ast.LShift, "<<", loc=(60366,60370)), Oper(ast.RShift, ">>", loc=(60390,60394)), loc=(60362,60365)), loc=(60340,60347))
    """shift_expr: arith_expr (('<<'|'>>') arith_expr)*"""

    arith_expr = BinOper("term", Alt(Oper(ast.Add, "+", loc=(60512,60516)), Oper(ast.Sub, "-", loc=(60532,60536)), loc=(60508,60511)), loc=(60492,60499))
    """arith_expr: term (('+'|'-') term)*"""

    term = BinOper("factor", Alt(Oper(ast.Mult, "*", loc=(60632,60636)), Oper(ast.MatMult, "@", loc=(60653,60657)),
                                 Oper(ast.Div, "/", loc=(60710,60714)), Oper(ast.Mod, "%", loc=(60730,60734)),
                                 Oper(ast.FloorDiv, "//", loc=(60783,60787)), loc=(60628,60631)), loc=(60610,60617))
    """term: factor (('*'|'/'|'%'|'//') factor)*"""

    @action(Seq(Alt(Oper(ast.UAdd, "+", loc=(60883,60887)), Oper(ast.USub, "-", loc=(60904,60908)), Oper(ast.Invert, "~", loc=(60925,60929)), loc=(60879,60882)),
                Rule("factor", loc=(60965,60969)), loc=(60875,60878)), loc=(60868,60874))
    def factor_1(self, op, factor):
        _all_stmts[(60986,60989)] = True
        return ast.UnaryOp(op=op, operand=factor,
                           loc=op.loc.join(factor.loc))

    factor = Alt(factor_1, Rule("power", loc=(61152,61156)), loc=(61138,61141))
    """factor: ('+'|'-'|'~') factor | power"""

    @action(Seq(Rule("atom", loc=(61231,61235)), Star(Rule("trailer", loc=(61250,61254)), loc=(61245,61249)), Opt(Seq(Loc("**", loc=(61276,61279)), Rule("factor", loc=(61287,61291)), loc=(61272,61275)), loc=(61268,61271)), loc=(61227,61230)), loc=(61220,61226))
    def power(self, atom, trailers, factor_opt):
        _all_stmts[(61310,61313)] = True
        """power: atom trailer* ['**' factor]"""
        for trailer in trailers:
            _all_stmts[(61412,61415)] = True
            if isinstance(trailer, ast.Attribute) or isinstance(trailer, ast.Subscript):
                _all_stmts[(61449,61451)] = True
                trailer.value = atom
            elif isinstance(trailer, ast.Call):
                _all_stmts[(61575,61579)] = True
                trailer.func = atom
            trailer.loc = atom.loc.join(trailer.loc)
            atom = trailer
        if factor_opt:
            _all_stmts[(61735,61737)] = True
            op_loc, factor = factor_opt
            return ast.BinOp(left=atom, op=ast.Pow(loc=op_loc), right=factor,
                             loc=atom.loc.join(factor.loc))
        return atom

    @action(Rule("testlist1", loc=(61961,61965)), loc=(61954,61960))
    def atom_1(self, expr):
        _all_stmts[(61984,61987)] = True
        return ast.Repr(value=expr, loc=None)

    @action(Tok("ident", loc=(62067,62070)), loc=(62060,62066))
    def atom_2(self, tok):
        _all_stmts[(62085,62088)] = True
        return ast.Name(id=tok.value, loc=tok.loc, ctx=None)

    @action(Alt(Tok("int", loc=(62186,62189)), Tok("float", loc=(62198,62201)), Tok("complex", loc=(62212,62215)), loc=(62182,62185)), loc=(62175,62181))
    def atom_3(self, tok):
        _all_stmts[(62233,62236)] = True
        return ast.Num(n=tok.value, loc=tok.loc)

    @action(Seq(Tok("strbegin", loc=(62322,62325)), Tok("strdata", loc=(62339,62342)), Tok("strend", loc=(62355,62358)), loc=(62318,62321)), loc=(62311,62317))
    def atom_4(self, begin_tok, data_tok, end_tok):
        _all_stmts[(62375,62378)] = True
        return ast.Str(s=data_tok.value,
                       begin_loc=begin_tok.loc, end_loc=end_tok.loc,
                       loc=begin_tok.loc.join(end_tok.loc))

    @action(Plus(atom_4, loc=(62606,62610)), loc=(62599,62605))
    def atom_5(self, strings):
        _all_stmts[(62624,62627)] = True
        return ast.Str(s="".join([x.s for x in strings]),
                       begin_loc=strings[0].begin_loc, end_loc=strings[-1].end_loc,
                       loc=strings[0].loc.join(strings[-1].loc))

    atom_6__26 = Rule("dictmaker", loc=(62876,62880))
    atom_6__27 = Rule("dictorsetmaker", loc=(62911,62915))

    atom__26 = Alt(BeginEnd("(", Opt(Alt(Rule("yield_expr", loc=(62976,62980)), Rule("testlist_comp", loc=(62996,63000)), loc=(62972,62975)), loc=(62968,62971)), ")",
                            empty=lambda self: ast.Tuple(elts=[], ctx=None, loc=None), loc=(62954,62962)),
                   BeginEnd("[", Opt(Rule("listmaker", loc=(63151,63155)), loc=(63147,63150)), "]",
                            empty=lambda self: ast.List(elts=[], ctx=None, loc=None), loc=(63133,63141)),
                   BeginEnd("{", Opt(Rule("atom_6", loc=(63300,63304)), loc=(63296,63299)), "}",
                            empty=lambda self: ast.Dict(keys=[], values=[], colon_locs=[],
                                                        loc=None), loc=(63282,63290)),
                   BeginEnd("`", atom_1, "`", loc=(63500,63508)),
                   atom_2, atom_3, atom_5, loc=(62950,62953))
    """
    (2.6)
    atom: ('(' [yield_expr|testlist_gexp] ')' |
           '[' [listmaker] ']' |
           '{' [dictmaker] '}' |
           '`' testlist1 '`' |
           NAME | NUMBER | STRING+)
    (2.7)
    atom: ('(' [yield_expr|testlist_comp] ')' |
           '[' [listmaker] ']' |
           '{' [dictorsetmaker] '}' |
           '`' testlist1 '`' |
           NAME | NUMBER | STRING+)
    """

    @action(Loc("...", loc=(63987,63990)), loc=(63980,63986))
    def atom_7(self, loc):
        _all_stmts[(64003,64006)] = True
        return ast.Ellipsis(loc=loc)

    @action(Alt(Tok("None", loc=(64080,64083)), Tok("True", loc=(64093,64096)), Tok("False", loc=(64106,64109)), loc=(64076,64079)), loc=(64069,64075))
    def atom_8(self, tok):
        _all_stmts[(64125,64128)] = True
        if tok.kind == "None":
            _all_stmts[(64156,64158)] = True
            value = None
        elif tok.kind == "True":
            _all_stmts[(64212,64216)] = True
            value = True
        elif tok.kind == "False":
            _all_stmts[(64270,64274)] = True
            value = False
        return ast.NameConstant(value=value, loc=tok.loc)

    atom__30 = Alt(BeginEnd("(", Opt(Alt(Rule("yield_expr", loc=(64422,64426)), Rule("testlist_comp", loc=(64442,64446)), loc=(64418,64421)), loc=(64414,64417)), ")",
                            empty=lambda self: ast.Tuple(elts=[], ctx=None, loc=None), loc=(64400,64408)),
                   BeginEnd("[", Opt(Rule("testlist_comp__list", loc=(64597,64601)), loc=(64593,64596)), "]",
                            empty=lambda self: ast.List(elts=[], ctx=None, loc=None), loc=(64579,64587)),
                   BeginEnd("{", Opt(Rule("dictorsetmaker", loc=(64756,64760)), loc=(64752,64755)), "}",
                            empty=lambda self: ast.Dict(keys=[], values=[], colon_locs=[],
                                                        loc=None), loc=(64738,64746)),
                   atom_2, atom_3, atom_5, atom_7, atom_8, loc=(64396,64399))
    """
    (3.0-)
    atom: ('(' [yield_expr|testlist_comp] ')' |
           '[' [testlist_comp] ']' |
           '{' [dictorsetmaker] '}' |
           NAME | NUMBER | STRING+ | '...' | 'None' | 'True' | 'False')
    """

    def list_gen_action(self, lhs, rhs):
        _all_stmts[(65231,65234)] = True
        if rhs is None: # (x)
            _all_stmts[(65276,65278)] = True
            return lhs
        elif isinstance(rhs, ast.Tuple) or isinstance(rhs, ast.List):
            _all_stmts[(65329,65333)] = True
            rhs.elts = [lhs] + rhs.elts
            return rhs
        elif isinstance(rhs, ast.ListComp) or isinstance(rhs, ast.GeneratorExp):
            _all_stmts[(65462,65466)] = True
            rhs.elt = lhs
            return rhs

    @action(Rule("list_for", loc=(65597,65601)), loc=(65590,65596))
    def listmaker_1(self, compose):
        _all_stmts[(65619,65622)] = True
        return ast.ListComp(generators=compose([]), loc=None)

    @action(List(Rule("test", loc=(65731,65735)), ",", trailing=True, leading=False, loc=(65726,65730)), loc=(65719,65725))
    def listmaker_2(self, elts):
        _all_stmts[(65785,65788)] = True
        return ast.List(elts=elts, ctx=None, loc=None)

    listmaker = action(
        Seq(Rule("test", loc=(65906,65910)),
            Alt(listmaker_1, listmaker_2, loc=(65932,65935)), loc=(65902,65905)), loc=(65886,65892)) \
        (list_gen_action)
    """listmaker: test ( list_for | (',' test)* [','] )"""

    testlist_comp_1__26 = Rule("test", loc=(66078,66082))
    testlist_comp_1__32 = Alt(Rule("test", loc=(66121,66125)), Rule("star_expr", loc=(66135,66139)), loc=(66117,66120))

    @action(Rule("comp_for", loc=(66167,66171)), loc=(66160,66166))
    def testlist_comp_2(self, compose):
        _all_stmts[(66189,66192)] = True
        return ast.GeneratorExp(generators=compose([]), loc=None)

    @action(List(Rule("testlist_comp_1", loc=(66309,66313)), ",", trailing=True, leading=False, loc=(66304,66308)), loc=(66297,66303))
    def testlist_comp_3(self, elts):
        _all_stmts[(66374,66377)] = True
        if elts == [] and not elts.trailing_comma:
            _all_stmts[(66415,66417)] = True
            return None
        else:
            _all_stmts[(66490,66494)] = True
            return ast.Tuple(elts=elts, ctx=None, loc=None)

    testlist_comp = action(
        Seq(Rule("testlist_comp_1", loc=(66597,66601)), Alt(testlist_comp_2, testlist_comp_3, loc=(66622,66625)), loc=(66593,66596)), loc=(66577,66583)) \
        (list_gen_action)
    """
    (2.6) testlist_gexp: test ( gen_for | (',' test)* [','] )
    (2.7, 3.0, 3.1) testlist_comp: test ( comp_for | (',' test)* [','] )
    (3.2-) testlist_comp: (test|star_expr) ( comp_for | (',' (test|star_expr))* [','] )
    """

    @action(Rule("comp_for", loc=(66942,66946)), loc=(66935,66941))
    def testlist_comp__list_1(self, compose):
        _all_stmts[(66964,66967)] = True
        return ast.ListComp(generators=compose([]), loc=None)

    @action(List(Rule("testlist_comp_1", loc=(67086,67090)), ",", trailing=True, leading=False, loc=(67081,67085)), loc=(67074,67080))
    def testlist_comp__list_2(self, elts):
        _all_stmts[(67151,67154)] = True
        return ast.List(elts=elts, ctx=None, loc=None)

    testlist_comp__list = action(
        Seq(Rule("testlist_comp_1", loc=(67292,67296)), Alt(testlist_comp__list_1, testlist_comp__list_2, loc=(67317,67320)), loc=(67288,67291)), loc=(67272,67278)) \
        (list_gen_action)
    """Same grammar as testlist_comp, but different semantic action."""

    @action(Seq(Loc(".", loc=(67486,67489)), Tok("ident", loc=(67496,67499)), loc=(67482,67485)), loc=(67475,67481))
    def trailer_1(self, dot_loc, ident_tok):
        _all_stmts[(67515,67518)] = True
        return ast.Attribute(attr=ident_tok.value, ctx=None,
                             loc=dot_loc.join(ident_tok.loc),
                             attr_loc=ident_tok.loc, dot_loc=dot_loc)

    trailer = Alt(BeginEnd("(", Opt(Rule("arglist", loc=(67786,67790)), loc=(67782,67785)), ")",
                           empty=_empty_arglist, loc=(67768,67776)),
                  BeginEnd("[", Rule("subscriptlist", loc=(67891,67895)), "]", loc=(67877,67885)),
                  trailer_1, loc=(67764,67767))
    """trailer: '(' [arglist] ')' | '[' subscriptlist ']' | '.' NAME"""

    @action(List(Rule("subscript", loc=(68039,68043)), ",", trailing=True, loc=(68034,68038)), loc=(68027,68033))
    def subscriptlist(self, subscripts):
        _all_stmts[(68083,68086)] = True
        """subscriptlist: subscript (',' subscript)* [',']"""
        if len(subscripts) == 1:
            _all_stmts[(68190,68192)] = True
            return ast.Subscript(slice=subscripts[0], ctx=None, loc=None)
        elif all([isinstance(x, ast.Index) for x in subscripts]):
            _all_stmts[(68297,68301)] = True
            elts  = [x.value for x in subscripts]
            loc   = subscripts[0].loc.join(subscripts[-1].loc)
            index = ast.Index(value=ast.Tuple(elts=elts, ctx=None,
                                              begin_loc=None, end_loc=None, loc=loc),
                              loc=loc)
            return ast.Subscript(slice=index, ctx=None, loc=None)
        else:
            _all_stmts[(68734,68738)] = True
            extslice = ast.ExtSlice(dims=subscripts,
                                    loc=subscripts[0].loc.join(subscripts[-1].loc))
            return ast.Subscript(slice=extslice, ctx=None, loc=None)

    @action(Seq(Loc(".", loc=(68963,68966)), Loc(".", loc=(68973,68976)), Loc(".", loc=(68983,68986)), loc=(68959,68962)), loc=(68952,68958))
    def subscript_1(self, dot_1_loc, dot_2_loc, dot_3_loc):
        _all_stmts[(68998,69001)] = True
        return ast.Ellipsis(loc=dot_1_loc.join(dot_3_loc))

    @action(Seq(Opt(Rule("test", loc=(69134,69138)), loc=(69130,69133)), Loc(":", loc=(69149,69152)), Opt(Rule("test", loc=(69163,69167)), loc=(69159,69162)), Opt(Rule("sliceop", loc=(69182,69186)), loc=(69178,69181)), loc=(69126,69129)), loc=(69119,69125))
    def subscript_2(self, lower_opt, colon_loc, upper_opt, step_opt):
        _all_stmts[(69205,69208)] = True
        loc = colon_loc
        if lower_opt:
            _all_stmts[(69303,69305)] = True
            loc = loc.join(lower_opt.loc)
        if upper_opt:
            _all_stmts[(69367,69369)] = True
            loc = loc.join(upper_opt.loc)
        step_colon_loc = step = None
        if step_opt:
            _all_stmts[(69468,69470)] = True
            step_colon_loc, step = step_opt
            loc = loc.join(step_colon_loc)
            if step:
                _all_stmts[(69580,69582)] = True
                loc = loc.join(step.loc)
        return ast.Slice(lower=lower_opt, upper=upper_opt, step=step,
                         loc=loc, bound_colon_loc=colon_loc, step_colon_loc=step_colon_loc)

    @action(Rule("test", loc=(69805,69809)), loc=(69798,69804))
    def subscript_3(self, expr):
        _all_stmts[(69823,69826)] = True
        return ast.Index(value=expr, loc=expr.loc)

    subscript__26 = Alt(subscript_1, subscript_2, subscript_3, loc=(69924,69927))
    """(2.6, 2.7) subscript: '.' '.' '.' | test | [test] ':' [test] [sliceop]"""

    subscript__30 = Alt(subscript_2, subscript_3, loc=(70069,70072))
    """(3.0-) subscript: test | [test] ':' [test] [sliceop]"""

    sliceop = Seq(Loc(":", loc=(70181,70184)), Opt(Rule("test", loc=(70195,70199)), loc=(70191,70194)), loc=(70177,70180))
    """sliceop: ':' [test]"""

    exprlist_1__26 = List(Rule("expr", loc=(70267,70271)), ",", trailing=True, loc=(70262,70266))
    exprlist_1__30 = List(Rule("star_expr", loc=(70327,70331)), ",", trailing=True, loc=(70322,70326))
    exprlist_1__32 = List(Alt(Rule("expr", loc=(70396,70400)), Rule("star_expr", loc=(70410,70414)), loc=(70392,70395)), ",", trailing=True, loc=(70387,70391))

    @action(Rule("exprlist_1", loc=(70463,70467)), loc=(70456,70462))
    def exprlist(self, exprs):
        _all_stmts[(70487,70490)] = True
        """
        (2.6, 2.7) exprlist: expr (',' expr)* [',']
        (3.0, 3.1) exprlist: star_expr (',' star_expr)* [',']
        (3.2-) exprlist: (expr|star_expr) (',' (expr|star_expr))* [',']
        """
        return self._wrap_tuple(exprs)

    @action(List(Rule("test", loc=(70781,70785)), ",", trailing=True, loc=(70776,70780)), loc=(70769,70775))
    def testlist(self, exprs):
        _all_stmts[(70820,70823)] = True
        """testlist: test (',' test)* [',']"""
        return self._wrap_tuple(exprs)

    @action(List(Seq(Rule("test", loc=(70955,70959)), Loc(":", loc=(70969,70972)), Rule("test", loc=(70979,70983)), loc=(70951,70954)), ",", trailing=True, loc=(70946,70950)), loc=(70939,70945))
    def dictmaker(self, elts):
        _all_stmts[(71019,71022)] = True
        """(2.6) dictmaker: test ':' test (',' test ':' test)* [',']"""
        return ast.Dict(keys=list(map(lambda x: x[0], elts)),
                        values=list(map(lambda x: x[2], elts)),
                        colon_locs=list(map(lambda x: x[1], elts)),
                        loc=None)

    dictorsetmaker_1 = Seq(Rule("test", loc=(71374,71378)), Loc(":", loc=(71388,71391)), Rule("test", loc=(71398,71402)), loc=(71370,71373))

    @action(Seq(dictorsetmaker_1,
                Alt(Rule("comp_for", loc=(71467,71471)),
                    List(dictorsetmaker_1, ",", leading=False, trailing=True, loc=(71505,71509)), loc=(71463,71466)), loc=(71425,71428)), loc=(71418,71424))
    def dictorsetmaker_2(self, first, elts):
        _all_stmts[(71570,71573)] = True
        if isinstance(elts, commalist):
            _all_stmts[(71619,71621)] = True
            elts.insert(0, first)
            return ast.Dict(keys=list(map(lambda x: x[0], elts)),
                            values=list(map(lambda x: x[2], elts)),
                            colon_locs=list(map(lambda x: x[1], elts)),
                            loc=None)
        else:
            _all_stmts[(71937,71941)] = True
            return ast.DictComp(key=first[0], value=first[2], generators=elts([]),
                                colon_loc=first[1],
                                begin_loc=None, end_loc=None, loc=None)

    @action(Seq(Rule("test", loc=(72167,72171)),
                Alt(Rule("comp_for", loc=(72201,72205)),
                    List(Rule("test", loc=(72244,72248)), ",", leading=False, trailing=True, loc=(72239,72243)), loc=(72197,72200)), loc=(72163,72166)), loc=(72156,72162))
    def dictorsetmaker_3(self, first, elts):
        _all_stmts[(72300,72303)] = True
        if isinstance(elts, commalist):
            _all_stmts[(72349,72351)] = True
            elts.insert(0, first)
            return ast.Set(elts=elts, loc=None)
        else:
            _all_stmts[(72471,72475)] = True
            return ast.SetComp(elt=first, generators=elts([]),
                               begin_loc=None, end_loc=None, loc=None)

    dictorsetmaker = Alt(dictorsetmaker_2, dictorsetmaker_3, loc=(72633,72636))
    """
    (2.7-)
    dictorsetmaker: ( (test ':' test (comp_for | (',' test ':' test)* [','])) |
                      (test (comp_for | (',' test)* [','])) )
    """

    @action(Seq(Loc("class", loc=(72859,72862)), Tok("ident", loc=(72873,72876)),
                Opt(Seq(Loc("(", loc=(72911,72914)), List(Rule("test", loc=(72926,72930)), ",", trailing=True, loc=(72921,72925)), Loc(")", loc=(72961,72964)), loc=(72907,72910)), loc=(72903,72906)),
                Loc(":", loc=(72989,72992)), Rule("suite", loc=(72999,73003)), loc=(72855,72858)), loc=(72848,72854))
    def classdef__26(self, class_loc, name_tok, bases_opt, colon_loc, body):
        _all_stmts[(73019,73022)] = True
        """(2.6, 2.7) classdef: 'class' NAME ['(' [testlist] ')'] ':' suite"""
        bases, lparen_loc, rparen_loc = [], None, None
        if bases_opt:
            _all_stmts[(73234,73236)] = True
            lparen_loc, bases, rparen_loc = bases_opt

        return ast.ClassDef(name=name_tok.value, bases=bases, keywords=[],
                            starargs=None, kwargs=None, body=body,
                            decorator_list=[], at_locs=[],
                            keyword_loc=class_loc, lparen_loc=lparen_loc,
                            star_loc=None, dstar_loc=None, rparen_loc=rparen_loc,
                            name_loc=name_tok.loc, colon_loc=colon_loc,
                            loc=class_loc.join(body[-1].loc))

    @action(Seq(Loc("class", loc=(73811,73814)), Tok("ident", loc=(73825,73828)),
                Opt(Seq(Loc("(", loc=(73863,73866)), Rule("arglist", loc=(73873,73877)), Loc(")", loc=(73890,73893)), loc=(73859,73862)), loc=(73855,73858)),
                Loc(":", loc=(73918,73921)), Rule("suite", loc=(73928,73932)), loc=(73807,73810)), loc=(73800,73806))
    def classdef__30(self, class_loc, name_tok, arglist_opt, colon_loc, body):
        _all_stmts[(73948,73951)] = True
        """(3.0) classdef: 'class' NAME ['(' [testlist] ')'] ':' suite"""
        arglist, lparen_loc, rparen_loc = [], None, None
        bases, keywords, starargs, kwargs = [], [], None, None
        star_loc, dstar_loc = None, None
        if arglist_opt:
            _all_stmts[(74266,74268)] = True
            lparen_loc, arglist, rparen_loc = arglist_opt
            bases, keywords, starargs, kwargs = \
                arglist.args, arglist.keywords, arglist.starargs, arglist.kwargs
            star_loc, dstar_loc = arglist.star_loc, arglist.dstar_loc

        return ast.ClassDef(name=name_tok.value, bases=bases, keywords=keywords,
                            starargs=starargs, kwargs=kwargs, body=body,
                            decorator_list=[], at_locs=[],
                            keyword_loc=class_loc, lparen_loc=lparen_loc,
                            star_loc=star_loc, dstar_loc=dstar_loc, rparen_loc=rparen_loc,
                            name_loc=name_tok.loc, colon_loc=colon_loc,
                            loc=class_loc.join(body[-1].loc))

    @action(Rule("argument", loc=(75067,75071)), loc=(75060,75066))
    def arglist_1(self, arg):
        _all_stmts[(75089,75092)] = True
        return [arg], self._empty_arglist()

    @action(Seq(Loc("*", loc=(75176,75179)), Rule("test", loc=(75186,75190)), Star(SeqN(1, Tok(",", loc=(75213,75216)), Rule("argument", loc=(75223,75227)), loc=(75205,75209)), loc=(75200,75204)),
                Opt(Seq(Tok(",", loc=(75267,75270)), Loc("**", loc=(75277,75280)), Rule("test", loc=(75288,75292)), loc=(75263,75266)), loc=(75259,75262)), loc=(75172,75175)), loc=(75165,75171))
    def arglist_2(self, star_loc, stararg, postargs, kwarg_opt):
        _all_stmts[(75309,75312)] = True
        dstar_loc = kwarg = None
        if kwarg_opt:
            _all_stmts[(75411,75413)] = True
            _, dstar_loc, kwarg = kwarg_opt

        for postarg in postargs:
            _all_stmts[(75478,75481)] = True
            if not isinstance(postarg, ast.keyword):
                _all_stmts[(75515,75517)] = True
                error = diagnostic.Diagnostic(
                    "fatal", "only named arguments may follow *expression", {},
                    postarg.loc, [star_loc.join(stararg.loc)])
                self.diagnostic_engine.process(error)

        return postargs, \
               ast.Call(args=[], keywords=[], starargs=stararg, kwargs=kwarg,
                        star_loc=star_loc, dstar_loc=dstar_loc, loc=None)

    @action(Seq(Loc("**", loc=(75997,76000)), Rule("test", loc=(76008,76012)), loc=(75993,75996)), loc=(75986,75992))
    def arglist_3(self, dstar_loc, kwarg):
        _all_stmts[(76027,76030)] = True
        return [], \
               ast.Call(args=[], keywords=[], starargs=None, kwargs=kwarg,
                        star_loc=None, dstar_loc=dstar_loc, loc=None)

    @action(SeqN(0, Rule("argument", loc=(76253,76257)), Tok(",", loc=(76271,76274)), loc=(76245,76249)), loc=(76238,76244))
    def arglist_4(self, arg):
        _all_stmts[(76286,76289)] = True
        return [], ([arg], self._empty_arglist())

    @action(Alt(Seq(Star(SeqN(0, Rule("argument", loc=(76396,76400)), Tok(",", loc=(76414,76417)), loc=(76388,76392)), loc=(76383,76387)),
                    Alt(arglist_1, arglist_2, arglist_3, loc=(76446,76449)), loc=(76379,76382)),
                arglist_4, loc=(76375,76378)), loc=(76368,76374))
    def arglist(self, pre_args, rest):
        # Python's grammar is very awkwardly formulated here in a way
        # that is not easily amenable to our combinator approach.
        # Thus it is changed to the equivalent:
        #
        #     arglist: (argument ',')* ( argument | ... ) | argument ','
        #
        _all_stmts[(76517,76520)] = True
        """arglist: (argument ',')* (argument [','] |
                                     '*' test (',' argument)* [',' '**' test] |
                                     '**' test)"""
        post_args, call = rest

        for arg in pre_args + post_args:
            _all_stmts[(77054,77057)] = True
            if isinstance(arg, ast.keyword):
                _all_stmts[(77099,77101)] = True
                call.keywords.append(arg)
            elif len(call.keywords) > 0:
                _all_stmts[(77186,77190)] = True
                error = diagnostic.Diagnostic(
                    "fatal", "non-keyword arg after keyword arg", {},
                    arg.loc, [call.keywords[-1].loc])
                self.diagnostic_engine.process(error)
            else:
                _all_stmts[(77452,77456)] = True
                call.args.append(arg)
        return call

    @action(Seq(Loc("=", loc=(77533,77536)), Rule("test", loc=(77543,77547)), loc=(77529,77532)), loc=(77522,77528))
    def argument_1(self, equals_loc, rhs):
        _all_stmts[(77562,77565)] = True
        def thunk(lhs):
            _all_stmts[(77609,77612)] = True
            if not isinstance(lhs, ast.Name):
                _all_stmts[(77637,77639)] = True
                error = diagnostic.Diagnostic(
                    "fatal", "keyword must be an identifier", {}, lhs.loc)
                self.diagnostic_engine.process(error)
            return ast.keyword(arg=lhs.id, value=rhs,
                               loc=lhs.loc.join(rhs.loc),
                               arg_loc=lhs.loc, equals_loc=equals_loc)
        return thunk

    @action(Opt(Rule("comp_for", loc=(78068,78072)), loc=(78064,78067)), loc=(78057,78063))
    def argument_2(self, compose_opt):
        _all_stmts[(78091,78094)] = True
        def thunk(lhs):
            _all_stmts[(78134,78137)] = True
            if compose_opt:
                _all_stmts[(78162,78164)] = True
                generators = compose_opt([])
                return ast.GeneratorExp(elt=lhs, generators=generators,
                                        begin_loc=None, end_loc=None,
                                        loc=lhs.loc.join(generators[-1].loc))
            return lhs
        return thunk

    @action(Seq(Rule("test", loc=(78504,78508)), Alt(argument_1, argument_2, loc=(78518,78521)), loc=(78500,78503)), loc=(78493,78499))
    def argument(self, lhs, thunk):
        # This rule is reformulated to avoid exponential backtracking.
        _all_stmts[(78552,78555)] = True
        """
        (2.6) argument: test [gen_for] | test '=' test  # Really [keyword '='] test
        (2.7-) argument: test [comp_for] | test '=' test
        """
        return thunk(lhs)

    list_iter = Alt(Rule("list_for", loc=(78867,78871)), Rule("list_if", loc=(78885,78889)), loc=(78863,78866))
    """(2.6, 2.7) list_iter: list_for | list_if"""

    def list_comp_for_action(self, for_loc, target, in_loc, iter, next_opt):
        _all_stmts[(78958,78961)] = True
        def compose(comprehensions):
            _all_stmts[(79039,79042)] = True
            comp = ast.comprehension(
                target=target, iter=iter, ifs=[],
                loc=for_loc.join(iter.loc), for_loc=for_loc, in_loc=in_loc, if_locs=[])
            comprehensions += [comp]
            if next_opt:
                _all_stmts[(79293,79295)] = True
                return next_opt(comprehensions)
            else:
                _all_stmts[(79366,79370)] = True
                return comprehensions
        return compose

    def list_comp_if_action(self, if_loc, cond, next_opt):
        _all_stmts[(79438,79441)] = True
        def compose(comprehensions):
            _all_stmts[(79501,79504)] = True
            comprehensions[-1].ifs.append(cond)
            comprehensions[-1].if_locs.append(if_loc)
            comprehensions[-1].loc = comprehensions[-1].loc.join(cond.loc)
            if next_opt:
                _all_stmts[(79719,79721)] = True
                return next_opt(comprehensions)
            else:
                _all_stmts[(79792,79796)] = True
                return comprehensions
        return compose

    list_for = action(
        Seq(Loc("for", loc=(79895,79898)), Rule("exprlist", loc=(79907,79911)),
            Loc("in", loc=(79937,79940)), Rule("testlist_safe", loc=(79948,79952)), Opt(Rule("list_iter", loc=(79975,79979)), loc=(79971,79974)), loc=(79891,79894)), loc=(79875,79881)) \
        (list_comp_for_action)
    """(2.6, 2.7) list_for: 'for' exprlist 'in' testlist_safe [list_iter]"""

    list_if = action(
        Seq(Loc("if", loc=(80141,80144)), Rule("old_test", loc=(80152,80156)), Opt(Rule("list_iter", loc=(80174,80178)), loc=(80170,80173)), loc=(80137,80140)), loc=(80121,80127)) \
        (list_comp_if_action)
    """(2.6, 2.7) list_if: 'if' old_test [list_iter]"""

    comp_iter = Alt(Rule("comp_for", loc=(80304,80308)), Rule("comp_if", loc=(80322,80326)), loc=(80300,80303))
    """
    (2.6) gen_iter: gen_for | gen_if
    (2.7-) comp_iter: comp_for | comp_if
    """

    comp_for = action(
        Seq(Loc("for", loc=(80469,80472)), Rule("exprlist", loc=(80481,80485)),
            Loc("in", loc=(80511,80514)), Rule("or_test", loc=(80522,80526)), Opt(Rule("comp_iter", loc=(80543,80547)), loc=(80539,80542)), loc=(80465,80468)), loc=(80449,80455)) \
        (list_comp_for_action)
    """
    (2.6) gen_for: 'for' exprlist 'in' or_test [gen_iter]
    (2.7-) comp_for: 'for' exprlist 'in' or_test [comp_iter]
    """

    comp_if__26 = action(
        Seq(Loc("if", loc=(80771,80774)), Rule("old_test", loc=(80782,80786)), Opt(Rule("comp_iter", loc=(80804,80808)), loc=(80800,80803)), loc=(80767,80770)), loc=(80751,80757)) \
        (list_comp_if_action)
    """
    (2.6) gen_if: 'if' old_test [gen_iter]
    (2.7) comp_if: 'if' old_test [comp_iter]
    """

    comp_if__30 = action(
        Seq(Loc("if", loc=(81000,81003)), Rule("test_nocond", loc=(81011,81015)), Opt(Rule("comp_iter", loc=(81036,81040)), loc=(81032,81035)), loc=(80996,80999)), loc=(80980,80986)) \
        (list_comp_if_action)
    """
    (3.0-) comp_if: 'if' test_nocond [comp_iter]
    """

    testlist1 = action(List(Rule("test", loc=(81183,81187)), ",", trailing=False, loc=(81178,81182)), loc=(81171,81177))(_wrap_tuple)
    """testlist1: test (',' test)*"""

    @action(Seq(Loc("yield", loc=(81287,81290)), Opt(Rule("testlist", loc=(81305,81309)), loc=(81301,81304)), loc=(81283,81286)), loc=(81276,81282))
    def yield_expr__26(self, yield_loc, exprs):
        _all_stmts[(81329,81332)] = True
        """(2.6, 2.7, 3.0, 3.1, 3.2) yield_expr: 'yield' [testlist]"""
        if exprs is not None:
            _all_stmts[(81452,81454)] = True
            return ast.Yield(value=exprs,
                             yield_loc=yield_loc, loc=yield_loc.join(exprs.loc))
        else:
            _all_stmts[(81605,81609)] = True
            return ast.Yield(value=None,
                             yield_loc=yield_loc, loc=yield_loc)

    @action(Seq(Loc("yield", loc=(81734,81737)), Opt(Rule("yield_arg", loc=(81752,81756)), loc=(81748,81751)), loc=(81730,81733)), loc=(81723,81729))
    def yield_expr__33(self, yield_loc, arg):
        _all_stmts[(81777,81780)] = True
        """(3.3-) yield_expr: 'yield' [yield_arg]"""
        if isinstance(arg, ast.YieldFrom):
            _all_stmts[(81880,81882)] = True
            arg.yield_loc = yield_loc
            arg.loc = arg.loc.join(arg.yield_loc)
            return arg
        elif arg is not None:
            _all_stmts[(82034,82038)] = True
            return ast.Yield(value=arg,
                             yield_loc=yield_loc, loc=yield_loc.join(arg.loc))
        else:
            _all_stmts[(82183,82187)] = True
            return ast.Yield(value=None,
                             yield_loc=yield_loc, loc=yield_loc)

    @action(Seq(Loc("from", loc=(82312,82315)), Rule("test", loc=(82325,82329)), loc=(82308,82311)), loc=(82301,82307))
    def yield_arg_1(self, from_loc, value):
        _all_stmts[(82344,82347)] = True
        return ast.YieldFrom(value=value,
                             from_loc=from_loc, loc=from_loc.join(value.loc))

    yield_arg = Alt(yield_arg_1, Rule("testlist", loc=(82538,82542)), loc=(82521,82524))
    """(3.3-) yield_arg: 'from' test | testlist"""
