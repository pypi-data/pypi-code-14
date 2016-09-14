
"""
Methods for accessing the HuffPost Pollster API. Documentation for this API
may be found at http://elections.huffingtonpost.com/pollster/api.
"""
try:
    from urllib.parse import urlencode
    from urllib.request import urlopen
    from urllib.error import HTTPError

    def get_items(x):
        return x.items()
except ImportError:
    from urllib2 import urlopen
    from urllib2 import HTTPError
    from urllib import urlencode

    def get_items(x):
        return x.viewitems()


try:
    import json
except ImportError:
    import simplejson as json


class PollsterException(Exception):
    """General exception raised by the Pollster API."""
    pass


class Pollster(object):
    """Base object for accessing the Pollster API."""

    API_SERVER = 'elections.huffingtonpost.com'
    API_BASE = '/pollster/api'

    def _build_request_url(self, path, params=None):
        if params is None:
            params = {}
        url = "http://%s%s/%s" % (self.API_SERVER, self.API_BASE, path)
        if params:
            url += "?%s" % urlencode(params)
        return url

    def _invoke(self, path, params=None):
        if params is None:
            params = {}
        url = self._build_request_url(path, params)
        try:
            response = urlopen(url)
        except HTTPError as url_exc:
            res = url_exc.read().decode('utf-8')
            msg = "An error occurred. URL: %s Reason: %s %s" % (url,
                                                                url_exc.code,
                                                                url_exc.reason)
            try:
                r_msg = dict(json.loads(res))
                if 'errors' in r_msg:
                    msg += " [%s]" % r_msg['errors'][0]
            except ValueError:
                pass
            raise PollsterException(msg)

        if response.msg == 'OK':
            return json.loads(response.read().decode('utf-8'))

        raise PollsterException('Invalid response returned: %s', response.msg)

    def charts(self, **kwargs):
        """Return a list of charts matching the specified parameters."""
        return [Chart(result) for result in self._invoke('charts', kwargs)]

    def chart(self, slug, **kwargs):
        """Return a specific chart matching the slug, optionally specifying
        parameters."""
        result = self._invoke('charts/%s' % slug, kwargs)
        return Chart(result)

    def polls(self, **kwargs):
        """Return a list of polls matching the specified parameters."""
        return [Poll(result) for result in self._invoke('polls', kwargs)]


class Chart(object):
    """Represents a chart of estimates on a specific topic (e.g.
    `obama-job-approval` or `2016-president`). Don't construct this directly;
    instead, call Pollster().chart(slug)."""

    def __init__(self, result):
        valid = ['last_updated',
                 'title',
                 'url',
                 'estimates',
                 'poll_count',
                 'topic',
                 'state',
                 'slug', ]
        for key, val in get_items(result):
            if key in valid:
                setattr(self, key, val)

        if 'estimates_by_date' in result:
            self._estimates_by_date = result['estimates_by_date']

    def polls(self, **kwargs):
        """Returns polls matching specified parameters."""
        kwargs['chart'] = self.slug
        return Pollster().polls(**kwargs)

    def estimates_by_date(self):
        """Returns (if necessary retrieving first) a list of estimates for
        this chart."""
        if hasattr(self, '_estimates_by_date'):
            return self._estimates_by_date
        else:
            try:
                chart = Pollster().chart(slug=self.slug)
                self._estimates_by_date = chart.estimates_by_date()
                return self.estimates_by_date()
            except IndexError:
                raise PollsterException("Can't find chart with slug: %s",
                                        self.slug)

    def __repr__(self):
        return '<Chart: %s>' % self.title


class Poll(object):
    """Represents a single poll. Don't construct this directly;
    instead, call e.g. `Pollster().polls(chart='obama-job-approval')`."""

    def __init__(self, result):
        valid = ['id',
                 'pollster',
                 'start_date',
                 'end_date',
                 'method',
                 'source',
                 'questions',
                 'survey_houses',
                 'sponsors',
                 'partisan',
                 'affiliation']
        for key, val in get_items(result):
            if key in valid:
                setattr(self, key, val)

    def __repr__(self):
        return '<Poll: %s (%s - %s)>' % (self.pollster, self.start_date,
                                         self.end_date)
