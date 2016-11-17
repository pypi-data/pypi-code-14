# -*- coding: utf-8 -*-
"""
Arris modem classes

Created by phillip on 11/16/2016
"""

from __future__ import unicode_literals

from . import BaseModem
from ..stats.streams import Downstream, Upstream

from bs4 import BeautifulSoup
import requests
from six.moves.urllib.parse import urlparse


class _ArrisModem(BaseModem):
    """
    Base for other Arris-brand modems
    """
    @classmethod
    def is_modem_type(cls, http_response):
        if 'ARRIS' not in http_response.text:
            return False
        return True


class ArrisDG1670(_ArrisModem):
    """
    Arris DG1670 Cable Modem
    """
    STATUS_PAGE = '/cgi-bin/status_cgi'
    VERSION_PAGE = '/cgi-bin/vers_cgi'
    STREAM_TABLE_MAP = {
        '': 'name',
        'DCID': 'cid',
        'Freq': 'freq',
        'Power': 'power',
        'SNR': 'snr',
        'Modulation': 'modulation',
        'Octets': 'octets',
        'Correcteds': 'correcteds',
        'Uncorrectables': 'uncorrectables',
        'UCID': 'cid',
        'Channel Type': 'channel_type',
        'Symbol Rate': 'symbol_rate',
    }

    def __init__(self, host_or_ip, auto_refresh=True):
        super(self.__class__, self).__init__(host_or_ip)
        self._session = requests.session()
        self._upstreams = None
        self._downstreams = None
        self.auto_refresh = auto_refresh

    @property
    def downstreams(self):
        html = self._get_status_page()
        downstreams = self._parse_downstream_table(html)
        return downstreams

    @property
    def upstreams(self):
        html = self._get_status_page()
        upstreams = self._parse_upstream_table(html)
        return upstreams

    def get_downstream(self, name):
        raise NotImplementedError

    def get_upstream(self, name):
        raise NotImplementedError()

    def _get_status_page(self):
        response = self._session.get('%s%s' % (self.host, self.STATUS_PAGE))
        if response.status_code != 200:
            raise ValueError("Received an error response code from %s" % self.host)
        html = response.text
        return html

    @classmethod
    def _parse_downstream_table(cls, html):
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('td', text='DCID').find_parent('table')
        return cls._convert_table_to_objects(table, Downstream)

    @classmethod
    def _parse_upstream_table(cls, html):
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('td', text='UCID').find_parent('table')
        return cls._convert_table_to_objects(table, Upstream)

    @classmethod
    def _convert_table_to_objects(cls, table, stream_class):
        streams = []
        rows = [row for row in table.find_all('tr')]
        header_row = rows.pop(0)
        headers = [td.text for td in header_row.find_all('td')]  # get the column headers for the downstream table

        # map column headers to Stream object attributes and position on table
        indexes = {}
        for idx, column_header in enumerate(headers):
            # if we can map this column header to an attribute on a Stream object, add it to our indexes dict
            attr = cls.STREAM_TABLE_MAP.get(column_header)
            if attr:
                indexes[idx] = attr

        # for each row, use indexes to get each column attribute and put it in the Stream object
        for row in rows:
            cells = [td.text for td in row.find_all('td')]
            stream_dict = {attr: cells[idx] for idx, attr in indexes.items()}
            streams.append(stream_class(**stream_dict))

        return streams


    @classmethod
    def is_modem_type(cls, http_response):
        if not _ArrisModem.is_modem_type(http_response):
            return False
        parsed = urlparse(http_response.url)
        url = "%s://%s/%s" % (parsed.scheme, parsed.netloc, cls.VERSION_PAGE)
        response = requests.get(url)
        return 'MODEL: DG1670' in response.text
