# coding=utf-8
"""
vCloud Air Metrics
==================

Metrics are available via the hybridity API (as of 2016) for the two current
subscription offerings: Dedicated Clouds and Virtual Private Clouds. This
module allows querying of metrics and also filtering by only the metrics the
programmer wants to see.

Metrics are retained for a 24-hour period server-side at the time of writing.
For more information about the metrics API, please see the following
documentation: https://pubs.vmware.com/vca/topic/com.vmware.vca.metrics.api.doc/GUID-95D137D6-04A7-4BB6-90A7-70B132343CBB.html

"""

__author__ = 'Scott Schaefer'

import requests
from urllib.parse import urljoin
from .util import check_http_response_error

class Metrics:
    """
    The metics class allows for metric retrieval against VMs or VDCs. Metrics
    do exist for NSX edges but this class doesn't retrieve those. Also, when
    retrieving a VDC, the returned metrics are for all of the VMs within that
    VDC.
    """
    _baseurl = "hybridity/api/metrics/"

    def __init__(self, org_info=None, vcdurl=None, token=None,
                 org_uuid=None, vm_uuids=None):
        """
        Create a metrics instance to query the vCA Metrics API.
        Either a VDC or list of VMs can be queried by one instance. NOT BOTH!

        :param dict org_info: Dictionary containing org login data
        :param str vcdurl: Base URL for vCD instance
        :param str token: vCD authentication token
        :param str org_uuid: UUID for the VDC to query
        :param list vm_uuids: List of VM UUIDs to query
        """
        org_info = {} if org_info is None else org_info
        if not all((org_info.get('vcdurl',vcdurl),org_info.get('token',token))):
            raise RuntimeError("Missing required parameter, VCDURL or Token")

        self.postdata = {'relativeStartTime': {'interval':5,
                                               'unit':'MINUTE'}}
        self.headers = {'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        'x-vcloud-authorization': org_info.get('token', token)}
        self.url = urljoin(org_info.get('vcdurl', vcdurl), self._baseurl)
        self.filters = []
        self.metric_data = {}
        self.vms = []
        org_uuid = org_info.get('org_uuid', org_uuid)
        if vm_uuids:
            self.url = urljoin(self.url, 'vApp/')
            self.vms.extend(vm_uuids)
        else:
            self.url = urljoin(self.url, 'vdc/{}'.format(org_uuid))

    def set_relative_interval(self, units, start, end=None):
        """
        Sets the interval for which to collect metrics. This is a relative (aka,
        N minutes/hours AGO) rather than time window specific date.

        :param str units: Duration units (MINUTE, HOUR, SECOND)
        :param int start: Number of <unit> ago to begin collecting at
        :param int end: Number of <unit> ago to end collecting at
        :return: ``None``
        """
        units = units.upper()
        if units not in ['HOUR', 'MINUTE', 'SECOND']:
            raise RuntimeError('Invalid unit selected: Must be HOUR, MINUTE, '
                               'SECOND')
        self.postdata['relativeStartTime'] = {'interval': int(start),
                                              'unit': units}
        if end:
            self.postdata['relativeEndTime'] = {'interval': int(end),
                                                'unit': units}

    def set_absolute_interval(self, start, end):
        """
        Not implemented at this time.

        :param start:
        :param end:
        :return:
        """
        raise NotImplementedError()

    def set_metric_filters(self, *filters):
        """
        Sets the list of specific metrics to pull out of the returned JSON
        results.

        :param str filters: The names of the specific filters
        :return: ``None``
        """
        self.filters = [x for x in filters]

    def add_metric_filters(self, *filters):
        """
        Adds additional filters to the existing list of filters.

        :param str filters: The names of the specific filters to add
        :return: ``None``
        """
        self.filters.extend([x for x in filters])

    def collect(self):
        """
        Initiate the data collection from the metrics API

        :return: ``None``
        """
        if len(self.vms):
            for vm in self.vms:
                url = urljoin(self.url, 'vm-{}'.format(vm))
                self._do_collect(url)
        else:
            self._do_collect(self.url)

    def _do_collect(self, url):
        """
        Internal function to handle the main collection routine. Called with
        data depending on whether VMs or a VDC is selected

        :param str url: The full URL string to query the metrics API endpoint
        :return: ``None``
        """
        nextpage = params = None
        while True:
            if nextpage:
                params = {'next': nextpage}
            resp = requests.post(url, headers=self.headers, json=self.postdata,
                                 params=params)
            check_http_response_error(resp)
            data = resp.json()
            self._format_data(data)
            nextpage = data.get('next')
            if nextpage is None:
                break

    def _format_data(self, data):
        """
        Pull out the relevant JSON data and format it into the local metrics
        datastructure.

        :param dict data: JSON data from the API call
        :return: ``None``
        """
        for row in data['rows']:
            mets = {m['name']: m['value'] for m in row['metrics']}
            vm = self.metric_data.setdefault(row['vmId'], {})
            ts = vm.setdefault(row['timestamp'], {})
            if len(self.filters):
                for m_filter in self.filters:
                        ts[m_filter] = mets.get(m_filter, 'Invalid Metric Name')
            else:
                #No filters, grab everything
                for m_name, m_value in mets.items():
                    ts[m_name] = m_value
