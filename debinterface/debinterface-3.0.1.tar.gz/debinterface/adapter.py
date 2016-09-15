# -*- coding: utf-8 -*-
import socket


class NetworkAdapter:
    """ A representation a network adapter. """

    _valid = {
        'hotplug': {'type': bool},
        'auto': {'type': bool},
        'name': {'required': True},
        'address': {'type': 'IP'},
        'netmask': {'type': 'IP'},
        'network': {'type': 'IP'},
        'broadcast': {'type': 'IP'},
        'gateway': {'type': 'IP'},
        'bridge-opts': {'type': dict},
        'dns-nameservers': {'type': 'IP'},
        'addrFam': {'in': ['inet', 'inet6', 'ipx']},
        'source': {'in': ['dhcp', 'static', 'loopback', 'manual',
                          'bootp', 'ppp', 'wvdial', 'dynamic',
                          'ipv4ll', 'v4tunnel']},
        'hostapd': {},
        'bridge-opts': {'type': dict},
        'up': {'type': list},
        'down': {'type': list},
        'pre-up': {'type': list},
        'post-down': {'type': list}

    }

    @property
    def attributes(self):
        return self._ifAttributes

    def get_attr(self, attr):
        return self._ifAttributes[attr]

    def validateAll(self):
        """ Not thorough validations... and quick coded. Raise ValueError """

        for k, v in self._valid.iteritems():
            val = None
            if k in self._ifAttributes:
                val = self._ifAttributes[k]
            self.validateOne(k, v, val)

        # Logic checks
        if self._ifAttributes["source"] == "static":
            for req in ["address", "netmask"]:
                if req not in self._ifAttributes:
                    msg = ("{0} field is required for "
                           "static interface".format(req))
                    raise ValueError(msg)
        elif self._ifAttributes["source"] == "dhcp":
            for req in ["address", "netmask"]:
                if req in self._ifAttributes:
                    if self._ifAttributes[req] is not None:
                        msg = ("{0} field is forbidden for "
                               "dhcp interface".format(req))
                        raise ValueError(msg)

    def validateOne(self, opt, validations, val):
        """ Not thorough validations... and quick coded. Raise ValueError """
        if validations is None:
            return
        if not val:
            if 'required' in validations and validations['required'] is True:
                raise ValueError("{0} is a required option".format(opt))
            else:
                return

        if 'type' in validations:
            if validations['type'] == 'IP':
                try:
                    self.validateIP(val)
                except socket.error:
                    msg = ("{0} should be a valid IP "
                           "(got : {1})".format(opt, val))
                    raise ValueError(msg)
            else:
                if not isinstance(val, validations['type']):
                    msg = "{0} should be {1}".format(opt, validations['type'])
                    raise ValueError(msg)
        if 'in' in validations:
            if val not in validations['in']:
                err_validations = ", ".join(validations['in'])
                msg = "{0} should be in {1}".format(opt, err_validations)
                raise ValueError(msg)

    def validateIP(self, ip):
        """
            Validate an IP Address
            Raise socket.error on invalid IP
            Works for subnet masks too.
        """
        socket.inet_aton(ip)
        if "." not in str(ip):
            raise socket.error("I need an ip with dots or :")

    def setName(self, n):
        """ Set the name option of an interface. """
        self.validateOne('name', self._valid['name'], n)
        self._ifAttributes['name'] = str(n)

    def setAddrFam(self, i):
        """ Set the address family option of an interface. """

        self.validateOne('addrFam', self._valid['addrFam'], i)
        self._ifAttributes['addrFam'] = i

    def setAddressSource(self, s):
        """ Set the address source for an interface.

        Valid values are : dhcp, static, loopback, manual,
        bootp, ppp, wvdial, dynamic, ipv4ll, v4tunnel

            Args:
                s (string): address source for an interface
        """

        self.validateOne('source', self._valid['source'], s)
        self._ifAttributes['source'] = s

    def setAddress(self, a):
        """ Set the ipaddress of an interface. """

        self.validateOne('address', self._valid['address'], a)
        self._ifAttributes['address'] = a

    def setNetmask(self, m):
        """ Set the netmask of an interface. """

        self.validateOne('netmask', self._valid['netmask'], m)
        self._ifAttributes['netmask'] = m

    def setGateway(self, g):
        """ Set the default gateway of an interface. """

        self.validateOne('gateway', self._valid['gateway'], g)
        self._ifAttributes['gateway'] = g

    def setBroadcast(self, b):
        """ Set the broadcast address of an interface. """

        self.validateOne('broadcast', self._valid['broadcast'], b)
        self._ifAttributes['broadcast'] = b

    def setNetwork(self, w):
        """ Set the network identifier of an interface."""

        self.validateOne('network', self._valid['network'], w)
        self._ifAttributes['network'] = w

    def setAuto(self, t):
        """ Set the option to autostart the interface. """

        self.validateOne('auto', self._valid['auto'], t)
        self._ifAttributes['auto'] = t

    def setHotplug(self, h):
        """ Set the option to allow hotplug on the interface. """

        self.validateOne('hotplug', self._valid['hotplug'], h)
        self._ifAttributes['hotplug'] = h

    def setHostapd(self, h):
        """ Set the wifi conf file on the interface. """

        self.validateOne('hostapd', self._valid['hostapd'], h)
        self._ifAttributes['hostapd'] = h

    def setDnsNameservers(self, h):
        self.validateOne('dns-nameservers', self._valid['dns-nameservers'], h)
        self._ifAttributes['dns-nameservers'] = h

    def setBropts(self, opts):
        """
            Set or append the bridge options of an interface.
            This should be a dictionary mapping option names and values.
            In the interfaces file, options will have a 'bridge_' prefix.
        """

        self.validateOne('bridge-opts', self._valid['bridge-opts'], opts)
        self._ifAttributes['bridge-opts'] = opts

    def replaceBropt(self, key, value):
        self._ifAttributes['bridge-opts'][key] = value

    def appendBropts(self, key, value):
        new_value = self._ifAttributes['bridge-opts'][key] + value
        self._ifAttributes['bridge-opts'][key] = new_value

    def setUp(self, up):
        """Set and add to the up commands for an interface.
        Takes a LIST of shell commands.

            Args:
                up (list): list of shell commands
        """
        if isinstance(up, list):
            self._ifAttributes['up'] = up
        else:
            self._ifAttributes['up'] = [up]

    def appendUp(self, cmd):
        self._ensure_list(self._ifAttributes, "up", cmd)

    def setDown(self, down):
        """
            Set and add to the down commands for an interface.
            Takes a LIST of shell commands.
        """
        if isinstance(down, list):
            self._ifAttributes['down'] = down
        else:
            self._ifAttributes['down'] = [down]

    def appendDown(self, cmd):
        self._ensure_list(self._ifAttributes, "down", cmd)

    def setPreUp(self, pre):
        """
            Set and add to the pre-up commands for an interface.
            Takes a LIST of shell commands.
        """
        if isinstance(pre, list):
            self._ifAttributes['pre'] = pre
        else:
            self._ifAttributes['pre'] = [pre]

    def appendPreUp(self, cmd):
        self._ensure_list(self._ifAttributes, "pre-up", cmd)

    def setPostDown(self, post):
        """
            Set and add to the post-down commands for an interface.
            Takes a LIST of shell commands.
        """
        self._ifAttributes['post-down'] = post

    def appendPostDown(self, cmd):
        self._ensure_list(self._ifAttributes, "post-down", cmd)

    def setUnknown(self, key, val):
        """Stores uncommon options as there are with no special handling

        It's impossible to know about all available options
        """
        if 'unknown' not in self._ifAttributes:
            self._ifAttributes['unknown'] = {}
        self._ifAttributes['unknown'][key] = val

    def export(self, options_list=None):
        """ Return the ifAttributes data structure.

        You can pass a list of parameters you want
        """

        if options_list:
            ret = {}
            for k in options_list:
                try:
                    ret[k] = self._ifAttributes[k]
                except:
                    ret[k] = None
            return ret
        else:
            return self._ifAttributes

    def display(self):
        """Display a (kind of) human readable representation of the adapter."""
        print('============')
        for key in self._ifAttributes.keys():
            if isinstance(self._ifAttributes[key], list):
                print(key + ': ')
                for item in self._ifAttributes[key]:
                    print('\t' + item)

            elif isinstance(self._ifAttributes[key], dict):
                print(key + ': ')
                for item in self._ifAttributes[key].keys():
                    print('\t' + item + ': ' + self._ifAttributes[key][item])
            else:
                print(key + ': ' + str(self._ifAttributes[key]))
        print('============')

    def __init__(self, options=None):
        # Initialize attribute storage structre.
        self.reset()
        self.set_options(options)

    def reset(self):
        """ Initialize attribute storage structre. """
        self._ifAttributes = {}
        self._ifAttributes['bridge-opts'] = {}
        self._ifAttributes['up'] = []
        self._ifAttributes['down'] = []
        self._ifAttributes['pre-up'] = []
        self._ifAttributes['post-down'] = []

    def set_options(self, options):
        """ raise ValueError or socket.error on issue """

        # Set the name of the interface.
        if isinstance(options, str):
            self.setName(options)

        # If a dictionary of options is provided, populate the adapter options.
        elif isinstance(options, dict):
            try:
                for key in options.keys():
                    if key == 'name':
                        self.setName(options[key])
                    if key == 'addrFam':
                        self.setAddrFam(options[key])
                    elif key == 'source':
                        self.setAddressSource(options[key])
                    elif key == 'address':
                        self.setAddress(options[key])
                    elif key == 'netmask':
                        self.setNetmask(options[key])
                    elif key == 'gateway':
                        self.setGateway(options[key])
                    elif key == 'broadcast':
                        self.setBroadcast(options[key])
                    elif key == 'network':
                        self.setNetwork(options[key])
                    elif key == 'auto':
                        self.setAuto(options[key])
                    elif key == 'allow-hotplug':
                        self.setHotplug(options[key])
                    elif key == 'bridgeOpts':
                        self.setBropts(options[key])
                    elif key == 'up':
                        self.setUp(options[key])
                    elif key == 'down':
                        self.setDown(options[key])
                    elif key == 'pre-up':
                        self.setPreUp(options[key])
                    elif key == 'post-down':
                        self.setPostDown(options[key])
                    elif key == 'hostapd':
                        self.setHostapd(options[key])
                    elif key == 'dns-nameservers':
                        self.setDnsNameservers(options[key])
                    else:
                        # Store it as if
                        self.setUnknown(key, options[key])
            except:
                self.reset()
                raise
        else:
            raise ValueError("No arguments given. Provide a name "
                             "or options dict.")

    def _ensure_list(self, dic, key, value):
        """Ensure the data for the given key will be in a list.
        If value is a list, will be flattened

            Args:
                dic (dict): source dict
                key (string): key to use in dic
                value: the data. Will be appended into a list if it's not one
        """
        if key not in dic:
            dic[key] = []
        if type(dic[key]) != list:
            tmp = dic[key]
            dic[key] = [tmp]
        if type(value) == list:
            dic[key] += value
        else:
            dic[key].append(value)
