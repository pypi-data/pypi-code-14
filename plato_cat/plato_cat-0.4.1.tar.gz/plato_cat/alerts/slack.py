import os
import requests
import json

from oslo_config import cfg
CONF = cfg.CONF

Incoming = os.getenv('PLATO_CAT_SLACK_HOOK')


class SlackAlert(object):

    def call(self, exceptions):
        if not Incoming:
            return

        endpoint = CONF.endpoint
        access_key = CONF.key

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
        if not Incoming:
            return

        url = Incoming

        payload = [title, 'Pass: %s' % is_pass]
        payload += ['%s: %s' % (k, v) for k, v in stat.items()]
        payload = '\n'.join(payload)
        requests.post(url, data=payload)
