#!/usr/bin/env python3
"""A module for creating Markov models of sequences
and generating sequences based on that model."""


import pprint as pp
import re
import random
import time
import itertools
import bisect
from collections import Counter


class InvalidStateError(Exception):

    """A simple exception to indicate chain referencing a nonexistent state."""
    pass


class Head():

    """A dummy class used to anchor the beginning of an input chain."""

    def __len__(self):
        return 0

    def __str__(self):
        return "[Head]"

    def __repr__(self):
        return "[Head]"

    def __cmp__(self, other):
        if isinstance(other, str):
            return -1


class Tail():

    """A dummy class used to anchor the end of an input chain."""

    def __len__(self):
        return 0

    def __str__(self):
        return "[Tail]"

    def __repr__(self):
        return "[Tail]"

    def __cmp__(self, other):
        if isinstance(other, str):
            return 1


class Markov:

    """Get a lot of input and produce a short output multiple times.
    Input should be lists of strings beginning with an emptystring.
    The Head object is used as the entry point every time generate() is called."""
    empty = dict()
    start = Head()

    def __init__(self, seeds=None, orders=(0,), discrete_mode=True):
        """Seeds should be an iterable of iterables.
        This is so that entry points can be determined automatically.
        discrete_mode=True Enables analysis of chains as having start and end points.
        discrete_mode=False treats all chains as a continuous time series, more or less.
        When discrete_mode=False, each seed must have 2 states.
        That is in order to establish a transition."""
        if seeds is None:
            seeds = []
        if 0 not in orders:
            raise ValueError("0 is a required order.")
        self.transitions = self.empty.copy()
        self.orders = sorted(orders)[::-1]  # force orders to be descending
        # self.cur_state = self.start
        self.discrete = discrete_mode
        self.feed(seeds)

    def feed(self, seeds):
        """Feed the generator with a list of lists, called seeds.
        I.e. m = pymarkoff.Markov()
        m.feed([['The','quick','brown','fox','jumped','over','the','lazy','dog.']])
        m.generate() => ['The','lazy','dog.']

        """
        for seed in seeds:
            # go throug each seed

            # Handle string seeds
            if isinstance(seed) == str:
                seed = list(seed)
            # prep it if in discrete mode.
            if self.discrete:
                seed = [Head()] + seed + [Tail()]
            # go through all user-specified orders
            # or 'state lengths'

            for cur_order in self.orders:
                for i in range(len(seed) - cur_order):
                    try:
                        # assume that the given state has been previously
                        # recorded
                        head = tuple(
                            s for s in seed[i:i + cur_order + 1] if len(s) > 0)

                        tail = seed[i + cur_order + 1]
                        self.transitions[head].update([tail])
                    except KeyError:
                        # If the current state has not been seen before,
                        # record it.
                        self.transitions[head] = Counter([tail])
                    except IndexError:
                        pass

    def get_next(self, state):
        """Takes a tuple of one or more states and predicts the next one.
        Example:
            If the object has been fed the string 'Bananas',
                In: ('B',)  Out: 'a'
        """
        try:
            choice = weighted_random(
                *list(
                    zip(
                        *list(
                            self.transitions[state].items())[::-1]
                    )
                )
            )
        except KeyError:
            raise InvalidStateError("state {} never fed in. Brain:{}".format(
                repr(state), dict(self).keys()))
        return choice

    def generate(self, *, max_length=100):
        """Returns a list of states chosen by simulation.
        Simulation starts from a state chosen fro mknown head states
        and ends at either a known terminating state or when the chain
        reaches max_length, whichever comes first."""
        result = []
        state = Head()
        choice = state
        i = 0
        while i <= max_length and not isinstance(state, Tail):
            # check for transitions in the highest allowed order first
            # then check lower orders
            for cur_order in self.orders[::-1]:
                try:
                    # reach back for a sequence of states of length less equal
                    # to the current order.
                    temp_state = tuple(result[-(cur_order + 1):len(result)])
                    # choice = random.choice(self.transitions[temp_state])
                    choice = self.get_next(temp_state)
                    break
                except InvalidStateError:
                    # An InvalidStateError happens when there aren't transitions for an
                    # arbitrary higher order state
                    # In which case, carry on and continue to the next lowest
                    # order.
                    pass

            state = choice
            result.append(choice)
            i += 1
        return result[:-1]  # slice off the tail

    def __str__(self):
        return str(self.transitions)

    def __iter__(self):
        for item in self.transitions.items():
            # yield (t[0],sorted(t[1]))
            yield item


def weighted_random(choices, weights):
    """Randomly choose an item from choices weighted by weights."""
    cumdist = list(itertools.accumulate(weights))
    cursor = random.random() * cumdist[-1]
    return choices[bisect.bisect(cumdist, cursor)]


def filter_by_user(data):
    """Return a list from data where each item was allowed by the user."""

    good = []
    for sentence in data:
        print(sentence)
        res = input("Good? y/n >>>").lower()
        if res == 'y':
            good.append(sentence)
        elif res == 'e':
            break
        else:
            pass
    return good


def main():
    """Interactive mode. Mostly used for testing."""
    # I have been playing a lot of Overwatch lately.
    s = """Ana
Bastion
D.Va
Genji
Hanzo
Junkrat
Lúcio
McCree
Mei
Mercy
Pharah
Reaper
Reinhardt
Roadhog
Soldier: 76
Symmetra
Torbjörn
Tracer
Widowmaker
Winston
Zarya
Zenyatta"""
    seeds = [list(i) for i in s.split('\n')]
    seeds = [
        "The quick brown fox jumped over the lazy dog.",
        "Jack and Jill ran up the hill to fetch a pail of water.",
        "Whenever the black fox jumped the squirrel gazed suspiciously."
    ]
    seeds = [i.split(' ') for i in seeds]
    pp.pprint(seeds, width=80)
    m = Markov(seeds, (0, 1))
    print(dict(m).keys())
    print(m.get_next(("the",)))
    # results_f = [' '.join(m.generate(max_length=30)) for i in range(10)]
    # pp.pprint(results_f,width=80)
    # pp.pprint(results_f)
    # pp.pprint(dict(m))
if __name__ == '__main__':
    main()

    # from itertools import product
# combs = '\n'.join(' '.join([''.join(line) for line in zip(*sol)])
#                   for sol in product(permutations(prefixes), permutations(suffixes)))
# print(combs)
