import os
import sys
import platform
import urlparse
import requests
import click

from rigid import __version__

DEFAULT_API_BASE = 'https://rigid-api.herokuapp.com'


class Client(object):
    def __init__(self, base=None):
        python_version = '{}.{}.{}'.format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
        self.base = base or os.environ.get('RIGID_API', DEFAULT_API_BASE)
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Rigid/{} Python/{} {}/{}'.format(__version__, python_version, platform.system(), platform.release())})

        path = os.path.expanduser('~/.rigid/credentials')
        if os.path.exists(path):
            with open(path) as fp:
                token = fp.read().strip()

            self.session.headers.update({'Authorization': 'Bearer {}'.format(token)})

    @property
    def host(self):
        return urlparse.urlparse(self.base).hostname

    def url(self, *components):
        return '/'.join([self.base] + list(components))

    def validate(self, response):
        if 400 <= response.status_code < 600:
            try:
                payload = response.json()
            except:
                payload = None

            if payload and 'detail' in payload:
                exception = click.ClickException(payload['detail'])
                exception.response = response
                raise exception

            if payload and len(payload):
                payload = map(lambda item: [item[0], ', '.join(item[1])], payload.items())
                reasons = map('{0[0]}: {0[1]}'.format, payload)
                exception = click.ClickException('\n'.join(reasons))
                exception.response = response
                raise exception

        response.raise_for_status()

    def user(self):
        response = self.session.get(self.url('user'))
        self.validate(response)
        return response.json()

    def token(self, auth=None):
        response = self.session.post(self.url('authorizations'), auth=auth)
        self.validate(response)
        return response.json()['token']

    # Applications

    def apps(self):
        response = self.session.get(self.url('apps'))
        self.validate(response)
        return response.json()

    def app(self, name):
        response = self.session.get(self.url('apps', name))
        self.validate(response)
        return response.json()

    def create_app(self, name=None):
        payload = None
        if name:
            payload = {'name': name}

        response = self.session.post(self.url('apps'), json=payload)
        self.validate(response)
        return response.json()

    def promote(self, app, alias, version, config=None):
        payload = {
            'version': version,
        }

        if config:
            payload['config'] = config

        response = self.session.put(self.url('apps', app, 'aliases', alias), json=payload)
        self.validate(response)
        return response.json()
