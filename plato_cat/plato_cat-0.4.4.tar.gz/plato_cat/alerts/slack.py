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

            try:
                requests.post(url, payload)
            except:
                pass

    def report(self, title, is_pass, stat):
        if not Incoming:
            return

        url = Incoming

        text = [title, 'Pass: %s' % is_pass]
        text += ['%s: %s' % (k, v) for k, v in stat.items()]
        text = '\n'.join(text)
        payload = json.dumps({'text': text})

        try:
            requests.post(url, payload)
        except:
            pass
