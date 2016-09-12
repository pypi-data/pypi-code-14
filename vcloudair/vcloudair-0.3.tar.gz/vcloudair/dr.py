# coding=utf-8
"""
Description
===========


"""

__author__ = 'Scott Schaefer'

import requests
from urllib.parse import urljoin
import xml.etree.ElementTree as ET
from .util import check_http_response_error

UUID_L = 36

class DisasterRecovery:

    def __init__(self, org_info=None, vcdurl=None, token=None, org_uuid=None,
                 version='5.7'):
        """
        Provides an interface to a DR environment with access to failover and
        cleanup actions.

        :param dict org_info: Data structure from a VCAODSession containing all required fields
        :param str vcdurl: The endpoint for the OD/DR instance
        :param str token: Authorization token
        :param str org_uuid: The org UUID for the DR instance
        :param str version: The API version to use
        """

        org_info = {} if org_info is None else org_info
        if not all(
                (org_info.get('vcdurl', vcdurl),
                 org_info.get('token', token),
                 org_info.get('org_uuid', org_uuid))):
            raise RuntimeError("Missing required parameter, URL, Token, or UUID")

        baseapi = '/api/compute/api/org/{}/'.format(org_info.get('org_uuid',
                                                               org_uuid))
        self.base_api_url = urljoin(org_info.get('vcdurl',vcdurl), baseapi)
        self.version = org_info.get('version', version)
        self.headers = {'Accept': 'application/*+xml;version={}'.format(self.version),
                        'x-vcloud-authorization': org_info.get('token', token)}
        self.replications = {}

    def retrieve_replications(self):
        """
        Connect to the DR API endpoint and retrieve the list of replications

        :return: ``None``
        """
        url = urljoin(self.base_api_url, 'replications')
        resp = requests.get(url, headers=self.headers)
        check_http_response_error(resp)
        self._parse_replication_list(resp.text)

    def do_test_failover(self, uuid='None', power_on=True, total=False):
        self.do_failover(uuid, power_on, total, test=True)

    def do_failover(self, uuid='None', power_on=True, total=False, test=False):
        """
        Initates a failover or test failover for a VM or all VMs

        :param str uuid: The uuid of the VM to failover
        :param bool power_on: Whether to power on the VM during the test fail
        :param bool total: Fail over all VMs. This takes precedence if UUID is provided
        :param bool test: Whether this is a test failover or actual failover
        :return: ``None``
        """
        headers = {}
        if test:
            action = '/action/testFailover'
            headers['Content-Type'] = 'application/vnd.vmware.hcs.testFailoverParams+xml'
        else:
            action = '/action/failover'
        headers.update(self.headers)

        if total is True:
            vm_list = [x for x in self.replications]
        else:
            vm_list = [uuid] if uuid in self.replications else []

        for vm in vm_list:
            action_url = self.replications.get(vm)['href'] + action
            payload = self._setup_xml_payload(vm, power_on, test=test)
            resp = requests.post(action_url, data=payload, headers=headers)
            check_http_response_error(resp)

    def do_test_cleanup(self, uuid='None', total=False):
        """
        Clean up the test failover from a VM or all VMs

        :param str uuid: The UUID of the VM that is being cleaned up
        :param bool total: Clean up all the VMs. This takes precedence
        :return: ``None``
        """
        action = '/action/testCleanup'
        if total is True:
            vm_list = [x for x in self.replications]
        else:
            vm_list = [uuid] if uuid in self.replications else []

        for vm in vm_list:
            action_url = self.replications.get(vm)['href'] + action
            resp = requests.post(action_url, headers=self.headers)
            check_http_response_error(resp)

    def _parse_replication_list(self, xmlstringdata):
        """
        Convert the XML data from the Replication list into ETree format and
        parse out the replications in the list. This will populate the replications
        data structure with ID, href, and names for easier access.

        :param str xmlstringdata: The body from the API request to the rep endpoint
        :return: ``None``
        """
        replist = ET.fromstring(xmlstringdata)
        nsmap = {'vcd': 'http://www.vmware.com/vcloud/v1.5'}
        for rep in replist.findall('vcd:Reference', nsmap):
            href = rep.get('href')
            uuid = href[-UUID_L:]
            data = self.replications.setdefault(uuid, {})
            data['href'] = href
            rep_details = ET.fromstring(requests.get(href, headers=self.headers).text)
            data['name'] = rep_details.get('name')

    def _setup_xml_payload(self, uuid, power_on=True, test=False):
        """
        Create the XML payload data for the Failover and TestFailover endpoints

        :param str uuid: The VM uuid (this is just for identification, not critical)
        :param bool power_on: Whether the VM will be powered on during failover
        :param bool test: Whether to generate data for a test or actual failover
        :return: XML data in string format
        :rtype: ``str``
        """
        tagname = 'FailoverParams'
        if test:
            tagname = 'Test'+tagname
        xmld = ET.Element(tagname)
        xmld.set('name', uuid)
        power = ET.Element('PowerOn')
        power.text = "1" if power_on else "0"
        xmld.append(power)
        if test:
            sync = ET.Element('Synchronize')
            sync.text = "0"
            xmld.append(sync)
        xmld.set('xmlns', 'http://www.vmware.com/vr/v6.0')
        return ET.tostring(xmld, encoding='unicode', method='xml')
