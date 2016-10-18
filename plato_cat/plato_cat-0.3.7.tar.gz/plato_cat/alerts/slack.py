import requests
import json
import sys
import urllib

Incoming = 'https://hooks.slack.com/services/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'  # noqa


class SlackAlert(object):

    def call(self, exceptions):
        endpoint = sys.argv[1]
        access_key = sys.argv[2]
        for exception in exceptions:
            url = Incoming
            payload = json.dumps({
                'text': 'endpoint: %s\naccess key: %s\n'
                'case: %s\nexception: %s\ntraceback: %s'
                % (endpoint, access_key, exception['case'],
                   exception['message'], exception['traceback']),
            })
            requests.post(url, payload)

    def report(self, title, is_pass, stat):
        url = Incoming

        payload = [title, 'Pass: %s' % is_pass]
        payload += ['%s: %s' % (k, v) for k, v in stat.items()]
        payload = '\n'.join(payload)
        requests.post(url, data=payload)
