# coding=utf-8
"""
vCloud Air Advanced Network Services
====================================

Advanced Networking Services (ANS) comes with a new/different set of API calls
than the normal vCD networking. This module breaks down the different parts of
the new API and its functionality. Now, firewall, NAT, routing, VPN, etc can
all be called and updated separately. Each class represents of a different part
of the ANS edge device.

"""

__author__ = 'Scott Schaefer'

import requests
from .util import check_http_response_error
from urllib.parse import urljoin
import re

class ANSSectionBase:
    """
    **Note** The ``org_info`` data structure can be supplied to the init method
    while omitting the other two keyword arguments.

    This is an abstract base class for ANS subclasses to inherit. It contains
    the general mechanisms for manipulating and referencing the ANS data.

    These classes support iteration as well as getting / deleting items based
    on index value. The values correspond to the rules or tunnels. The global
    configuration must be edited through the ``config_data`` member variable.
    """
    _ans_url = 'hybridity/api/gateways/{}/{}/config'

    def __init__(self, edge_id, org_info=None, vcdurl=None, token=None):
        """
        Base class for ANS sections. The org_info parameter will take precedence
        when passed. It is expected to be a dictionary with the keys returned
        from the VCA Session class after log in.

        :param str edge_id: UUID of the edge
        :param dict org_info: Dictionary containing Org login data
        :param str vcdurl: If org_info is absent, the vCD URL
        :param str token: If org_info is absent, the authorzation token
        """
        org_info = {} if org_info is None else org_info
        self.base_url = org_info.get('vcdurl', vcdurl)
        self.edge = edge_id
        self.headers = {'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        'x-vcloud-authorization': org_info.get('token', token)}
        self.config_data = {}
        self.records = [] #Will point to the repeating part of the config data:
                          #Firewall rules, Nat rules, tunnels, etc

    def __getitem__(self, index):
        return self.records[index]

    def __delitem__(self, index):
        del self.records[index]

    def __len__(self):
        return len(self.records)

    def __iter__(self):
        for r in self.records:
            yield r

    def _get_section_config(self, section):
        """
        Retreive the ANS configuration information from the edge API

        :param str section: The ANS section name, e.g: nat, firewall, etc
        :return: ``None``
        """
        full_url = self._create_ans_url(section)
        resp = requests.get(full_url, headers=self.headers)
        check_http_response_error(resp)
        self.config_data = resp.json()
        try:
            #Delete the version key from the JSON response since it errors the
            #API if it is submitted. The version is internally incrimented and
            #should not exist in the payload
            del self.config_data['version']
        except KeyError:
            pass

    def _update_section_config(self, section):
        """
        Submit the section config to the API

        :param str section: The ANS section name, e.g: nat, firewall, etc
        :return: ``None``
        """
        full_url = self._create_ans_url(section)
        resp = requests.put(full_url, headers=self.headers,
                            json=self.config_data)
        check_http_response_error(resp)

    def _create_ans_url(self, section):
        """
        Helper function to set up the full ANS url.

        :param str section: The section name to format into the URL
        :return:
        """
        section_url = self._ans_url.format(self.edge, section)
        return urljoin(self.base_url, section_url)

    def _validate_ip(self, ipstr):
        """
        Does a basic validation of an IP address. Bad addresses may still make
        it through the check. E.g: 1.1.1.1/99 would validate.

        :param str ipstr: The IP address or CIDR string to validate
        :return: ``None``
        """
        match = re.match(r'(\d+)\.(\d+)\.(\d+)\.(\d+)(?:/\d{1,2})?$',
                         ipstr, re.I)
        if not match:
            raise RuntimeError('Invalid IP Address entered')

        for octet in match.groups():
            if int(octet) > 255:
                raise RuntimeError("Invalid IP Address entered")

        return ipstr

class ANSFirewall(ANSSectionBase):
    """
    This class handles interactions with the Firewall configuration.
    """
    def get_config(self):
        """
        Retrieve the firewall configuration from the ANS API.

        :return: ``None``
        """
        self._get_section_config('firewall')
        self.records = self.config_data['firewallRules']['firewallRules']

    def save_config(self):
        """
        Save and submit the firewall configuration to the ANS API.

        :return: ``None``
        """
        self._update_section_config('firewall')

    def add_rule(self, name, source, destination, action='accept',
                 protocol='tcp', source_port='any', dest_port='any'):
        """
        Add a new firewall rule into the current configuration. Must retrieve
        configuration from API first before adding new rules.

        :param str name: The name of the rule
        :param str source: The source IP or interface: 'external' or 'internal'
        :param str destination: The destination IP or interface (see source)
        :param str action: Accept or Deny
        :param str protocol: The protocol for the rule (TCP, UDP, ICMP, etc)
        :param str source_port: Source port or range (33-44) or 'any'
        :param str dest_port: Destination port or range or 'any'
        :return: ``None``
        """
        directions = ['internal', 'external']
        new_rule = {'name': name,
                    'enabled': True,
                    'description': '',
                    'ruleType': 'user',
                    'action': action.lower(),
                    'destination': {
                        'ipAddress': [],
                        'vnicGroupId': []
                    },
                    'source': {
                        'ipAddress': [],
                        'vnicGroupId': []
                    },
                    'application': {
                        'service': []
                    }}
        app_service = {'protocol': protocol.lower(),
                       'port': [str(dest_port).lower()],
                       'sourcePort': [str(source_port).lower()]}

        if source.lower() in directions:
            new_rule['source']['vnicGroupId'].append(source.lower())
        else:
            new_rule['source']['ipAddress'].append(self._validate_ip(source))

        if destination.lower() in directions:
            new_rule['destination']['vnicGroupId'].append(destination.lower())
        else:
            new_rule['destination']['vnicGroupId'].append(self._validate_ip(destination))

        new_rule['application']['service'].append(app_service)
        if not len(self.config_data):
            raise RuntimeError('Empty configuration. Retrieve configuration using'
                               'get_config() first.')
        self.records.append(new_rule)


class ANSNat(ANSSectionBase):
    """
    This class handles interactions with the NAT configuration.
    """
    def get_config(self):
        """
        Retrieve the NAT configuration from the ANS API.

        :return: ``None``
        """
        self._get_section_config('nat')
        self.records = self.config_data['rules']['natRulesDtos']

    def save_config(self):
        """
        Save and submit the NAT configuration to the ANS API.

        :return: ``None``
        """
        self._update_section_config('nat')

    def add_rule(self, action, original_address, translated_address,
                 original_port='any', translated_port='any', protocol='tcp',
                 description=''):
        """
        Creates a new NAT rule and appends it to the existing list of NAT rules
        within the retrieved configuration data.

        :param str action: Type of rule, 'dnat' or 'snat'
        :param str original_address: IP address to translate
        :param str translated_address: IP address to translate into
        :param str original_port: Port, port range, or 'any' to translate from
        :param str translated_port: Port, range, or 'any' to translate to
        :param str protocol: TCP, UDP, ICMP, etc
        :param str description: Rule description
        :return: ``None``
        """
        if action.lower() not in ('snat', 'dnat'):
            raise RuntimeError('Invalid action. Must be either snat or dnat')

        new_rule = {'action': action.lower(),
                    'description': str(description),
                    'enabled': True,
                    'vnic': '0',
                    'originalAddress': self._validate_ip(original_address),
                    'originalPort': str(original_port),
                    'protocol': protocol.lower(),
                    'translatedAddress': self._validate_ip(translated_address),
                    'translatedPort': str(translated_port),
                    'ruleType': 'user',
                    'loggingEnabled': False}

        if new_rule['protocol'] == 'icmp':
            new_rule['icmpType'] = 'any'

        if not len(self.config_data):
            raise RuntimeError('Empty configuration. Retrieve configuration '
                               'using get_config() first.')
        self.records.append(new_rule)

class ANSIPSec(ANSSectionBase):
    """
    This class handles interactions with the IPSec configuration.
    """
    def get_config(self):
        """
        Retrieve the IPSec configuration from the ANS API.

        :return: ``None``
        """
        self._get_section_config('ipsec')
        self.records = self.config_data['sites']['sites']

    def save_config(self):
        """
        Save and submit the IPSec configuration to the ANS API.

        :return: ``None``
        """
        self._update_section_config('ipsec')

    def add_psk_tunnel(self, name, local_id, local_ip, peer_id, peer_ip,
                       local_subnets, peer_subnets, psk,
                       enc_algo='aes256', pfs=True, dhgroup=2, extension=None):
        """
        Add a new IPSec tunnel using Pre-Shared Key authentication.

        For a full description of parameters, see vCA documentation:
        https://pubs.vmware.com/vca/topic/com.vmware.vca.ans.api.doc/GUID-DD69C65F-FD55-4934-A67B-2BF65491F272.html

        :param str name: The friendly name of the IPSec tunnel
        :param str local_id: The external IP of the local edge gateway
        :param str local_ip: Endpoint network for the tunnel (usually external IP)
        :param str peer_id: The public IP of the remote endpoint
        :param str peer_ip: Public IP of the remote device (blank means wait for connection)
        :param str or list local_subnets: The networks to share across the VPN
        :param str or list peer_subnets: The remote networks shared across the VPN
        :param str psk: Pre-Shared Key
        :param str enc_algo: The encryption type/algorithm used
        :param bool pfs: Enable Perfect-Forward Secrecy or not
        :param int dhgroup: The Diffie-Hellman cryptography scheme
        :param str extension: Optional extension configuration directive
        :return: ``None``
        """
        new_tunnel = {'name': name,
                      'enabled': True,
                      'localId': local_id,
                      'localIp': local_ip,
                      'peerId': peer_id,
                      'peerIp': peer_ip,
                      'encryptionAlgorithm': enc_algo,
                      'enablePfs': pfs,
                      'dhGroup': 'dh{}'.format(dhgroup),
                      'localSubnets': {
                          'subnets': self._format_subnets(local_subnets)
                      },
                      'peerSubnets': {
                          'subnets': self._format_subnets(peer_subnets)
                      },
                      'psk': psk,
                      'authenticationMode': 'psk'}
        if extension:
            new_tunnel['extension'] = str(extension)

        if not len(self.config_data):
            raise RuntimeError('Empty configuration. Retrieve configuration '
                               'using get_config() first.')
        self.records.append(new_tunnel)

    def _format_subnets(self, subnets):
        """
        Format the subnets into a list structure usable in the IPSec
        configuration section.

        :param str or iterable subnets: The original list or single subnet
        :return: List of string subnets
        :rtype: list
        """
        if isinstance(subnets, (list, set, tuple)):
            return [str(x) for x in subnets]
        elif isinstance(subnets, str):
            return subnets.replace(' ','').split(',')
        else:
            raise RuntimeError('Invalid subnet format. Use a list or '
                               'comma-separated strings')
