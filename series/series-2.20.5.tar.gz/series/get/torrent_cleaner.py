from datetime import datetime, timedelta

from series.get import ReleaseMonitor, ReleaseHandler
from series.get.search import TorrentSearch
from series.get.model.link import Torrent
from series.handler import Job

from golgi import configurable

from tek_utils.sharehoster.errors import ShareHosterError

from amino import _, List


class Downgrade(Job):
    pass


class CheckCaching(Job):
    pass


@configurable(torrent=['search_engine'], get=['min_seeders'])
class TorrentCleaner(ReleaseHandler):

    def __init__(self, releases, *a, **kw):
        super().__init__(releases, 600, 'torrent cleaner', **kw)
        self._search = TorrentSearch(self._search_engine, self._min_seeders)

    @property
    def _candidates(self):
        down = (
            self._no_cached_torrents_q
            .filter(ReleaseMonitor.downgrade_after > 0)
            .all()
        )
        caching = (
            self._no_cached_torrents_q
            .join(Torrent)
            .filter(Torrent.caching)
            .all()
        )
        return ((List.wrap(down) / Downgrade) +
                (List.wrap(caching) / CheckCaching))

    def _qualify_job(self, job):
        item = job.item
        if isinstance(job, Downgrade):
            intval = timedelta(hours=item.downgrade_after)
            return (
                '' not in item.resolutions and
                not self._alternative_hd_releases(item) and
                (item.last_torrent_update < datetime.now() - intval)
            )
        elif isinstance(job, CheckCaching):
            return True

    def _handle_job(self, job):
        monitor = job.item
        if isinstance(job, Downgrade):
            return self._downgrade(monitor)
        elif isinstance(job, CheckCaching):
            return self._check_caching(monitor)

    def _downgrade(self, monitor):
        self.log.info('Downgrading resolution of {}'.format(monitor.release))
        self._update(
            monitor,
            _resolutions=','.join(monitor.resolutions.cat('')),
        )
        self._releases.reset_torrent(monitor.id)

    def _alternative_hd_releases(self, monitor):
        return self._search.search(monitor).exists(_.choose.is_just)

    def _check_caching(self, monitor):
        self._check_pending(monitor)

    def _check_pending(self, monitor):
        msg = 'Checking status of caching torrents for {}'
        self.log.debug(msg.format(monitor.release))
        for link in monitor.torrent_links:
            torrent = link.torrent
            try:
                if not link.cached and torrent.cached:
                    self._releases.torrent_cached(link.id)
                    msg = 'Flagging torrent as cached: {}'
                    self.log.info(msg.format(monitor.release))
                elif not link.dead and not link.cached and not torrent.caching:
                    self._releases.update_link(link.id, caching=False)
                    msg = 'Torrent was canceled remotely: {}'
                    self.log.warning(msg.format(link))
            except ShareHosterError as e:
                msg = 'Error checking torrent status for {}: {}'
                self.log.error(msg.format(monitor.release, e))

__all__ = ('TorrentCleaner',)
