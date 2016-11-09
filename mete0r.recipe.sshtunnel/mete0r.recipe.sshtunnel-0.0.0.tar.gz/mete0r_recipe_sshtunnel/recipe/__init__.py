# -*- coding: utf-8 -*-
#
#   mete0r.recipe.sshtunnel: a zc.buildout recipe to make on-demand ssh tunnel
#   Copyright (C) 2015-2016 mete0r <mete0r@sarangbang.or.kr>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import
from distutils.util import strtobool
from textwrap import dedent
import logging
import os.path


def recipe(worker_fn):

    def __init__(self, buildout, name, options):
        self.gen = worker_fn(buildout, name, options)
        next(self.gen)

    def make_method(method):
        def method_fn(self):
            try:
                first = self.gen.send(method)
            except StopIteration:
                return
            else:
                yield first
            for item in self.gen:
                yield item
        method_fn.__name__ = method
        return method_fn

    return type(worker_fn.__name__, (), {
        '__init__': __init__,
        'install': make_method('install'),
        'update': make_method('update'),
    })


def bool2str(b):
    return str(b).lower()


def str2bool(s):
    s = s.strip()
    s = s.lower()
    return strtobool(s)


@recipe
def default(buildout, name, options):
    logger = logging.getLogger(name)
    deployment_name = options['deployment']
    deployment = buildout[deployment_name]
    deployment_etc_user = deployment['etc-user']
    deployment_etc_prefix = deployment['etc-prefix']
    deployment_run_dir = deployment['run-directory']
    deployment_user = deployment['user']

    systemctl = '/bin/systemctl'
    if deployment_etc_user != 'root':
        systemctl += ' --user'
        systemd_prefix = '~%s/.config/systemd' % deployment_etc_user
        systemd_prefix = os.path.expanduser(systemd_prefix)
        systemd_confdir = os.path.join(systemd_prefix, 'user')
    else:
        systemctl = '/bin/systemctl'
        # NOTE: install in the deployment etc directory: you should symlink
        # unit files into /etc/systemd manually
        systemd_prefix = os.path.join(deployment_etc_prefix, 'systemd')
        systemd_confdir = os.path.join(systemd_prefix, 'system')
    options['systemctl'] = systemctl
    options['systemd.prefix'] = systemd_prefix
    directory = systemd_confdir

    socket_name = options.get('socket.name', name + '.sock')
    socket_mode = options.setdefault('socket.mode', '0600')
    socket_path = os.path.join(deployment_run_dir, socket_name)
    socket_path = options.setdefault('socket.path', socket_path)
    socket_user = deployment_user
    ssh_host = options['ssh.hostname']
    ssh_process_user = options.setdefault('ssh.process.user', deployment_user)
    remote_bind = options['remote.bind']
    try:
        remote_host, remote_port = remote_bind.split(':')
    except ValueError:
        remote_path = remote_bind
        nc_args = '-U {}'  # unix domain socket
        nc_args = nc_args.format(remote_path)
    else:
        nc_args = '{} {}'  # address, port
        nc_args = nc_args.format(remote_host, remote_port)

    section = '''
    [{name}.socket]
    recipe = zc.recipe.deployment:configuration
    deployment = {deployment}
    directory = {directory}
    on-change =
        {systemctl} daemon-reload
    text =
        [Socket]
        ListenStream={socket_path}
        SocketMode={socket_mode}
        SocketUser={socket_user}
        Accept=true

        [Install]
        WantedBy=sockets.target
    '''
    section = dedent(section)
    section = section.format(**{
        'name': name,
        'deployment': deployment_name,
        'directory': directory,
        'socket_path': socket_path,
        'socket_mode': socket_mode,
        'socket_user': socket_user,
        'systemctl': systemctl,
    })
    buildout.parse(section)

    section = '''
    [{name}@.service]
    recipe = zc.recipe.deployment:configuration
    deployment = {deployment}
    directory = {directory}
    on-change =
        {systemctl} daemon-reload
    text =
        [Service]
        User={ssh_process_user}
        ExecStart={ssh} -T -S none {ssh_host} '{nc} {nc_args}'
        StandardInput=socket
    '''
    section = dedent(section)
    section = section.format(**{
        'name': name,
        'deployment': deployment_name,
        'directory': directory,
        'ssh': '/usr/bin/ssh',
        'ssh_process_user': ssh_process_user,
        'ssh_host': ssh_host,
        'nc': '/usr/bin/nc',
        'nc_args': nc_args,
        'systemctl': systemctl,
    })
    buildout.parse(section)

    # configuration successful

    yield

    # install/update

    logger.info(
        'On-demand ssh tunnel socket\n'
        '\tpath: %s\n'
        '\tmode: %s\n'
        '\tuser: %s\n'
        '\tssh process user: %s\n'
        '\tremote host: %s\n'
        '\tremote bind: %s',
        socket_path,
        socket_mode,
        socket_user,
        ssh_process_user,
        ssh_host,
        remote_bind,
    )


def default_uninstall(name, options):
    logger = logging.getLogger(name)
    socket_path = options['socket.path']
    if os.path.exists(socket_path):
        try:
            os.unlink(socket_path)
        except OSError as e:
            logger.exception(e)
