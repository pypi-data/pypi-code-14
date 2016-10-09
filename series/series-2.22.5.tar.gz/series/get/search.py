import re
import itertools

import requests

import lxml

from amino.lazy import lazy
from amino import List, LazyList, _, L

from tek_utils.sharehoster.torrent import SearchResultFactory
from tek_utils.sharehoster.kickass import NoResultsError

from series.get import ReleaseMonitor
from series.logging import Logging


class SearchQuery:

    def __init__(self, monitor: ReleaseMonitor, res: str) -> None:
        self.monitor = monitor
        self.release = self.monitor.release
        self.res = res

    @property
    def _enum(self):
        return 's{:0>2}e{:0>2}'.format(self.release.season,
                                       self.release.episode)

    @property
    def _name(self):
        return self.release.name.replace('_', ' ').replace('\'', '')

    @property
    def query(self):
        return '{} {} {}'.format(
            self._name,
            self._enum,
            self.res,
        )

    @property
    def valid(self):
        return True

    @property
    def search_string(self):
        return self.release.search_string_with_res(self.res, False)

    @lazy
    def search_re(self):
        return re.compile(self.search_string, re.I)

    @property
    def desc(self):
        return 'torrent {} {}'.format(self.release, self.res)


class DateQuery(SearchQuery):

    @property
    def _enum(self):
        return self.release.airdate.strftime('%Y-%m-%d')

    @property
    def valid(self):
        return self.release.has_airdate

    @property
    def search_string(self):
        return self.release.search_string_with_res(self.res, True)


class SearchResults:

    def __init__(self, monitor, query, results, min_seeders) -> None:
        self.monitor = monitor
        self.query = query
        self.results = results
        self.min_seeders = min_seeders

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.results)

    @property
    def choose(self):
        matcher = self.query.search_re
        valid = (
            self.results
            .filter(lambda a: a.seeders is not None)
            .filter(_.seeders > self.min_seeders)
        )
        return (
            valid
            .filter(lambda a: matcher.search(a.title))
            .filter(_.magnet_link)
            .filter_not(lambda a: self.monitor.contains_torrent(a.magnet_link))
            .head
        )


class TorrentSearch(Logging):

    def __init__(self, requester, search_engine, min_seeders) -> None:
        self.requester = requester
        self.search_engine = search_engine
        self.min_seeders = min_seeders
        self._limit = 10

    @lazy
    def _search(self):
        return (self._search_tpb if self.search_engine == 'piratebay' else
                self._search_kickass)

    def _search_tpb(self, query):
        from tek_utils.sharehoster import piratebay
        bay = piratebay.Search(query)
        return bay.run[:self._limit] / SearchResultFactory.from_tpb

    def _search_kickass(self, query):
        from tek_utils.sharehoster import kickass
        search = kickass.Search(query).order(kickass.ORDER.SEED,
                                             kickass.ORDER.DESC)
        return List.wrap(SearchResultFactory.from_kickass(res) for res in
                         itertools.islice(search, self._limit))

    def _queries(self, monitor):
        q = lambda r: List(SearchQuery(monitor, r), DateQuery(monitor, r))
        return monitor.resolutions // q

    def search(self, monitor):
        return (
            LazyList(self._queries(monitor))
            .filter(_.valid)
            .apzip(self._safe_search)
            .map2(L(SearchResults)(monitor, _, _, self.min_seeders))
        )

    def _safe_search(self, query):
        self.log.debug(
            'Search {} for {}: {}'.format(query.desc, self.requester,
                                          query.query))
        try:
            return List.wrap(self._search(query.query))
        except NoResultsError as e:
            self.log.debug('Error searching for torrent: {}'.format(e))
        except requests.RequestException as e:
            self.log.warning(
                'Connection failure in {} search'.format(self.search_engine))
        except lxml.etree.XMLSyntaxError as e:
            self.log.warning('Parse error in kickass results: {}'.format(e))
        return List()

__all__ = ('TorrentSearch',)
