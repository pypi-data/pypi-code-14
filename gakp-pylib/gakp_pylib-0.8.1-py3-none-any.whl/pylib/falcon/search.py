import itertools
import re
from collections import namedtuple
from pylib.lib import maybe

Engine = namedtuple('Engine', ['handlers', 'default'])


def create_engine(default=None):
    """
    Creates a search engine. The default parameter is used for managing scenarios
    where the search query is None.
    @sig create_engine :: (* -> [a]) -> Engine
    """
    default = default if default else lambda *args, **kwargs: []
    return Engine([], default)


def search_with(engine, criteria):
    """
    Adds a search handler that handles only queries that pass the given
    criteria.
    @sig search_with :: Engine -> (Str -> Bool) -> ((* -> [a]) -> (* -> [a]))
    """
    def decorator(f):
        engine.handlers.append(maybe(f, criteria))
        return f
    return decorator


def search(engine, query, *args, **kwargs):
    """
    Generates a reduced result of all the results of all the handlers that of
    which the query pass their criteria.
    @sig search :: Engine -> Str -> * -> [a]
    """
    if query is None:
        return engine.default(*args, **kwargs)

    # mapping the mapped results in cases of None
    results = [[] if x is None else x for x in [f(query.strip(), *args, **kwargs) for f in engine]]
    return list(itertools.chain(*results))


def regex_criteria(regex, match=False):
    """
    Create a function to test queries based on the given regex. The match parameter
    makes the criteria function only pass when the query is a full match of the
    criteria.
    @sig regex_criteria :: RegExp -> Bool -> (Str -> Bool)
    """
    regex = re.compile(regex)

    def criteria(query):
        return bool(regex.match(query) if match else regex.search(query))
    return criteria
