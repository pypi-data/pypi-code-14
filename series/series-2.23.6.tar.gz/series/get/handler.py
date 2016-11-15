from series.condition import AttrCondition
from series.handler import Handler
from series.get.model.release import ReleaseMonitor
from series.get.model.link import Link, Torrent
from series.get.model.show import Show

from sqlalchemy.sql.expression import and_


class ReleaseAttr(AttrCondition[ReleaseMonitor]):

    def __init__(self, attr: str, target=True) -> None:
        super().__init__('release', attr, target=target)

R = ReleaseAttr


class LinkAttr(AttrCondition[Link]):

    def __init__(self, attr: str, target=True) -> None:
        super().__init__('link', attr, target)


L = LinkAttr


class ShowAttr(AttrCondition[Show]):

    def __init__(self, attr: str, target=True) -> None:
        super().__init__('show', attr, target)


S = ShowAttr


class BaseHandler(Handler):

    def __init__(self, data, interval, description, **kw):
        self._data = data
        super().__init__(interval, description, **kw)

    @property
    def _candidates(self):
        return self._data.all

    @property
    def _lock(self):
        return self._data.lock

    def _update(self, item, **data):
        self._update_id(item.id, **data)

    def _update_id(self, id, **data):
        self._data.update_by_id(id, **data)


class ReleaseHandler(BaseHandler):

    @property
    def _releases(self):
        return self._data

    @property
    def _no_cached_torrents_q(self):
        return (
            self._releases.monitors
            .filter_by(downloaded=False, downloading=False)
            .filter(~ReleaseMonitor.torrents.any(
                and_(Torrent.cached, ~Torrent.dead)))
        )

    @property
    def _no_cached_torrents(self):
        return self._no_cached_torrents_q.all()


class ShowHandler(BaseHandler):

    @property
    def _shows(self):
        return self._data

__all__ = ['ReleaseHandler', 'ShowHandler']
