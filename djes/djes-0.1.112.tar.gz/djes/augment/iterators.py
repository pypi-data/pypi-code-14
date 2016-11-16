import six

from djes.search import LazySearch
from .wrappers import SearchWrapper


class AugmentedSearchIterator(object):
    """This manages multiple LazySearch objects.self

     Allows for indexing multiple elasticsearch queries."""

    def __init__(self, *args):
        self._searches = self.init_searches(*args)
        self._results = []

    def __getitem__(self, n):
        if isinstance(n, int):
            if n >= len(self._results):
                _search = self.get_search(n)
                try:
                    self._results.append(six.next(_search))
                except StopIteration:
                    _search._exhausted = True
                    return self.__getitem__(n)
            return self._results[n]
        raise TypeError('''AugmentedSearchIterator can only be indexed by an integer''')

    def get_search(self, n):
        """Should return a search based on priority based on search exhuastion and validators.

        RULES:
        1. SearchWrapper.exhausted = False.
        2. First SearchWrapper.is_valid({result_index}) = True.
        3. If none of them return `is_valid({result_index}) = True` return first SearchWrapper.exhausted = False.
        """

        _search = None
        for search in self._searches:
            if search._exhausted:
                continue
            elif search.is_priority(n):
                _search = search
                break
            elif not _search:
                _search = search
        return _search

    def init_searches(self, *args):
        _searches = []
        for search in args:
            if isinstance(search, LazySearch):
                _searches.append(SearchWrapper(search))
            elif isinstance(search, tuple):
                if len(search) != 2:
                    raise ValueError(
                        "SearchWrapper tuple must be of length 2"
                        "e.g., (SearchInstance, [{validators..}])"
                    )
                _searches.append(SearchWrapper(search[0], validators=search[1]))
        return _searches

    @property
    def search(self):
        for search in self._searches:
            if not search._exhausted:
                return search
