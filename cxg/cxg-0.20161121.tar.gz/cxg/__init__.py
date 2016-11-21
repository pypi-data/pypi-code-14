#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

import logging
import bisect
import math
from collections import defaultdict, namedtuple
from itertools import product
from operator import itemgetter, mul
from functools import reduce
import datetime

import pandas

logger = logging.getLogger("cxg")
logger.setLevel(logging.DEBUG)


def dict_to_object(obj, dct):
    for key, value in dct.items():
        setattr(obj, key, value)


config_proto = dict(
    mutate = True,

    reorder_penalty = -1,
    mutate_penalty = -10,
    unmatched_penalty = -10,
    cx_bonus = 1,
    factor = 0,

    minimum_rate = 0.5,
    last_rate = 1,
    delta_rate = 1,
)


class config:
    pass

dict_to_object(config, config_proto)


def lprint(l, msg=''):
    l = list(l)
    print("{} - {}::".format(msg, len(l)))
    for i in l:
        print(i)


def unique(items):
    seen = {}
    return [seen.setdefault(x, x) for x in items if x not in seen]


def format_2cols(col1, col2, title=''):
    def formatter(df, col):
        return '{{:<{}s}}'.format(df[col].str.len().max()).format

    df = pandas.DataFrame(dict(a=[str(x) for x in col1],
                               b=[str(x) for x in col2]))
    formatters = {'a': formatter(df, 'a'), 'b': formatter(df, 'b')}
    return title + df.to_string(header=False, formatters=formatters)


class TraceItem:
    "A TraceStep is a list of TraceItem"

    def __init__(self, cx):
        assert isinstance(cx, Cx)
        self.cx = cx
        self.stem = cx.pattern[cx.index - 1]
        self.expected = self.stem.value

    @property
    def trust(self):
        if not isinstance(self.cx, Cx):
            return 0

        return self.cx.trust

    def __lt__(self, other):
        return self.trust < other.trust

    def __repr__(self):
        stem = self.stem if self.stem else "-"
        return "{} {} {:.1f}>{}".format(
            self.cx.simple_repr(), stem, self.trust, self.expected)


class BriefTraceItem:
    def __init__(self, traceitem):
        self.traceitem = traceitem

    def __repr__(self):
        return "{} {}".format(self.traceitem.cx.simple_repr(), self.traceitem.stem)


class TraceStep(list):
    "A trace is a list of TraceStep"
    def __init__(self, *args):
        super().__init__(*args)
        self.any_match = False

    def get_clean(self):
        retval = TraceStep()
        retval.any_match = self.any_match

        for item in self:
            if item.cx.matched:
                retval.append(item)

        return retval


class Trace(list):
    def __init__(self):
        super().__init__()
        self._votes = None

    def brief(self):
        retval = []
        for step in self:
            retval.append([BriefTraceItem(i) for i in step.get_clean()])

        return retval

    def sort(self):
        for item in self:
            item.sort(reverse=True)

    def show(self):
        self.sort()
        logger.debug("trace:")
        for line in self:
            logger.debug(line)

    def get_votes(self, minimum_rate=config.minimum_rate):
        if self._votes is None:
            self._votes = self._get_votes(minimum_rate)

        return self._votes

    def _get_votes(self, minimum_rate):
        retval = []

        for r in self:
            vote_map = defaultdict(lambda: 0)
            for vote in r:
                vote_map[vote.stem] += vote.trust

            votes = [Ballot(v, c) for v, c in vote_map.items()]
            if minimum_rate:
                votes = [b for b in votes if b.trust >= minimum_rate]

            votes.sort(key=itemgetter(1), reverse=True)
            retval.append(votes)

        return retval


class Ballot(namedtuple('Ballot', ['candidate', 'trust'])):
    def __repr__(self):
        return "({}, {:.1f})".format(self.candidate, self.trust)


class OverrunToken(Exception):
    pass


class BrokenRestriction(Exception):
    pass


class Token(list):
    "it's a list of likely input values"
    def __init__(self, *raw_values):
        super().__init__(raw_values)
        self.last = False
        self.changed = False

    def copy(self):
        if self.changed:
            raise OverrunToken()

        retval = Token(*self[:])
        retval.last = self.last
        retval.changed = True
        return retval

    def find(self, stem):
        for i, x in enumerate(self):
            if stem.equals(x):
                return i

        return None

    def reorder(self, index):
        retval = self.copy()
        retval[0], retval[index] = retval[index], retval[0]
        return retval

    def mutate(self, value):
        if not config.mutate:
            return

        retval = self.copy()
        retval[:0] = [value]
        return retval


# def isiterable(value):
#     try:
#         iter(value)
#         return True
#     except TypeError:
#         pass

#     return False


class Stem:
    def __init__(self, value):
        self.value = value
        if not hasattr(self, 'sign'):
            self.sign = self.__class__.__name__ + '.'

    def equals(self, input_value):
        return self.value == input_value

    def __eq__(self, other):
        return isinstance(other, Stem) and self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return "{}{}".format(self.sign, self.value)


class Simple(Stem):
    sign = '='

    def parse(self, token, cx):
        try:
            pos = token.find(self)
            if pos == 0:
                return 1

            if pos is None:
                return 0

            return 0.5

        except OverrunToken:
            pass

        return 0


class FixedPos(Simple):
    def __init__(self, value, position):
        super().__init__(value)
        self.position = position

    def parse(self, token, cx):
        if cx.offset != 0:
            raise BrokenRestriction()

        return super().parse(token, cx)


# FIXME: should be first in pattern
class Begin(FixedPos):
    sign = '^'

    def __init__(self, value):
        super().__init__(value, 0)


# FIXME: should be last in pattern
class End(Simple):
    sign = '$'

    def parse(self, token, cx):
        if not token.last:
            raise BrokenRestriction()

        return super().parse(token, cx)


# FIXME: Or may be a factory creating a Cx per each
# class Or(Stem):
#     sign = '|'

#     def __init__(self, *values):
#         self.values = values

#     def try_parse(self, token, cx):
#         found_at = []

#         for v in self.values:
#             pos = token.find(v)
#             found_at.append((pos, v))
#             if pos == 0:
#                 self.value = v
#                 return 1

#         for pos, value in found_at:
#             if pos is None:
#                 cx.mutate_token(token.copy(), value)
#             else:
#                 cx.reorder_token(token.copy(), pos)

#         # FIXME: return 0.5 if value in group[1:]
#         return 0

#     def parse(self, token, cx):
#         try:
#             return self.try_parse(token, cx)
#         except OverrunToken:
#             return 0


class PatternProcess(type):
    def __init__(cls, name, bases, dct):
        type.__init__(cls, name, bases, dct)
        cls.pattern = cls.process_pattern(cls.pattern)

    @classmethod
    def process_pattern(cls, pattern):
        retval = []
        for p in pattern:
            if isinstance(p, Stem):
                retval.append(p)
            else:
                retval.append(Simple(p))

        return retval


class Cx(metaclass=PatternProcess):
    pattern = tuple()

    def __init__(self, offset):
        self.offset = offset
        self.index = 0
        self.match = True
        self.trust = 0
        self.enabled = True

    def parse(self, token):
        assert not self.completed
        if not self.enabled:
            return

        stem = self.pattern[self.index]

        try:
            score = stem.parse(token, self)
            self.trust += score

            if score == 1:
                return stem

        except BrokenRestriction:
            self.trust = 0
            self.enabled = False

        finally:
            self.index += 1

        self.match = False

    @property
    def completed(self):
        return self.index == len(self.pattern) or not self.enabled

    @property
    def matched(self):
        return self.completed and self.match

    def __lt__(self, other):
        return self.offset < other.offset

    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
            self.offset == other.offset

    def simple_repr(self):
        m = '/' if not self.matched else ''
        return "{}{}:{}".format(
            m, self.__class__.__name__, self.offset)

    def __repr__(self):
        return "{} {:.1f}".format(self.simple_repr(), self.trust)


class Serie(list):
    def __init__(self, data=None):
        self[:] = data or []

    @classmethod
    def from_data(cls, raw_serie):
        return Serie([Token(*x) for x in raw_serie])

    def promote(self, stems):
        retval = self.copy()

        for index, (stem, token) in enumerate(zip(stems, self)):
            pos = token.find(stem)

            if pos not in [0, None]:
                retval[index] = token.reorder(pos)

            if pos is None:
                retval[index] = token.mutate(stem.value)

        return retval

    def copy(self):
        return Serie(self[:])

    @property
    def main(self):
        return [x[0] for x in self]

    def __repr__(self):
        return "<Serie:{}>".format(self.main)


class Result:
    def __init__(self, serie=None, cxs=None, score=0):
        self.serie = serie.copy() if serie else Serie()
        self.cxs = cxs or []
        self.trace = Trace()
        self.score = score

    def get_top_rated_per_token(self, last_rate=config.last_rate):
        retval = []

        for token_votes, token in zip(self.trace.get_votes(), self.serie):
            if not token_votes:
                retval.append([Simple(token[0])])
                continue

            if len(token_votes) == 1:
                retval.append([token_votes[0].candidate])
                continue

            rates = sorted({b.trust for b in token_votes}, reverse=True)
            # print("RATES", list(rates), last_rate)

            cut = rates[0]
            for i, r in enumerate(rates):
                if (rates[0] - r) > config.delta_rate or i > last_rate:
                    break
                cut = r

#            cut = rates[last_rate] if len(rates) > last_rate else rates[-1]

            elegibles = [b.candidate for b in token_votes if b.trust >= cut]
            # print("CUT  ", list(rates), cut)
            # print("ELEGI", elegibles)
            retval.append(elegibles)

        return retval

    def __eq__(self, other):
        return (self.serie, self.cxs) == (other.serie, other.cxs)

    def __lt__(self, other):
        if self.score == other.score:
            return len(self.cxs) > len(other.cxs)

        return self.score > other.score

    def composed_trace(self):
        retval = []
        for i, d in enumerate(self.serie):
            retval.append((d, self.trace[i]))

        return retval

    def format_trace(self):
        return format_2cols(self.serie, self.trace.brief())

    # FIXME: call by the engine
    # def apply_scores(self, original):
    #     trace.clean()
    #     count_unmatching_tokens

    def commit(self, original):
        def count_matched_cx(step):
            return sum(isinstance(item.cx, Cx) and item.cx.matched for item in step)

        unmatched_tokens = 0
        for i, step in enumerate(self.trace):
            cx_this_step = count_matched_cx(step)

            if cx_this_step:
                step.any_match = True
                continue

            unmatched_tokens += 1

        self.unmatched_tokens = unmatched_tokens
        self._apply_all_scores(original)

    def _apply_all_scores(self, original):
        def apply_score(score, msg=""):
            if not score:
                return

            self.score += score
            # logger.debug("scored {:+} to {} by '{}'".format(
            #     score, self, msg))

        def original_changes():
            for this, orig in zip(self.serie, original):
                try:
                    pos = orig.index(this[0])
                    if pos != 0:
                        apply_score(config.reorder_penalty, "reorder")

                except ValueError:
                    apply_score(config.mutate_penalty, "mutate")

        original_changes()
        apply_score(self.unmatched_tokens * config.unmatched_penalty,
                    'unmatched tokens')
        apply_score(len(self.cxs) * config.cx_bonus,
                    "matched Cxs")

    def full_matching(self):
        return self.unmatched_tokens == 0

    def __repr__(self):
        cxs = str.join(', ', [cx.simple_repr() for cx in self.cxs])
        return "<Result{:+} {} [{}]>".format(self.score, self.serie, cxs)


class Engine:
    def __init__(self, cxs, serie, config_=None):
        self.cx_protos = set(cxs)
        self.series = []
        self.preseries = []
        self.visited_series = []
        self.results = []
        self.better_score = None
        self.some_full_matching = False

        self.processed = 0
        self.tini = 0
        self.elapsed = 0

        self.apply_config(config_)
        self.worst_case = config.unmatched_penalty * len(serie)

        if not isinstance(serie, Serie):
            serie = Serie.from_data(serie)

        self.original = serie
        self.add_serie(serie)
        serie[-1].last = True

    @staticmethod
    def apply_config(config_=None):
        global config
        dict_to_object(config, config_proto)

        if not config_:
            return

        dict_to_object(config, config_)

    def add_series(self, series):
        self.preseries.extend(series)

    def add_serie(self, serie):
        if not self.suitable_serie(serie):
            return

        logger.debug("-- add_serie {}".format(serie))
        self.visited_series.append(serie)
        self.series.append(serie)
        # bisect.insort_left(self.series, serie)

    def suitable_serie(self, serie):
        # print("visited:", serie)
        # for i, visited in enumerate(self.visited_series):
        #     lprint(visited[:], i)

        if serie in self.visited_series:
            return False

        # if self.better_score is None:
        #     return True

        # if serie.score < self.average_score():
        #     return False

        return True

    def average_score(self):
        range_ = (self.better_score - self.worst_case)
        percent = math.ceil(config.factor * range_ / 100)
        return min(self.better_score + percent, 0)

    def run(self):
        tini = datetime.datetime.now()
        while self.series:
            #  if len(self.results) > 5; break
            self.current_serie = self.series.pop()
            self.run_serie(self.current_serie)  # copy required?

        self.elapsed_time = datetime.datetime.now() - tini
        return self

    def run_serie(self, serie):
        # logger.debug("run-serie: %s", serie)

        # if serie.score >= self.average_score():
        #     return

        self.processed += 1
        parser = Parser(self.cx_protos, self)
        parser.process_serie(serie)
        self.add_result(parser.result)

        for serie in self.preseries:
            self.add_serie(serie)

        self.preseries = []

        # print("\nSeries:")
        # for s in self.series:
        #     print(s)

    def add_result(self, result):
        logger.debug("add-result %s", result)
        if not result.cxs:
            return

        if self.better_score is None:
            self.better_score = result.score

        if result.full_matching():
            self.some_full_matching = True

        improve = result.score - self.better_score
        if improve > 0:
            self.better_score = result.score
            self.worst_case += improve

            logger.debug("better:{} avg:{} worst:{}".format(
                self.better_score, self.average_score(), self.worst_case))

        # print("result:", result)
        self.results.append(result)

    def get_results(self):
        retval = sorted(self.results)
        if self.some_full_matching:
            retval = [r for r in retval if r.full_matching()]

        return retval


class Parser:
    def __init__(self, cx_protos=None, engine=None):
        self.cx_protos = cx_protos or []
        self.engine = engine
        self.reset()

    def reset(self):
        self.cx_active = []
        self.index = 0
        self.result = Result()

    def process_serie(self, serie):
        if not isinstance(serie, Serie):
            raise TypeError(serie, "Not such a Serie")

        logger.debug("\n--- parse serie %s", serie)

        self.reset()
        self.result.serie = serie
        for token in serie:
            self.process(token)

        self.result.trace.show()
        self.result.commit(self.engine.original)
        self.create_new_series()

    def create_new_series(self):
        self.engine.add_series([self.gen_revert_not_matched()])
        self.engine.add_series(self.gen_top_rated_series())

    def gen_revert_not_matched(self):
        retval = self.result.serie.copy()

        for i, step in enumerate(self.result.trace):
            if not step.any_match:
                retval[i] = self.engine.original[i]

        return retval

    def gen_top_rated_series(self):
        def calculate_total(votes):
            return reduce(mul, (len(x) for x in votes))

        retval = []
        rserie = self.result.serie

        # logger.debug(format_2cols(self.get_votes(), self.result.serie,
        #                          title='votes|serie:\n'))

        top_rated = self.result.get_top_rated_per_token()
        # lprint(top_rated, 'top rated')
        # print("combinations:", calculate_total(top_rated))

        for candidates in product(*top_rated):
            try:
                retval.append(rserie.promote(candidates))
            except OverrunToken:
                pass

        return retval

    def process(self, token):
        logger.debug("-- parsing token %s", token)

        for proto in self.cx_protos:
            instance = proto(self.index)
            self.cx_active.append(instance)

        trace_step = TraceStep()

        for c in self.cx_active[:]:
            c.parse(token)
            if c.enabled:
                trace_step.append(TraceItem(c))

            if not c.completed:
                continue

            self.cx_active.remove(c)

            if c.matched:
                self.result.cxs.append(c)

        self.index += 1
        self.result.trace.append(trace_step)
        self.show_status()

    def set_cxs(self, cxs):
        self.cx_protos = cxs

    def show_status(self):
        logger.debug("active:  %s", self.cx_active)
        logger.debug("matched: %s", self.result.cxs)
