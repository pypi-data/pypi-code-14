#!/usr/bin/env python
"""PyPi Configuration File Manager."""

import optparse
import os


try:
    import configparser
    from urllib.parse import urlparse, urlunparse

except ImportError:
    import ConfigParser as configparser  # @UnusedImport
    from urlparse import urlparse, urlunparse


class SetPyPi(object):
    """
    PyPi Configuration File Manager.

    Can be used for updating ~/.pypirc file programatically.

    Example::
        >>> a = SetPyPi('doctest_pypi.cfg')
        >>> new_server = {'pypi': {'repository': 'http://pypi.example.com'}}
        >>> new_server2 = {'pypi2': {'repository': 'http://pypi2.example.com'}}
        >>> a.servers.update(new_server)
        >>> a.servers.update(new_server2)
        >>> a.save()
        >>> 'pypi' in a.servers
        True
        >>> 'pypi2' in a.servers
        True
    """

    RC_FILE = os.path.join(os.path.expanduser('~'), '.pypirc')

    def __init__(self, rc_file=None):
        if rc_file is None:
            self.rc_file = self.RC_FILE
        else:
            self.rc_file = rc_file

        self.conf = configparser.ConfigParser()

        if os.path.exists(self.rc_file):
            self.conf.read(self.rc_file)

        self._create_distutils()

        self._servers = {}
        for server in self._get_index_servers():
            if self.conf.has_section(server):
                server_conf = {server: dict(self.conf.items(server))}
                self.servers.update(server_conf)

    def _create_distutils(self):
        """Creates top-level distutils stanza in pypirc."""
        if not self.conf.has_section('distutils'):
            self.conf.add_section('distutils')

    def save(self):
        """Saves pypirc file with new configuration information."""
        for server, conf in self.servers.items():
            self._add_index_server()
            for conf_k, conf_v in conf.items():
                if not self.conf.has_section(server):
                    self.conf.add_section(server)
                self.conf.set(server, conf_k, conf_v)

        with open(self.rc_file, 'wb') as configfile:
            self.conf.write(configfile)
        self.conf.read(self.rc_file)
        self.patch_pip_conf()

    def _get_index_servers(self):
        """Gets index-servers current configured in pypirc."""
        idx_srvs = []
        if 'index-servers' in self.conf.options('distutils'):
            idx = self.conf.get('distutils', 'index-servers')
            idx_srvs = [srv.strip() for srv in idx.split('\n') if srv.strip()]
        return idx_srvs

    def _add_index_server(self):
        """Adds index-server to 'distutil's 'index-servers' param."""
        index_servers = '\n\t'.join(self.servers.keys())
        self.conf.set('distutils', 'index-servers', index_servers)

    @property
    def servers(self):
        """index-servers configured in pypirc."""
        return self._servers

    @servers.setter
    def servers(self, server):
        """Adds index-servers to pypirc."""
        self._servers.update(server)

    def patch_pip_conf(self):
        server = self.servers['pypi']
        repository = server['repository']
        repository_domain = urlparse(repository).netloc

        if server['username'] and server['password']:
            o = list(urlparse(repository))
            o[1] = '%s:%s@%s' % (server['username'], server['password'], o[1])
            repository = urlunparse(o)

        pip_conf = self._get_pip_conf()
        cfg = configparser.ConfigParser()
        cfg.read(pip_conf)
        G = 'global'

        if not cfg.has_section(G):
            cfg.add_section(G)

        get_or_empty = lambda option: cfg.get(G, option) if cfg.has_option(G, option) else ''  # @IgnorePep8
        set_clean = lambda option, value:cfg.set(G, option, value.strip())  # @IgnorePep8

        pre_index_url = get_or_empty('index-url')
        if pre_index_url is not repository:
            set_clean('index-url', repository)

        pre_trusted_hosts = get_or_empty('trusted-host')
        if repository_domain not in pre_trusted_hosts:
            set_clean('trusted-host', repository_domain + '\n' + pre_trusted_hosts)

        if cfg.has_option(G, 'extra-index-url'):
            cfg.remove_option(G, 'extra-index-url')

        try:
            os.makedirs(os.path.dirname(pip_conf))
        except OSError:
            pass

        with open(pip_conf, 'w') as fp:
            cfg.write(fp)

    def _get_pip_conf(self):
        virtual_env = os.environ.get('VIRTUAL_ENV')
        if virtual_env is None:
            if os.name == 'nt':
                path_to = os.path.join(os.path.expanduser('~'), 'pip')
            else:
                path_to = os.path.join(os.path.expanduser('~'), '.config/pip')
        else:
            path_to = os.path.abspath(virtual_env)

        if os.name == 'nt':
            pip_conf = os.path.join(path_to, 'pip.ini')
        else:
            pip_conf = os.path.join(path_to, 'pip.conf')
        return pip_conf

    def handle_args(self, args=None):
        parser = optparse.OptionParser()
        parser.add_option(
            '-s', '--server', help='Index Server Name [default: pypi]', metavar='SERVER', default='pypi')
        parser.add_option(
            '-r', '--repository', help='Repository URL', metavar='URL')
        parser.add_option(
            '-u', '--username', help='User Name', metavar='USERNAME')
        parser.add_option(
            '-p', '--password', help='Password', metavar='PASSWORD')
        options, args = parser.parse_args()

        if args:
            if len(args) == 1 and options.repository is None:
                options.repository = args[0]
            else:
                raise ValueError('cannot process args ')

        if options.repository and '@' in options.repository:
            if (options.username or options.password):
                raise ValueError('plese set one user-pass')
            else:
                o = urlparse(options.repository)
                options.username = o.username
                options.password = o.password
                netloc = o.hostname
                if o.port:
                    netloc += ":%s" % o.port
                o = list(o)
                o[1] = netloc
                options.repository = urlunparse(o)

        self.set(options.repository, options.username, options.password, options.server)

    def set(self, repository, username=None, password=None, server_alias='pypi'):
        if server_alias:
            server = self.servers.get(server_alias, {})
            if repository:
                server['repository'] = repository
            if username:
                server['username'] = username
            if password:
                server['password'] = password

            self.servers[server_alias] = server
            self.save()

        if self.servers:
            print('.pypirc and pip.conf configured.')

        else:
            print('.pypirc Empty!')


def main():
    SetPyPi().handle_args()


if __name__ == '__main__':
    main()
