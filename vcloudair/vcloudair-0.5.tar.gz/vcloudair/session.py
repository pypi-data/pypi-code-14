# coding=utf-8
"""
vCloud Air Sessions
===================

The VCA session module handles logging into vCloud Air and subsequent virtual
datacenters within the service offering.

For Virtual Private Clouds (VPC) and Dedicated Clouds (DC) multiple virtual
datacenters (vDCs) can be logged into at once. The Session
class will store the tokens for the vDCs and allow them to be looked up by
vDC name in the key format: session[vdc].

For On-Demand environments, an instance can be logged into via its index number.
The index numbers can be found through the method call ``show_instance_list()``
on the On-Demand session class instance.

"""

__author__ = 'Scott Schaefer'

import json
import requests
import xml.etree.ElementTree as ET
from .util import check_http_response_error, UUID_L

class VCASession:
    """
    This is the session class to handle VPC / Dedicated instances. This uses the
    older vchs platform instead of the on-demand platform.

    Each session class can handle and track multiple vCD login tokens.
    """
    _vca_login_url = 'https://vchs.vmware.com/api/vchs/sessions'

    def __init__(self, version='5.6', username=None, password=None):
        """
        Create login sessions to vCA (root) and vCD (child) orgs.

        :param str version: API version number, e.g: '5.6'
        :param str username: vCloud Air username
        :param str password: vCloud Air password
        """
        self.login_url = self._vca_login_url
        self.version = str(version)
        self.username = username
        self.password = password
        self.headers = {}
        self.service_list_url = None
        self.vca_token = None
        self.vcd_tokens = {}
        self.vdc_list = {}

    def __getitem__(self, orgname):
        """
        Implements session[orgname] to retrieve the data for an org after login

        :param str orgname: The name of the vCD org
        :return: Dict of token, UUID, and APIURL
        :rtype: dict
        """
        return self.vcd_tokens[orgname.lower()]

    def login(self, username=None, password=None, orgname='',
              vcd_url=None):
        """
        Log into either the vCA main portal or directly into a vCloud Director
        instance.

        :param str username: vCloud Air Username
        :param str password: vCloud Air Password
        :param str orgname: vCloud Director Org Name
        :param str vcd_url: URL to a vCD Instance
        :return: None or Org login details
        """
        orgname = orgname.lower()
        if username:
            self.username = username
        if not self.username:
            raise RuntimeError('No username specified')

        if password:
            self.password = password
        if not self.password:
            raise RuntimeError('No password specified')

        if vcd_url and not orgname:
            raise RuntimeError('Cannot log into vCD without an org name')

        if vcd_url:
            return self._vcd_login(vcd_url, orgname)
        else:
            return self._portal_login(orgname)

    def _portal_login(self, orgname=None):
        """
        Log in using the vCloud Air portal process and retrieve the vCA token
        and org listing.

        :param str or None orgname: Optional OrgVDC to create a session on
        :return: None or Org Data
        """

        self.headers['Accept'] = 'application/xml;version={}'.format(self.version)
        response = requests.post(self.login_url,headers=self.headers,
                                 auth=(self.username,self.password))
        check_http_response_error(response)

        self.vca_token = response.headers.get('x-vchs-authorization')
        self.headers['x-vchs-authorization'] = self.vca_token
        self._parse_service_list_url(response.text)

        response = requests.get(self.service_list_url, headers=self.headers)
        check_http_response_error(response)
        self._parse_vcd_org_list(response.text)

        if orgname:
            return self.login_to_vdc(orgname)

    def login_to_vdc(self, orgname):
        """
        Create a login session to a specific VDC based on the org name specified

        **Note:** The org name refers to the actual Org name and not the VDC
        name. Usually they are the same, but the VDC name may be different. While
        not the case in vCloud Air today (2016), a single Org may contain
        multiple VDCs.

        :param str orgname: The orgname for which to create the session
        :return: Dict of org data from the login: UUID, Token, APIURL
        :rtype: dict
        """
        orgname = orgname.lower()
        vcd_session_url = self.vdc_list.get(orgname)
        if not vcd_session_url:
            raise RuntimeError("Unable to locate VDC '{}'".format(orgname))
        resp = requests.post(vcd_session_url, headers=self.headers)
        check_http_response_error(resp)
        self.vcd_tokens[orgname] = self._parse_vdc_org_token(resp.text)
        return self.vcd_tokens[orgname]

    @property
    def vdc_names(self):
        return [x for x in self.vdc_list]

    def _parse_vcd_org_list(self, xmlstring):
        """
        Cycle through the services returned and then the VDCs under each
        service and store the org name and URL

        :param str xmlstring: XML content returned from the service list URL
        :return: ``None``
        """
        servlist = ET.fromstring(xmlstring)
        for service in servlist: #Services include, DR, VPC, DC, etc
            resp = requests.get(service.get('href'), headers=self.headers)
            vdclist = ET.fromstring(resp.text)
            for vdc in vdclist: #Under each service is a list of vDCs in vCloud
                try:
                    org_url = vdc[0].get('href') #The first item under a vdc record
                                                 #Is a link containing its url
                    self.vdc_list[vdc.get('name').lower()] = org_url
                except IndexError:
                    pass

    def _parse_vdc_org_token(self, xmlstring):
        """
        Parse the VDC item and pull out the attributes to allow logging into
        the vCD instance directly

        :param str xmlstring:
        :return: Dictionary containing the token, API URL, and Header Name
        :rtype: dict
        """
        session = ET.fromstring(xmlstring)
        vdc = session[1] #Object 0 is the <link> element, 1 is the actual VDC
        vdc_api_url, uuid = vdc.get('href').split(':443/api/vdc/') #API Root URL for the VDC
        return {'auth-header': vdc.get('authorizationHeader'),
                'token': vdc.get('authorizationToken'),
                'vcdurl': vdc_api_url,
                'org_uuid': uuid,
                'version': self.version}

    def _parse_service_list_url(self, xmlstring):
        """
        Parse the service list URL from the XML response after the vCA token
        is returned.

        :param str xmlstring: The XML content returned from the session URL
        :return: None
        """
        xml = ET.fromstring(xmlstring)
        for item in xml:
            if item.get('type').find('servicelist') != -1:
                self.service_list_url = item.get('href')
                break

    def _parse_vcd_uuid(self, xmlstring):
        """
        Parse the vdc UUID from a direct vCD login session

        :param str xmlstring: POST response content from the vCD login session
        :return: None or UUID
        """
        session = ET.fromstring(xmlstring)
        for link in session:
            if link.get('type') and 'vcloud.org+xml' in link.get('type'):
                resp = requests.get(link.get('href'), headers=self.headers)
                check_http_response_error(resp)
                break
        else:
            raise RuntimeError('Could not locate Org UUID')

        org_data = ET.fromstring(resp.text)
        for link in org_data:
            if link.get('type') and 'vcloud.vdc+xml' in link.get('type'):
                #This assumes each Org will only have a single VDC, as is
                #currently (2016) the case within VPC and Dedicated Clouds
                return link.get('href')[-UUID_L:]
        else:
            raise RuntimeError('Could not locate VDC UUID')


    def _vcd_login(self, vcd_url, orgname):
        """
        Do login to vCD instance directly, bypassing vCA portal

        :param str vcd_url: vCD URL e.g: https://p1v17-vcd.vchs.vmware.com
        :param str orgname: Organization name
        :return:
        """
        auth_header = 'x-vcloud-authorization'
        self.headers['Accept'] = 'application/*+xml;version={}'.format(self.version)
        username = "{}@{}".format(self.username, orgname)
        resp = requests.post(vcd_url+'/api/sessions', headers=self.headers,
                             auth=(username,self.password))
        check_http_response_error(resp)
        self.headers[auth_header] = resp.headers.get(auth_header)
        uuid = self._parse_vcd_uuid(resp.text)
        del self.headers[auth_header]
        self.vcd_tokens[orgname] = {
            'auth-header': auth_header,
            'token': resp.headers.get(auth_header),
            'vcdurl': vcd_url,
            'version': self.version,
            'org_uuid': uuid
        }
        return self.vcd_tokens[orgname]

class VCAODSession:
    """
    This session class handles the newer on-demand architecture. Like the main
    session class, this can also handle multiple vCD login tokens.
    """
    _od_login_url = 'https://vca.vmware.com/api/iam/login'

    def __init__(self, version='5.7', username=None, password=None):
        """
        Used to create login sessions and On-Demand instance sessions within
        vCloud Air

        :param str version: Version of the API to interact with
        :param str username: vCA Username
        :param str password: vCA Password
        """
        self.version = str(version)
        self.instances = []
        self._plans = []
        self.vcd_tokens = {}
        self.username = username
        self.password = password
        self.vca_token = None

    def login(self, username=None, password=None):
        """
        Log into the On-Demand top-level system and generate a list of available
        instances.

        :param str username: vCA Username
        :param str password: vCA Password
        :return: ``None``
        """
        if username:
            self.username = username
        if not self.username:
            raise RuntimeError('No username specified')

        if password:
            self.password = password
        if not self.password:
            raise RuntimeError('No password specified')

        headers = {'Accept':'application/json;version={}'.format(self.version)}
        resp = requests.post(self._od_login_url, headers=headers,
                             auth=(self.username, self.password))
        check_http_response_error(resp)
        self.vca_token = resp.headers.get('vchs-authorization')
        self._get_instance_list()

    def login_to_instance(self, idx):
        """
        Log into a specific instance within the On-Demand infrastructure and
        issue an auth token that can be used for further operations

        :param int idx: Index of the instance in self.instances to log into
        :return: Login information for the session that was created
        :rtype: ``dict``
        """
        instance = self.instances[idx]
        headers = {'Accept': 'application/*+xml;version={}'.format(self.version)}
        try:
            url = instance['instanceAttributes']['sessionUri']
            username = self.username + '@' + instance['instanceAttributes']['orgName']
        except KeyError:
            raise RuntimeError('That instance does not have a session URI')

        resp = requests.post(url, headers=headers, auth=(username, self.password))
        check_http_response_error(resp)
        data = {'auth-header':'x-vcloud-authorization',
                'token':resp.headers.get('x-vcloud-authorization'),
                'vcdurl':instance['apiUrl'].split('api/org')[0],
                'org_uuid':instance['id'],
                'version':self.version}
        self.vcd_tokens[instance['id']] = data
        return data

    def show_instance_list(self):
        """
        Prints out the current list of OD instances and their indexes in a
        human-readable format

        :return: ``None``
        """
        fmt_string = "{:5} {:30} {:20}"
        print(fmt_string.format('Index', 'Type', 'Region'))
        for idx,val in enumerate(self.instances):
            print(fmt_string.format(str(idx),
                                    val['friendlyName'],
                                    val['region'].split('.')[0]))

    def _get_instance_list(self):
        """
        Retrieve the On-Demand instance list from the API

        :return: ``None``
        """
        url = 'https://vca.vmware.com/api/sc/instances'
        headers = {'Accept': 'application/json;version={}'.format(self.version),
                   'Authorization': 'Bearer {}'.format(self.vca_token)}
        resp = requests.get(url, headers=headers)
        check_http_response_error(resp)
        self.instances = resp.json()['instances']
        self._format_instance_list()

        #Get plans to match the friendly names
        resp = requests.get('https://vca.vmware.com/api/sc/plans',
                            headers=headers)
        check_http_response_error(resp)
        self._plans = resp.json()['plans']
        self.instances = list(filter(self._filter_instance_list, self.instances))
        self._match_friendly_names()

    def _filter_instance_list(self, instance):
        """
        Used to filter the instance list to only those instances that supply a
        VCD session token URL, which is used later by the actual login process.

        :param dict instance: An instance dict item from the instance list
        :return: True or False
        :rtype: ``bool``
        """
        try:
            instance['instanceAttributes']['sessionUri']
        except (KeyError, TypeError):
            return False
        return True

    def _format_instance_list(self):
        """
        Formats the instance list to convert the strings inside the attributes
        into proper JSON as the API sends them as escaped strings.

        :return: ``None``
        """
        for instance in self.instances:
            try:
                instance['instanceAttributes'] = json.loads(instance['instanceAttributes'])
            except (ValueError,KeyError):
                pass

    def _match_friendly_names(self):
        """
        Checks through the Plan data and finds the friendly name and plan type
        for each On-Demand instance. Inserts two new keys into each instance
        dictionary containing the type and friendly name.

        :return: ``None``
        """
        for instance in self.instances:
            for plan in self._plans:
                if plan.get('id') == instance.get('planId'):
                    instance['friendlyName'] = plan.get('name','Unnamed')
                    instance['planType'] = plan.get('planType','NoType')
