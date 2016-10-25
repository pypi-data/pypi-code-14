from cement.core.controller import CementBaseController, expose
from cement.utils.shell import Prompt
from droplet import Droplet
import os
import json
import requests
import re
import ConfigParser
import shutil
from subprocess import call
from python_hosts import Hosts, HostsEntry
from terminaltables import AsciiTable


class DOController(CementBaseController):
    class Meta:
        label = 'iDO tool'
        description = "iDO controller"

        arguments = [
            (['-n', '--name'], dict(action='store', help='Droplet name')),
            (['-i', '--id'], dict(action='store', help='Droplet ID')),
        ]

    def _input_service_url(self):
        service_url = Prompt("Press enter the droplet service URL:", default='')

        if not service_url.input or len(service_url.input) == 0:
            print 'Droplet service URL is required.'
            exit(1)

        config = ConfigParser.RawConfigParser()
        config.add_section('service')
        config.set('service', 'url', service_url.input)

        with open(self.conf_file_path, 'wb') as configfile:
            config.write(configfile)

    def _setup(self, app_obj):
        super(CementBaseController, self)._setup(app_obj)
        self.ETC_HOSTS_PRIVATE_FILENAME = self.app.config.get('global', 'etc_hosts_private_filename')
        self.ETC_HOSTS_PUBLIC_FILENAME = self.app.config.get('global', 'etc_hosts_public_filename')

        self.user_home = os.environ['HOME']
        self.conf_dir_name = self.app.config.get('global', 'conf_dir_name')
        self.conf_file_name = self.app.config.get('global', 'conf_file_name')
        self.conf_home = os.path.join(self.user_home, self.conf_dir_name)
        self.conf_file_path = os.path.join(self.conf_home, self.conf_file_name)

        self.init_config()

    def init_config(self):
        # Create config dir if not available
        if not os.path.exists(self.conf_home):
            os.makedirs(self.conf_home)

        # Check if config file exists with content
        config = ConfigParser.ConfigParser()
        config.read(self.conf_file_path)
        try:
            self.service_url = config.get('service', 'url')
            if not self.service_url:
                self.init()

        except ConfigParser.NoSectionError:
            self._input_service_url()

    @expose(help="Init configuration")
    def init(self):
        shutil.rmtree(self.conf_home)
        self.init_config()

    def _get_file_path(self, filename):
        return os.path.join(self.conf_home, filename)

    @expose(help="List all droplets", aliases=['l'])
    def list(self):
        droplets = self._get_droplet_objects()
        self._render_table(droplets)

    @staticmethod
    def _render_table(droplets):
        droplet_table = []
        headers = ['#', 'name', 'id', 'private ip', 'public ip', 'status']
        droplet_table.append(headers)
        i = 0
        for d in droplets:
            i += 1
            dt = [
                i,
                d.get_name(),
                d.get_id(),
                d.get_ipv4('private'),
                d.get_ipv4('public'),
                d.get_status()
            ]
            droplet_table.append(dt)

        table = AsciiTable(droplet_table)
        print table.table

    @expose(help="Generate /etc/hosts with private IPs", aliases=['pri'])
    def etc_hosts_private(self):
        droplets = self._get_droplet_objects()
        self._write_etc_hosts(droplets, private=True)

    @expose(help="Generate /etc/hosts with public IPs", aliases=['pub'])
    def etc_hosts_public(self):
        droplets = self._get_droplet_objects()
        self._write_etc_hosts(droplets, private=False)

    def _get_droplet_objects(self):
        droplets_config = self._get_droplets()
        droplets = []

        for a_droplet_config in droplets_config['droplets']:
            a_droplet = Droplet(a_droplet_config)
            droplets.append(a_droplet)

        return droplets

    @staticmethod
    def render_droplets(droplets):
        return DOController._render_table(droplets)

    @staticmethod
    def _remove_file_if_exists(filename):
        if os.path.isfile(filename):
            os.remove(filename)

    def _write_etc_hosts(self, droplets, private):
        file_path = self._get_file_path(self.ETC_HOSTS_PRIVATE_FILENAME) \
            if private else self._get_file_path(self.ETC_HOSTS_PUBLIC_FILENAME)

        self._remove_file_if_exists(file_path)
        hosts = Hosts(path=file_path)

        for d in droplets:
            if d.get_ipv4('private') is None:
                self.app.log.warn('%s does not have a private IP' % d.get_name())
                continue

            ipv4_address = d.get_ipv4('private') if private else d.get_ipv4('public')
            new_entry = HostsEntry(entry_type='ipv4', address=ipv4_address, names=[d.get_name(), str(d.get_id())])
            hosts.add([new_entry])

        hosts.write()
        print self.file_get_contents(file_path)

    def _get_server_url(self):
        return self.service_url

    def _get_droplets(self):
        try:
            r = requests.get(self._get_server_url())
        except requests.exceptions.MissingSchema as e:
            print str(e)
            exit(1)
        else:
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.app.log.error("Error while getting connecting server: %s" % r.text)
                return {}

    @expose(help="Find a droplet", aliases=['f'])
    def find(self):
        droplets = self._get_droplet_objects()
        droplet_name = self.app.pargs.name

        if not droplet_name:
            self.render_droplets(droplets)
            return

        found_droplets = []
        for d in droplets:
            if re.search(droplet_name, d.get_name(), re.IGNORECASE):
                found_droplets.append(d)

        print 'Found %d droplets' % len(found_droplets)
        self.render_droplets(found_droplets)

    @expose(help="SSH into a droplet")
    def ssh(self):
        droplet_name = self.app.pargs.name
        droplet_id = self.app.pargs.id

        if droplet_name:
            self._ssh_with_name(droplet_name)

        if droplet_id:
            self._ssh_with_id(droplet_id)

    def _ssh_with_name(self, droplet_name):
        droplets = self._get_droplet_objects()
        found_droplets = []
        for d in droplets:
            if re.search(droplet_name, d.get_name(), re.IGNORECASE):
                found_droplets.append(d)

        if len(found_droplets) == 1:
            self._ssh(found_droplets[0])
        else:
            print 'Found %d droplets. Please use unique ID with --id flag if needed!' % len(found_droplets)
            self.render_droplets(found_droplets)

    def _ssh_with_id(self, droplet_id):
        droplets = self._get_droplet_objects()

        for d in droplets:
            if str(droplet_id) == str(d.get_id()):
                self._ssh(d)

    @staticmethod
    def _check_port(ip, port, timeout=3):
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        if result != 0:
            raise Exception('Port not open')

    @staticmethod
    def file_get_contents(filename):
        with open(filename) as f:
            return f.read()

    def _ssh(self, d):
        try:
            print 'Checking IP: %s' % d.get_ipv4('private')
            self._check_port(d.get_ipv4('private'), 22)
        except Exception as e:
            print 'Checking IP: %s' % d.get_ipv4('public')
            call(["ssh", d.get_ipv4('public')])
        else:
            call(["ssh", d.get_ipv4('private')])
