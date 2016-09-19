#!/usr/bin/env python2.7

from nagios import BaseCheckCommand

try:
    from requests import HTTPError
    requests_installed = True
except ImportError:
    requests_installed = False

try:
    from sumologic import SumoLogic
    sumo_installed = True
except ImportError:
    sumo_installed = False

from optparse import OptionParser
import time
import datetime

class CollectorLastMessageCheckCommand(BaseCheckCommand):
    def __init__(self, **kwargs):
        # Exit early if prereqs are not installed
        self.prerequites_test()

        # Invoke parent class's constructor
        self.__class__.__bases__[0].__init__(self,\
                parser=OptionParser(usage='%prog [options] COLLECTOR_NAME', version="%prog 1.0"))

        # Constructor for CollectorLastMessage
        self.add_options()
        params      = kwargs
        opts, args  = self.parse_args()

        self.access_id      = params.get('access_id') or opts.access_id
        self.secret_key     = params.get('secret_key') or opts.secret_key
        self.collector_name = params.get('collector_name') or args[0]

        self.warning        = int(opts.warning)
        self.critical       = int(opts.critical)

        # Instantiating the session will not raise if there are invalid credentials
        self.session        = SumoLogic(self.access_id, self.secret_key)

    def add_options(self):
        self.parser.add_option('-a', '--access-id',
                                dest='access_id',
                                action='store',
                                help='Sets the SumoLogic API access ID to use for queries.',
                                metavar='ACCESS_ID')
        self.parser.add_option('-s', '--secret-key',
                                dest='secret_key',
                                action='store',
                                help='sets the SumoLogic API secret key to use for queries.',
                                metavar='SECRET_KEY')

    def prerequites_test(self):
        if not requests_installed:
            self.usage(3,
                        msg='Unable to import requests. Ensure the "requests" package is installed. To install: `pip install requests`')

        if not sumo_installed:
            self.usage(3, 
                        msg='Unable to import sumologic-sdk. Ensure the "sumologic-sdk" package is installed. To install: `pip install sumologic-sdk`')

    def check(self):
        try:
            if not self.collector_alive():
                self.status = "CRITICAL: %s is not alive" % self.collector_name
                self.perf_data = "alive=0;1;1;;"
                self.exit(exit_code=2)
                return None

            time_now = int(time.time())
            time_diff = time_now - self.last_message_time()
        except HTTPError as e:
            self.status = "API Error: %s" % e.message
            self.exit(exit_code=3)
        except AssertionError as e:
            self.status = "Check Error: %s" % e.message
            self.exit(exit_code=3)

        if time_diff >= self.critical:
            self.status = "CRITICAL: %s last logged %s seconds ago" % (self.collector_name, time_diff)
            self.perf_data = "last_message=%ss;%s;%s;; alive=1;1;1;;" % (time_diff, self.warning, self.critical)
            self.exit(exit_code=2)
        elif time_diff >= self.warning:
            self.status = "WARNING: %s last logged %s seconds ago" % (self.collector_name, time_diff)
            self.perf_data = "last_message=%ss;%s;%s;; alive=1;1;1;;" % (time_diff, self.warning, self.critical)
            self.exit(exit_code=1)
        else:
            self.status = "OK: %s last logged %s seconds ago" % (self.collector_name, time_diff)
            self.perf_data = "last_message=%ss;%s;%s;; alive=1;1;1;;" % (time_diff, self.warning, self.critical)
            self.exit(exit_code=0)

        return None

    def collector_alive(self):
        collectors = self.session.collectors()
        assert len(collectors) > 0, "No collectors"
        for collector in collectors:
            if 'name' in collector and collector['name'] == self.collector_name:
                return collector.get('alive')
        return False

    def last_message_time(self):
        time_now = datetime.datetime.now()
        time_now_iso = time_now.isoformat().split('.')[0]
        time_twelve_hours_ago = (time_now - datetime.timedelta(hours=12)).isoformat().split('.')[0]

        search_res = self.session.search('_collector=%s | limit 1' % self.collector_name, fromTime=time_twelve_hours_ago, toTime=time_now_iso, timeZone='PST')

        assert len(search_res) > 0, "No messages"
        last_message = search_res[0]
        assert type(last_message) == dict, "Unreadable search result"
        return int(last_message.get('_messagetime')) / 1000
