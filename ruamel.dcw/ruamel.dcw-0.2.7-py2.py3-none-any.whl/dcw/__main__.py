# coding: utf-8

from __future__ import print_function
from __future__ import absolute_import

import sys                                   # NOQA
import os                                    # NOQA
import traceback                             # NOQA
import ruamel.yaml                           # NOQA
from ruamel.std.pathlib import Path          # NOQA
from ruamel.showoutput import show_output    # NOQA

from ruamel.dcw import __version__

dbg = int(os.environ.get('DCWDBG', 0))
env_inc = Path('.dcw_env_vars.inc')


class DockerComposeWrapper(object):
    def __init__(self):
        self._args = None
        self._file_name = None
        self._data = None
        for p in sys.path:
            pp = os.path.join(p, 'docker-compose')
            if dbg > 0:
                print('pp', pp)
            if os.path.exists(pp):
                self._dc = pp
                break
        else:
            print(sys.path)
            print('docker-compose not found in path')
            sys.exit(1)

    def process_args(self, args):
        if (len(args) > 1) and args[0] in ['-f', '--file']:
            self._file_name = self.find_yaml(args[1])
            self._args = args[2:]
        elif (len(args) > 0) and (args[0].startswith('--file=') or args[0].startswith('-f=')):
            self._file_name = self.find_yaml(args[0].split('=', 1)[1])
            self._args = args[1:]
        else:
            self._file_name = Path('docker-compose.yml')
            self._args = args

    def find_yaml(self, name):
        for file_name in [
            Path(name),                                         # full path
            Path(name) / 'docker-compose.yml',                  # base dir
            Path('/opt/docker') / name / 'docker-compose.yml',  # standard docker dir
        ]:
            if file_name.exists():
                # print('Found', file_name)
                file_name.parent.chdir()
                return file_name

    def load_yaml(self):
        with self._file_name.open() as fp:
            self._data = ruamel.yaml.load(fp, Loader=ruamel.yaml.RoundTripLoader)

    def set_os_env_defaults(self):
        envs = self._data.get('user-data', {}).get('env-defaults')
        if envs is None:
            return
        # some values that can be <named in
        host_name_file = Path('/etc/hostname')
        lookup = {}
        lookup['hostname'], lookup['domain'] = host_name_file.read_text().strip().split('.', 1)
        # assume hostname is in the hosts file
        hosts_file = Path('/etc/hosts')
        for line in hosts_file.read_text().splitlines():
            sline = line.split('#')[0].split()
            if lookup['hostname'] in sline:
                lookup['hostip'] = sline[0]
        # print(lookup)
        fp = None
        if not env_inc.exists() or (env_inc.stat().st_mtime <
                                    self._file_name.stat().st_mtime):
            print('writing', str(env_inc))
            fp = env_inc.open('w')
        for k in envs:
            if k not in os.environ:
                value = str(envs[k])
                if value and value[0] == '<':
                    value = lookup.get(value[1:], value)
                os.environ[k] = value  # str for those pesky port numbers
            if fp:
                fp.write(u'export {}="{}"\n'.format(k, os.environ[k]))
        if fp:
            fp.close()
        # print(env_inc.read_text())
        # sys.exit(1)

    def write_temp_file_call_docker_compose(self):
        odata = self.rewrite_data()
        sys.argv = [self._dc]
        alt_yaml = Path('.dcw_alt.yml')
        ruamel.yaml.round_trip_dump(odata, stream=alt_yaml.open('wb'),
                                    encoding='utf-8')
        sys.argv.append('--file={}'.format(alt_yaml))
        sys.argv.extend(self._args)
        self.call_docker_compose()

    def call_docker_compose(self):
        # print(sys.argv)
        try:
            import compose.cli.main
        except ImportError:
            print(sys.path)
        compose.cli.main.main()

    def rewrite_data(self):
        odata = ruamel.yaml.comments.CommentedMap()
        for k in self._data:
            try:
                if k == 'user-data' or k.startswith('user-data-'):
                    continue
            except TypeError:
                pass
            odata[k] = self._data[k]
        return odata

    def run_truncate(self):
        # dc ps -q -> id of container
        alt_yaml = Path('.dcw_alt.yml')
        cid = show_output([self._dc, '--file={}'.format(alt_yaml), 'ps', '-q'],
                          verbose=-1).rstrip()
        print(cid)
        path = Path('/var/lib/docker/containers/{}/{}-json.log'.format(cid, cid))
        cmd = 'sudo truncate -s 0 ' + str(path)
        # print(cmd)
        os.system(cmd)
        # res = show_output(['sudo', 'truncate', '-s ', str(path)])

    def run_bash(self):
        odata = self.rewrite_data()
        # first of the services
        for x in odata['services']:
            name = odata['services'][x].get('container_name')
            if not name:
                raise NotImplementedError
            if name.startswith('${') and name.endswith('}'):
                name = os.environ.get(name[2:-1])
            os.system('docker exec -it {} /bin/bash'.format(name))

    def run(self):
        dcw = False
        if self._args and self._args[0].startswith('dcw-'):
            self._args[0] = self._args[0][4:]
            dcw = True
        dcw = dcw  # temporary to use it without getting warning
        # should check if it is a docker-compose command first
        if self._args[0] == 'expand':
            ruamel.yaml.round_trip_dump(self.rewrite_data(), stream=sys.stdout,
                                        encoding='utf-8')
            print('------ env:')
            with open(env_inc) as fp:
                print(fp.read())
            return 0
        if self._args[0] == 'truncate':
            self.run_truncate()
            return 0
        if self._args[0] == 'bash':
            self.run_bash()
            return 0
        return self.write_temp_file_call_docker_compose()

    def help_asked(self):
        """return true if help found in arguments"""
        if '-h' in sys.argv[1:] or '--help' in sys.argv[1:]:
            return True
        return False

    def version_asked(self):
        """return true if help found in arguments"""
        if 'version' in sys.argv[1:] or '--version' in sys.argv[1:]:
            print('dcw version:', __version__)
            return True
        return False


def main():
    if dbg > 0:
        print('---------------------------------')

    dcw = DockerComposeWrapper()
    dcw.process_args(sys.argv[1:])
    # some special handling
    if dcw.version_asked():
        sys.argv[1:] = ['version']
        dcw.call_docker_compose()
        res = 0
    elif dcw.help_asked():
        print('here2')
        try:
            dcw.call_docker_compose()
        except SystemExit:
            for cmd, hlp in sorted((
                    ('bash', 'run bash in container'),
                    ('expand', 'show expanded YAML and {}'.format(env_inc)),
                    ('truncate', 'truncate log file (needs sudo)'),
            )):
                print(' *{:<18s} {}'.format(cmd, hlp))
            print('\n *: ruamel.dcw extensions')
        res = 0
    else:
        dcw.load_yaml()
        dcw.set_os_env_defaults()
        res = dcw.run()
    sys.exit(res)

if __name__ == "__main__":
    main()
