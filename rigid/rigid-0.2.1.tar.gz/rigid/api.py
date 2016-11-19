import os
import sys
import platform

try:
    import urlparse
except ImportError:
    # Python 3
    from urllib import parse as urlparse

import requests
import click

from rigid import __version__

DEFAULT_API_BASE = 'https://api.rigidapp.com'


class Client(object):
    def __init__(self, base=None):
        python_version = '{}.{}.{}'.format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
        self.base = base or os.environ.get('RIGID_API', DEFAULT_API_BASE)
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Rigid/{} Python/{} {}/{}'.format(__version__, python_version, platform.system(), platform.release())})

        token = None

        path = os.path.expanduser('~/.rigid/credentials')
        if os.path.exists(path):
            with open(path) as fp:
                token = fp.read().strip()

        if 'RIGID_TOKEN' in os.environ:
            token = os.environ['RIGID_TOKEN']

        if token:
            self.session.headers.update({'Authorization': 'Bearer {}'.format(token)})

    @property
    def host(self):
        return urlparse.urlparse(self.base).hostname

    def url(self, *components):
        return '/'.join([self.base] + list(components))

    def validate(self, response):
        if response.status_code == 401:
            exception = click.ClickException('You are not logged in. Use `rigid login` to get started.')
            exception.response = response
            raise exception

        if 400 <= response.status_code < 600:
            try:
                payload = response.json()
            except:
                payload = None

            if isinstance(payload, list):
                exception = click.ClickException('\n'.join(payload))
                exception.response = response
                raise exception

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

    def token(self, auth=None, scopes=None):
        payload = {}
        if scopes:
            payload['scopes'] = scopes

        response = self.session.post(self.url('authorizations'), json=payload, auth=auth)
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

    def delete_app(self, name):
        response = self.session.delete(self.url('apps', name))
        self.validate(response)

    def update_app(self, name, payload):
        response = self.session.patch(self.url('apps', name), json=payload)
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

    def add_domain(self, app, alias, domain):
        response = self.session.post(self.url('apps', app, 'aliases', alias, 'domains'), json={'domain': domain})
        self.validate(response)
        return response.json()

    def remove_domain(self, app, alias, domain):
        response = self.session.delete(self.url('apps', app, 'aliases', alias, 'domains', domain))
        self.validate(response)

    # Organisations

    def orgs(self):
        response = self.session.get(self.url('organisations'))
        self.validate(response)
        return response.json()

    def org(self, name):
        response = self.session.get(self.url('organisations', name))
        self.validate(response)
        return response.json()

    def create_organisation(self, name):
        response = self.session.post(self.url('organisations'), json=dict(name=name))
        self.validate(response)
        return response.json()

    def update_organisation(self, name, payload):
        response = self.session.patch(self.url('organisations', name), json=payload)
        self.validate(response)
        return response.json()

    def delete_organisation(self, name):
        response = self.session.delete(self.url('organisations', name))
        self.validate(response)
