"""
A plugin for tox that reports each environment status to bitbucket.
"""
import os
import logging

from tox import hookimpl

import requests

LOGGER = logging.getLogger(__name__)

STATE_MAP = {
    'started': 'INPROGRESS',

    0: 'SUCCESSFUL',
    'commands succeeded': 'SUCCESSFUL',
    'ignored failed command': 'SUCCESSFUL',
    'platform mismatch': 'SUCCESSFUL',

    'skipped tests': 'FAILED',
    'commands failed': 'FAILED',
}

API_URL = 'https://api.bitbucket.org/2.0/repositories/'\
          '{BB_REPO_OWNER}/{BB_REPO_SLUG}/commit/{CI_COMMIT_ID}/statuses/build'


def get_data():
    "Build up the data from the environment"
    result = dict(os.environ)
    # If we have an environment variable called 'JENKINS_URL', then we assume we are
    # running under jenkins.
    if result.get('JENKINS_URL', None) is not None:
        result.setdefault('CI_NAME', 'Jenkins')
        result.setdefault('CI', True)
        result.setdefault('CI_BUILD_URL', result.get('BUILD_URL'))

    # If we are running under Jenkins/mercurial, then we want to grab as much data as possible
    # from the repository itself.
    if 'MERCURIAL_REPOSITORY_URL' in result:
        server, repo_owner, repo_slug = result['MERCURIAL_REPOSITORY_URL'].rsplit('/', 2)
        if server == 'ssh://hg@bitbucket.org':
            result.setdefault('BB_REPO_OWNER', repo_owner)
            result.setdefault('BB_REPO_SLUG', repo_slug)
    # We could also get this data directly from hg, if we have an hg repo in our current directory.

    if 'MERCURIAL_REVISION' in result:
        result.setdefault('CI_COMMIT_ID', result['MERCURIAL_REVISION'])

    result.setdefault('BB_USERNAME', result.get('BB_REPO_OWNER'))

    result.setdefault('CI', False)

    return result


def send(state, venvname, environ):
    "Actually send the data to bitbucket, if we are in a CI environment"
    if environ['CI']:
        data = {
            'state': state,
            'key': '{1}-{0}'.format(venvname, environ['CI_NAME'].lower()),
            'name': '{CI_NAME}: {0}'.format(venvname, **environ),
            'url': environ['CI_BUILD_URL']
        }

        if 'BB_PASSWORD' not in environ:
            return

        auth = (environ['BB_USERNAME'], environ['BB_PASSWORD'])
        response = requests.post(API_URL.format(**environ), auth=auth, json=data)
        if response.status_code >= 400:
            LOGGER.warn('Warning! Unable to send data to bitbucket.')
            LOGGER.warn(response.content)


@hookimpl
def tox_runtest_pre(venv):
    "Send notification that this env has started testing."
    send('INPROGRESS', venv.envconfig.envname, get_data())


@hookimpl
def tox_runtest_post(venv):
    "Send notification that this env has finished testing."
    send(STATE_MAP.get(venv.status, 'FAILED'), venv.envconfig.envname, get_data())
