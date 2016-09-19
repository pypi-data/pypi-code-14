# vi:et:ts=4 sw=4 sts=4
#
# local-pipelines : run Bitbucket pipelines locally
# Copyright (C) 2016  Gary Kramlich <grim@reaperworld.com>
# Copyright (C) 2016  Sean Farley <sean@farley.io>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA

import os
import subprocess


def run_command(cmd, path):
    env = os.environ.copy()

    # ignore user's config
    env['HGRCPATH'] = '/dev/null'
    env['HOME'] = '/tmp'
    env['GIT_CONFIG_NOSYSTEM'] = '1'

    try:
        return subprocess.check_output(cmd.split(),
                                       env=env,
                                       stderr=open(os.devnull, 'w'),
                                       cwd=path).strip().decode('utf-8')
    except subprocess.CalledProcessError:
        return ''


class git_backend(object):
    def __init__(self, path):
        self._path = path

    @property
    def branch(self):
        return run_command('git rev-parse --abbrev-ref HEAD',
                           self._path)

    @property
    def node(self):
        return run_command('git rev-parse HEAD',
                           self._path)

    @property
    def _owner_repo(self):
        url = run_command('git remote get-url origin', self._path)
        if url.endswith('.git'):
            url = url[:-4]
        return url.replace(':', '/').split('/')[-2:]

    @property
    def owner(self):
        return self._owner_repo[0]

    @property
    def slug(self):
        return '/'.join(self._owner_repo)


class hg_backend(object):
    def __init__(self, path):
        self._path = path

    @property
    def branch(self):
        return run_command('hg log -r . -T {branch}',
                           self._path)

    @property
    def node(self):
        return run_command('hg log -r . -T {node}',
                           self._path)

    @property
    def _owner_repo(self):
        return run_command('hg paths default',
                           self._path).split('/')[-2:]

    @property
    def owner(self):
        return self._owner_repo[0]

    @property
    def slug(self):
        return '/'.join(self._owner_repo)


class repo(object):
    def __init__(self, search_path):
        self._repo = None

        # search for .git or .hg to determine our backend class
        prev_dir = None
        next_dir = os.path.realpath(search_path)
        while prev_dir != next_dir:
            if os.path.exists(os.path.join(next_dir, '.git')):
                self._repo = git_backend(next_dir)
                break
            elif os.path.exists(os.path.join(next_dir, '.hg')):
                self._repo = hg_backend(next_dir)
                break
            prev_dir = next_dir
            next_dir = os.path.dirname(prev_dir)

        # sanity check
        if self._repo is None:
            raise IOError("Could not find .git nor .hg")

    @property
    def branch(self):
        return self._repo.branch

    @property
    def node(self):
        return self._repo.node

    @property
    def owner(self):
        return self._repo.owner

    @property
    def slug(self):
        return self._repo.slug
