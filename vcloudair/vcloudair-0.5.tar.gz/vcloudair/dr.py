# coding=utf-8
"""
vCloud Air Disaster Recovery
============================

The disaster recovery module provides a class for accessing DRaaS in vCloud Air
and executing DR actions: Failover, Test Failover, and Test Cleanup.

This class is meant for DR 2.x and will not work properly with DR 1.x.

"""

__author__ = 'Scott Schaefer'

import requests
from requests import Request, Session
from urllib.parse import urljoin
import xml.etree.ElementTree as ET
from .util import check_http_response_error, ThreadPool, UUID_L
from time import sleep
import datetime

nsmap = {'vcd': 'http://www.vmware.com/vcloud/v1.5'}

class DisasterRecovery:
    """
    This class works with DRaaS version 2.x. Replication status or configuration
    cannot be viewed or modified by this class. It's purpose is to take actions
    against replicated VMs: Fail, Test, Recover (after test).

    Failing back cannot be done from this class, nor can recovery of a failed
    VM.
    """
    def __init__(self, org_info=None, vcdurl=None, token=None, org_uuid=None,
                 version='5.7'):
        """
        Provides an interface to a DR environment with access to failover and
        cleanup actions.

        :param dict org_info: Data structure from a VCAODSession containing
            all required fields
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

        baseapi = 'api/org/{}/'.format(org_info.get('org_uuid',
                                                               org_uuid))
        self.base_api_url = urljoin(org_info.get('vcdurl',vcdurl), baseapi)
        self.version = org_info.get('version', version)
        self.headers = {'Accept': 'application/*+xml;version={}'.format(self.version),
                        'x-vcloud-authorization': org_info.get('token', token)}
        self.replications = {}
        self.task_pool = ThreadPool(20)
        self.action_errors = []

    def retrieve_replications(self):
        """
        Connect to the DR API endpoint and retrieve the list of replications.
        After retrieval, replication information is stored in the ``replications``
        member variable.

        :return: ``None``
        """
        url = urljoin(self.base_api_url, 'replications')
        resp = requests.get(url, headers=self.headers)
        check_http_response_error(resp)
        self._parse_replication_list(resp.text)

    def dump_replication_details(self, filelocation='details.csv'):
        """
        Write the replication names and UUIDs into a file

        :param str filelocation: The file path/name of where to write the data
        :return: ``None``
        """
        with open(filelocation, mode='w', encoding='utf-8') as f:
            for k,v in self.replications.items():
                line = "{},{}\n".format(k,v['name'])
                f.write(line)

    def do_test_failover(self, *uuids, power_on=True, total=False):
        """
        Initates a test failover, specifically, against the supplied VMs or the
        entire DR environment.

        :return: ``None``
        """
        self.do_failover(*uuids, power_on=power_on, total=total, test=True)

    def do_failover(self, *uuids, power_on=True, total=False, test=False):
        """
        Initates a failover or test failover for a VM or all VMs

        :param uuids: The uuids of the VMs to failover
        :param bool power_on: Whether to power on the VM during the test fail
        :param bool total: Fail over all VMs. This takes precedence if UUID
            is provided
        :param bool test: Whether this is a test failover or actual failover
        :return: ``None``
        """
        headers = {}
        if test:
            action = '/action/testFailover'
            headers['Content-Type'] = 'application/vnd.vmware.hcs.testFailoverParams+xml'
        else:
            headers['Content-Type'] = 'application/vnd.vmware.hcs.FailoverParams+xml'
            action = '/action/failover'
        headers.update(self.headers)
        self._do_action(*uuids, action=action, headers=headers,
                        power_on=power_on, total=total, test=test)

    def do_test_cleanup(self, *uuids, total=False):
        """
        Clean up the test failover from a VM or all VMs

        :param uuids: The UUIDs of the VMs that are being cleaned up
        :param bool total: Clean up all the VMs. This takes precedence
        :return: ``None``
        """
        action = '/action/testCleanup'
        self._do_action(*uuids, action=action, headers=self.headers,
                        total=total, test=True)

    def _do_action(self, *uuids, action=None, headers=None, power_on=True,
                   total=False, test=False):
        """
        Execute a DR action against the API. Action can be failover, test, or
        cleanup (at time of writing).

        :param tuple uuids: The UUIDs of the VMs that are being acted upon
        :param str action: The action suffix that appends the URL
        :param dict headers: HTTP headers to be submitted
        :param bool power_on: Whether to power on machines. Failovers only.
        :param bool total: Whether to fail over ALL VMs
        :param bool test: Whether this is a test failover or not
        :return: ``None``
        """
        payload = None
        self.action_errors.clear()
        if total is True:
            vm_list = [x for x in self.replications]
        else:
            vm_list = []
            for uuid in uuids:
                if uuid in self.replications and uuid not in vm_list:
                    vm_list.append(uuid)

        for vm in vm_list:
            action_url = self.replications.get(vm)['href'] + action
            if 'failover' in action.lower():
                payload = self._setup_xml_payload(vm, power_on, test=test)
            request = Request('POST', action_url, data=payload,
                              headers=headers).prepare()
            self.task_pool.add(self._submit_vcd_task, request,
                               name=self.replications.get(vm)['name'],
                               uuid=vm)
        self.task_pool.join()

    def _parse_replication_details(self, vmdata):
        """
        Called via threads for grabbing the details of each replicated VM.
        Threaded for faster retrieval.

        :param dict vmdata: The dictionary containing the VM replication data
        :return: ``None``
        """
        rep_details = ET.fromstring(requests.get(vmdata['href'],
                                                 headers=self.headers).text)
        vmdata['name'] = rep_details.get('name')

    def _parse_replication_list(self, xmlstringdata):
        """
        Convert the XML data from the Replication list into ETree format and
        parse out the replications in the list. This will populate the replications
        data structure with ID, href, and names for easier access.

        :param str xmlstringdata: The body from the API request to the rep endpoint
        :return: ``None``
        """
        replist = ET.fromstring(xmlstringdata)
        for rep in replist.findall('vcd:Reference', nsmap):
            href = rep.get('href')
            uuid = href[-UUID_L:]
            data = self.replications.setdefault(uuid, {})
            data['href'] = href
            self.task_pool.add(self._parse_replication_details, data)
        self.task_pool.join()

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

    def _submit_vcd_task(self, request, **kwargs):
        """
        Submits a prepared request object to VCD. Expects a VCD task object to
        be returned from the HTTP call.

        :param request: Prepared request object
        :return: ``None``
        """
        s = Session()
        name = kwargs.get('name', 'Unnamed VM')
        uuid = kwargs.get('uuid', 'Unknown UUID')
        resp = s.send(request)
        idletime = datetime.datetime.utcnow()
        percentage = '0'
        while True:
            delta = (datetime.datetime.utcnow() - idletime).seconds
            if resp.status_code >= 400:
                print(name, ' Error! ', resp.reason)
                self.action_errors.append((uuid,name,resp.reason))
                break
            elif delta >= 600: #10 Minutes
                print(name, ' Task Hung Timeout!')
                self.action_errors.append((uuid,name,'Task Timeout - 10min'))
                break
            vcdtask = ET.fromstring(resp.text)
            progress = vcdtask.find('vcd:Progress', nsmap)
            if progress is None or progress.text == '100':
                print(name, ' Done!')
                break
            print('{} -- {} percent'.format(name, progress.text))
            if percentage != progress.text:
                idletime = datetime.datetime.utcnow()
                percentage = progress.text
            sleep(10)
            resp = requests.get(vcdtask.get('href'), headers=self.headers)
        s.close()
