# -*- coding: utf-8 -*-
from collections import OrderedDict
import difflib
import unittest

try:
    # py3
    from urllib.parse import urlparse, parse_qs, urljoin, urlunparse, urlencode
except ImportError:
    from urlparse import urljoin, urlparse, parse_qs, urlunparse
    from urllib import urlencode

from pypiwik.tracker import TrackingCodeBuilder, PiwikTracker
import re

img_src_re = re.compile('img src="(.*?)"', re.IGNORECASE)

class TrackingCodeBuilderTest(unittest.TestCase):

    def assertTrackingCodeEquals(self, first, second):

        def _clean(s):
            m = img_src_re.search(s)
            assert m and len(m.groups()) == 1, "String does not have an image tracker code"

            url = m.group(1)
            urlparts = urlparse(url)
            query = parse_qs(urlparts.query)
            d = OrderedDict(sorted(((k, v[0]) for k, v in query.items()), key=lambda x: x[0]))
            new_url = urlunparse((urlparts.scheme, urlparts.netloc, urlparts.path, urlparts.params, urlencode(d), urlparts.fragment))

            s2 = img_src_re.sub(new_url, s)
            return [x.strip(' ') for x in s2.splitlines(True) if x.strip(' ') if x.strip(' ') != '\n']

        t1_lines = _clean(first)
        t2_lines = _clean(second)

        assert difflib.SequenceMatcher(None, t1_lines, t2_lines).ratio() == 1.0, \
                "Tracking codes do not match: %s" % ''.join(difflib.ndiff(t1_lines, t2_lines))

    def assertImageTrackingVars(self, tracking_code, expected_vars):
        m = img_src_re.search(tracking_code)
        assert m and len(m.groups()) == 1, "String does not have an image tracker code"

        url = m.group(1)
        urlparts = urlparse(url)
        query = parse_qs(urlparts.query)

        for k, v in expected_vars.items():
            assert k in query, "Image tracker query string does not contain '%s'" % k
            assert query[k] == [v], \
                "Image tracker variable %s does not match expected value '%s'. It's '%s'" % (k, v, query[k])


    def test_simple_tracking_code(self):
        tracker = PiwikTracker('http://localhost', 1)
        builder = TrackingCodeBuilder(tracker)

        s = builder.render(tracker._build_parameters())

        self.assertTrackingCodeEquals(s, """<script type="text/javascript">
var _paq = _paq || [];
_paq.push(['trackPageView']);
_paq.push(['enableLinkTracking']);
(function() {
 _paq.push(['setTrackerUrl', 'http://localhost/piwik.php']);
 _paq.push(['setSiteId', 1]);
 var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
 g.type='text/javascript'; g.async=true; g.defer=true; g.src='http://localhost/piwik.js'; s.parentNode.insertBefore(g,s);
})();
</script>
<noscript><p><img src="http://localhost/piwik.php?idsite=1&rec=1&apiv=1" style="border:0;" alt="" /></p></noscript>""")

    def test_event_tracking_code(self):
        tracker = PiwikTracker('http://localhost', 1)
        tracker.event_category = "event_category"
        tracker.event_action = "event_action"
        builder = TrackingCodeBuilder(tracker)

        s = builder.render(tracker._build_parameters())

        self.assertTrackingCodeEquals(s, """<script type="text/javascript">
var _paq = _paq || [];
_paq.push(["trackEvent", "event_category", "event_action"]);
_paq.push(['trackPageView']);
_paq.push(['enableLinkTracking']);
(function() {
 _paq.push(['setTrackerUrl', 'http://localhost/piwik.php']);
 _paq.push(['setSiteId', 1]);
 var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
 g.type='text/javascript'; g.async=true; g.defer=true; g.src='http://localhost/piwik.js'; s.parentNode.insertBefore(g,s);
})();
</script>
<noscript><p><img src="http://localhost/piwik.php?idsite=1&rec=1&apiv=1&e_a=event_action&e_c=event_category" style="border:0;" alt="" /></p></noscript>""")

    def test_method_call_generation(self):
        # test new_visit=True
        tracker = PiwikTracker('http://localhost', 1)
        tracker.new_visit = True
        builder = TrackingCodeBuilder(tracker)

        s = builder.render(tracker._build_parameters())

        assert '_paq.push(["deleteCookies"]);' in s
        assert '_paq.push(["appendToTrackingUrl", "new_visit=1"]);' in s
        self.assertImageTrackingVars(s, {
            'new_visit': '1'
        })

        # test track_bots=True
        tracker = PiwikTracker('http://localhost', 1)
        tracker.track_bots = True
        builder = TrackingCodeBuilder(tracker)

        s = builder.render(tracker._build_parameters())

        assert '_paq.push(["appendToTrackingUrl", "bots=1"]);' in s
        self.assertImageTrackingVars(s, {
            'bots': '1'
        })

        # test action_name
        tracker = PiwikTracker('http://localhost', 1)
        tracker.action_name = "Foo / Bar"
        builder = TrackingCodeBuilder(tracker)
        s = builder.render(tracker._build_parameters())

        assert '_paq.push(["setDocumentTitle", "Foo / Bar"]);' in s
        self.assertImageTrackingVars(s, {
            'action_name': 'Foo / Bar'
        })

        # test action_name
        tracker = PiwikTracker('http://localhost', 1)
        tracker.referer = 'http://foobar.local'
        builder = TrackingCodeBuilder(tracker)
        s = builder.render(tracker._build_parameters())

        assert '_paq.push(["setReferrerUrl", "http://foobar.local"]);' in s
        self.assertImageTrackingVars(s, {
            'urlref': 'http://foobar.local'
        })

    def test_heartbeat_timer(self):
        tracker = PiwikTracker('http://localhost', 1)
        tracker.heartbeat_timer = None
        builder = TrackingCodeBuilder(tracker)
        s = builder.render(tracker._build_parameters())
        assert 'enableHeartBeatTimer' not in s, "Heartbeat timer enabled but set to None"

        tracker = PiwikTracker('http://localhost', 1)
        tracker.heartbeat_timer = 0
        builder = TrackingCodeBuilder(tracker)
        s = builder.render(tracker._build_parameters())
        assert 'enableHeartBeatTimer' not in s, "Heartbeat timer enabled but set to 0"

        tracker = PiwikTracker('http://localhost', 1)
        tracker.heartbeat_timer = 10
        builder = TrackingCodeBuilder(tracker)
        s = builder.render(tracker._build_parameters())
        assert '_paq.push(["enableHeartBeatTimer", 10]);' in s, "heartbeat_timer set but not enabled in tracking code"