# coding=utf-8
"""
vCloud Air vCloud Director Queries
==================================

The query classes inherit from the base class which is used to return data
from vCloud Director's query API. The subclasses are for convenience when
querying common vCD types.

An instance of the base class can be instantiated and manipulated manually in
order to query more specific objects. A manual call to add the 'type' key to
the instance variable "params" as well as changing the instance variable
"record_name" to a matching query type will facilitate querying anything from
the query API.

See the vCD API schema or documentation for additional query and type
information.

"""

__author__ = 'Scott Schaefer'

import requests
import xml.etree.ElementTree as ET
from urllib.parse import urljoin
from .util import check_http_response_error, UUID_L

query_record_types = {'vm':'VMRecord',
                      'edgeGateway': 'EdgeGatewayRecord',
                      'vApp': 'VAppRecord',
                      'vAppTemplate': 'VAppTemplateRecord',
                      'orgVdc': 'OrgVdcRecord'}

class QueryBase:
    """
    This is the base class for vCD queries. It can be instantiated on its own
    but some additional configuration will need to happen to get it to actually
    return query results.

    Manipulating the  ``params`` dictionary will dictate how the results are
    returned and for what type of record. The inheriting query classes are
    simply shortcuts for those changes.
    """
    _nsmap = {'vcd':'http://www.vmware.com/vcloud/v1.5'}

    def __init__(self, org_info=None, version=None, vcdurl=None, token=None):
        """
        Base query class for using the query API within vCloud Director. There
        are child classes which are helper classes to make querying specific
        objects easier.

        :param dict org_info: Dictionary containing org login data
        :param str version: API version string, e.g: '5.6'
        :param str vcdurl: vCD base URL
        :param str token: vCD authorization token
        """
        org_info = {} if org_info is None else org_info
        if not all([org_info.get('version', version),
                    org_info.get('vcdurl', vcdurl),
                    org_info.get('token', token)]):
            raise RuntimeError('Missing required parameter: version, '
                               'vcdurl, or token')

        version = org_info.get('version', version)
        self.headers = {'Accept': 'application/*+xml;version={}'.format(version),
                        'x-vcloud-authorization': org_info.get('token', token)}
        self.params = {'pageSize': 100,
                       'format': 'records',
                       'page': 1}
        self.url = urljoin(org_info.get('vcdurl', vcdurl), 'api/query')
        self.record_name = ''
        self.fields = {'name'}
        self.results = {}

    def set_fields(self, *fields):
        """
        The fields to be returned in each query record. Refer to vCD
        documentation for the list of fields available to each query type.

        :param fields: Field names to be concatenated into the fields parameter
        :return: ``None``
        """
        fields = list(fields)
        fields.append('name')
        self.fields = fields = set(fields)
        self.params['fields'] = ','.join(fields)

    def set_query_type(self, qtype):
        """
        Sets the type of the query, e.g: vm, edge, vapp, etc. Check vCD
        documentation for available types.

        :param str qtype: Query type to be appended to query
        :return: ``None``
        """
        try:
            self.record_name = query_record_types[qtype]
        except KeyError:
            msg = 'Invalid or Not Implemented query type.\n' \
                  'Available types are: {} (case-sensitive)'\
                .format(', '.join(query_record_types.keys()))
            raise RuntimeError(msg)
        self.params['type'] = qtype

    def execute(self):
        """
        Executes the query by sending a web request to the vCD API

        :return: Query results in dict format instead of XML
        :rtype: dict
        """
        self.results = {}
        page = 1
        while page > 0:
            resp = requests.get(self.url, params=self.params,
                                headers=self.headers)
            check_http_response_error(resp)
            xmldata = ET.fromstring(resp.text)
            self._parse_results(xmldata)
            if self._find_next_page(xmldata):
                page += 1
                self.params['page'] = page
            else:
                page = 0
        self.params['page'] = 1
        return self.results

    def find_by_name(self, name):
        """
        Search the query results by friendly name and return a list of UUIDs
        that contain the matching name attribute. Since name is not unique,
        there may be multiple results.

        :param str name: The friendly name of the object
        :return: Resulting UUIDs
        :rtype: list
        """
        matches = []
        name = name.lower()
        for uuid,fields in self.results.items():
            if fields['name'].lower() == name:
                matches.append(uuid)
        return matches

    def _parse_results(self, xmldata):
        """
        Parse the XML records into a dict and pull out the fields that were
        set for the query

        :param xmldata: Elementree XML element
        :return: Parsed data
        """
        recordname = 'vcd:{}'.format(self.record_name)
        for record in xmldata.findall(recordname, self._nsmap):
            uuid = record.get('href')[-UUID_L:]
            item = self.results.setdefault(uuid.lower(), {})
            for field in self.fields:
                item[field] = record.get(field)

    def _find_next_page(self, xmldata):
        """
        Parse through the XML to locate a next page link. If a link is found
        just return true

        :param xmldata: XML API data from vCD
        :return: True if a next page relation is found, otherwise false
        :rtype: bool
        """
        for link in xmldata.findall('vcd:Link', self._nsmap):
            if link.get('rel') == 'nextPage':
                return True
        else:
            return False

class VMQuery(QueryBase):
    """
    The query results will be VM records when using this class.
    """
    def __init__(self, org_info=None, version=None, vcdurl=None, token=None):
        super().__init__(org_info, version, vcdurl, token)
        self.set_query_type('vm')

class EdgeGatewayQuery(QueryBase):
    """
    The query results will be Edge records when using this class.
    """
    def __init__(self, org_info=None, version=None, vcdurl=None, token=None):
        super().__init__(org_info, version, vcdurl, token)
        self.set_query_type('edgeGateway')

class VAppQuery(QueryBase):
    """
    The query results will be vApp records when using this class.
    """
    def __init__(self, org_info=None, version=None, vcdurl=None, token=None):
        super().__init__(org_info, version, vcdurl, token)
        self.set_query_type('vApp')

class VAppTemplateQuery(QueryBase):
    """
    The query results will be vApp Template records when using this class.
    """
    def __init__(self, org_info=None, version=None, vcdurl=None, token=None):
        super().__init__(org_info, version, vcdurl, token)
        self.set_query_type('vAppTemplate')

class OrgVdcQuery(QueryBase):
    """
    The query results will be OrgVDC records when using this class.
    """
    def __init__(self, org_info=None, version=None, vcdurl=None, token=None):
        super().__init__(org_info, version, vcdurl, token)
        self.set_query_type('orgVdc')
