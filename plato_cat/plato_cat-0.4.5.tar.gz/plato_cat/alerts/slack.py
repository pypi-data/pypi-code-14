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

        url = Incoming

        endpoint = CONF.endpoint
        access_key = CONF.key

        for ex in exceptions:
            text = ['endpoint: %s\naccess key: %s' % (endpoint, access_key)]
            text += ['case: %s' % ex['case']]
            text += ['exception: %s' % ex['message']]
            text += ['traceback: %s' % ex['traceback']]
            text = '\n'.join(text)
            payload = json.dumps({'text': text})

            try:
                requests.post(url, payload)
            except:
                pass

    def report(self, title, is_pass, stat):
        if not Incoming:
            return

        url = Incoming

        endpoint = CONF.endpoint
        access_key = CONF.key

        text = ['endpoint: %s\naccess key: %s' % (endpoint, access_key)]
        text += [title]
        text += ['Pass: %s' % is_pass]
        text += ['%s: %s' % (k, v) for k, v in stat.items()]
        text = '\n'.join(text)
        payload = json.dumps({'text': text})

        try:
            requests.post(url, payload)
        except:
            pass
