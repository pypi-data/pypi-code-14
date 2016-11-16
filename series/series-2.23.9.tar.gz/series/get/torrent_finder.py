from datetime import datetime

from series.get.handler import R, ProcessHandler, ThreadHandler
from series.condition import LambdaCondition
from series.get.search import TorrentSearch, SearchResults, SearchQuery
from series.util import now_unix

from golgi.config import configurable

from tek_utils.sharehoster.torrent import SearchResult

from amino import F, __, Just


@configurable(torrent=['search_engine'], get=['torrent_recheck_interval',
                                              'min_seeders'])
class TorrentFinder(ThreadHandler):

    def __init__(self, releases, *a, **kw):
        super().__init__(2, releases, 5, 'torrent finder',
                         cooldown=self._torrent_recheck_interval, **kw)

    def _create_async(self, monitor):
        self.log.info('Torrent search: {}'.format(monitor.release))
        self._update(monitor, last_torrent_search=datetime.now())
        return Just(TorrentSearch(monitor, self._description,
                                  self._search_engine, self._min_seeders))

    def _clean_done(self, a):
        return a.proc.result // __.find(self._process_results) | False

    def _clean_timeout(self, proc):
        pass

    def _process_results(self, results: SearchResults):
        return (
            results.choose
            .map(F(self._add_link, results.query))
            .replace(True)
            .get_or_else(F(self._no_result, results))
        )

    def _add_link(self, query: SearchQuery, result: SearchResult):
        self.log.info('Added torrent to release {}: {} ({} seeders)'
                      .format(query.release, result.title, result.seeders))
        self._releases.add_torrent_by_id(query.monitor.id, result.magnet_link)
        self._update(query.monitor, last_torrent_update_stamp=now_unix())

    def _no_result(self, results):
        self.log.debug('None of the results match the release.')
        self.log.debug('min_seeders: {}'.format(self._min_seeders))
        self.log.debug('Search string: {}'.format(results.query.search_string))
        self.log.debug('\n'.join([r.title for r in results.results]))

    @property
    def _conditions(self):
        return (
            ~R('downloaded') & ~R('has_cachable_torrents') &
            LambdaCondition('recheck interval',
                            __.can_recheck(self._torrent_recheck_interval))
        )

    @property
    def _candidates(self):
        return self._no_cached_torrents

    def activate_id(self, id):
        super().activate_id(id)
        self._releases.update_by_id(id, last_torrent_search_stamp=0)

__all__ = ['TorrentFinder']
