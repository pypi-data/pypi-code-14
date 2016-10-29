import re

from golgi.config import configurable

from tek.tools import find
from tek.user_input import SpecifiedChoice
from golgi.io.terminal import terminal as term, ColorString

from amino import Map, List, __, F, Empty, Just

from series.api_client import ApiClient as Base
from series.get import format_explain_release, format_explain_show
from series.get.util.format import format_status_lines
from series.etvdb import ETVDBFacade


def is_error(response):
    return isinstance(response, dict) and 'error' in response


@configurable(get_client=['rest_api_port', 'rest_api_url', 'query_etvdb'])
class ApiClient(Base):
    command = Base.command

    def _find_release_id(self, series, season, episode, url=None):
        if episode is not None:
            data = dict(series=series, season=season, episode=episode)
            _id = self.get('release_id', body=data)
        elif isinstance(series, int) or (isinstance(series, str) and
                                         series.isdigit()):
            _id = int(series)
        elif url is not None:
            dls = self.get('download/pending')
            release = find(lambda r: re.search(r[1], url, re.I), dls)
            _id = release[0] if release else -1
        else:
            _id = -1
        return _id

    def _with_record(self, _id, desc, f):
        if _id != -1:
            response = f(_id)
            if not is_error(response):
                self.log.info(response)
            else:
                _id = -1
                self.log.error('Command failed')
        else:
            self.log.error('No matching {} found'.format(desc))
        return _id

    def _with_release(self, series, season, episode, f, url=None):
        _id = self._find_release_id(series, season, episode, url)
        return self._with_record(_id, 'release', f)

    def _with_show(self, _id, f):
        return self._with_record(_id, 'show', f)

    def _with_release_args(self, f, fr, *args, **kw):
        series, season, episode, rest = self._parse_episode_args(args)
        return self._with_release(series, season, episode, F(f, rest), **kw)

    def _release_put(self, series, season, episode, path=None, url=None,
                     **args):
        sub = '/{}'.format(path) if path else ''
        go = lambda _id: self.put('release/{}{}'.format(_id, sub), **args)
        return self._with_release(series, season, episode, go, url)

    @command('url (id || series season episode)', 'Add the url to the ' +
             'specified release\'s links')
    def add_link(self, url, series=None, season=None, episode=None):
        return self._release_put(series, season, episode, 'link', url=url,
                                 body=dict(url=url))

    @command('count', 'Describe the state of the latest `count` releases,'
             ' default 5')
    def explain_old(self, count=5):
        output = self.get('release/explain_old/{}'.format(count))
        for line in output:
            self.log.info(line)
        return output

    @command('id', 'Set the \'downloaded\' flag for the specified release')
    def mark_downloaded(self, _id):
        return self._downloaded_flag(_id, True)

    @command('id', 'Unset the \'downloaded\' flag for the specified release')
    def mark_not_downloaded(self, _id):
        return self._downloaded_flag(_id, False)

    def _downloaded_flag(self, _id, value):
        success = self.put('release/{}'.format(_id),
                           body=dict(downloaded=value, archived=value))
        if success:
            self.log.info('Success!')
        else:
            self.log.error('Release not found!')
        return bool(success)

    def _resolve_show(self, name):
        e = ETVDBFacade()
        def run(names, ids):
            return (
                Empty()
                if ids.empty else
                ids.head
                if ids.length == 1 else
                self._ask_show(names, ids)
            )
        return e.shows(name).flat_map2(run)

    def _ask_show(self, names, ids):
        choice = SpecifiedChoice(names, text_pre=['Select a show'])
        choice.read()
        return ids.lift(choice.index)

    @command('[regex]', 'Display id, name, season and episode for all ' +
             'releases matching the regex (default all)')
    def list(self, regex=''):
        matches = self.get('release', body=dict(regex=regex))
        if matches:
            text = 'id #{}: {}'
            for id, description in matches:
                self.log.info(text.format(id, description))
        else:
            self.log.info('No matching release found.')
        return matches

    @command('series season episode', 'Create an empty release with the ' +
             'supplied metadata')
    def create_release(self, series, season, episode):
        response = self.post('release/{}/{}/{}'.format(series, season,
                                                       episode))
        self.log.info(response)
        return response

    @command('series season episode', 'Delete the release matching the ' +
             'supplied metadata')
    def delete_release(self, series, season, episode):
        response = self.delete('release/{}/{}/{}'.format(series, season,
                                                         episode))
        self.log.info(response)
        return response

    @command('series season', 'Add the specified season of series to the db')
    def add_season(self, name, season):
        response = self.post('season', body=dict(name=name, season=season))
        self.log.info(response)
        return response

    @command('name [etvdb_id]', 'Add the specified show')
    def add_show(self, name, manual_id=None):
        id = (
            (self._resolve_show(name) if self._query_etvdb else Empty())
            if manual_id is None else Just(manual_id)
        )
        body = Map(name=name).add_maybe('id', id)
        response = self.post('show', body=body)
        self.log.info(response)
        return response

    @command('canonical_name|id', 'Delete the specified show')
    def delete_show(self, name):
        response = self.delete('show', body=dict(name=name))
        self.log.info(response)
        return response

    @command('[regex]', 'List show names matching the regex')
    def list_shows(self, regex=''):
        matches = self.get('show', body=dict(regex=regex))
        if matches:
            text = 'id #{}: {}'
            for id, description in matches:
                self.log.info(text.format(id, description))
        else:
            self.log.info('No matching show found.')
        return matches

    def print_shows(self, shows):
        colors = {
            0: term.blue,
            1: term.green,
            2: term.yellow,
            3: term.red,
        }
        if shows:
            for name, nepi, rel, status in shows:
                term.push([ColorString('>> ', term.red),
                           ColorString(name, term.bold)])
                term.push([ColorString(' | ', term.green), nepi])
                if rel:
                    col = colors.get(status, term.black)
                    term.push([ColorString(' | ', term.green),
                               ColorString(rel, col)])
                self.log.info('')
        else:
            self.log.info('No matching show found.')
        return shows

    @command('[regex]', 'Extended info for shows matching regex')
    def shows(self, regex=''):
        return self.print_shows(self.get('show/info', body=dict(regex=regex)))

    @command('[regex]', 'List upcoming releases for shows matching regex')
    def next(self, regex=''):
        return self.print_shows(self.get('show/next', body=dict(regex=regex)))

    @command('[regex]', 'List current releases for shows matching regex')
    def ready(self, regex=''):
        return self.print_shows(self.get('show/ready', body=dict(regex=regex)))

    @command('[regex]', 'List downloaded releases for shows matching regex')
    def done(self, regex=''):
        return self.print_shows(self.get('show/done', body=dict(regex=regex)))

    @command('id || series season episode', 'Reset a release and mark its ' +
             'torrent as dead, forcing download of a different torrent')
    def reset_torrent(self, series=None, season=None, episode=None):
        return self._release_put(series, season, episode, 'reset_torrent')

    @command('id || series season episode', 'Print release info')
    def show_release(self, series=None, season=None, episode=None):
        go = lambda _id: self.get('release/{}'.format(_id))
        return self._with_release(series, season, episode, go)

    def _parse_episode_args(self, args):
        a = List.wrap(args)
        if a.lift(2).exists(__.isdigit()):
            series, season, episode = a[:3]
            rest = a[3:]
        else:
            series, season, episode = a[0], None, None
            rest = a[1:]
        return series, season, episode, rest

    @command('(id || series season episode) [key=value ...]',
             'Update release data')
    def update_release(self, *args):
        series, season, episode, rest = self._parse_episode_args(args)
        data = Map(rest.map(__.split('=')))
        return self._release_put(series, season, episode, '', body=data)

    @command('(id || name) [key=value ...]',
             'Update show data')
    def update_show(self, id, *rest):
        data = Map(List.wrap(rest).map(__.split('=')))
        response = self.put('show/{}'.format(id), body=data)
        self.log.info(response)
        return response

    @command('id || series season episode', 'Reset cooldown time for release')
    def activate_release(self, *args):
        series, season, episode, _ = self._parse_episode_args(args)
        return self._release_put(series, season, episode, 'activate')

    @command('[id || series season episode] [services]', 'Explain why the ' +
             'csv-specified services treat the release as they do')
    def explain(self, *args):
        def rest(a):
            return a.head.map(lambda b: dict(body=dict(services=b))) | dict()
        def go(r, id):
            resp = self.get('release/{}/explain'.format(id), **rest(r))
            return resp if is_error(resp) else format_explain_release(resp)
        self._with_release_args(go, rest, *args)

    @command('id [services]', 'Explain why the ' +
             'csv-specified services treat the show as they do')
    def explain_show(self, _id, services='all'):
        args = dict(body=dict(services=services))
        def go(id):
            resp = self.get('show/{}/explain'.format(id), **args)
            return resp if is_error(resp) else format_explain_show(resp)
        self._with_show(_id, go)

    @command('(id || series season episode) [YYYY-]MM-DD',
             'set a release\'s airdate')
    def set_airdate(self, *args):
        series, season, episode, rest = self._parse_episode_args(args)
        data = rest.head / (lambda d: dict(date=d)) | dict()
        return self._release_put(series, season, episode, 'airdate', body=data)

    @command('', 'status of recent releases')
    def status(self):
        output = Map(self.get('release/status'))
        info = format_status_lines(output)
        info % self.log.info
        return output

__all__ = ('ApiClient',)
