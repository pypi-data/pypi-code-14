import requests
import json

Incoming = 'https://hooks.slack.com/services/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'  # noqa


class SlackAlert(object):

    def call(self, exceptions):
        for exception in exceptions:
            url = Incoming
            payload = json.dumps({
                'text': '%s\n%s' % (exception['case'], exception),
            })
            requests.post(url, payload)
