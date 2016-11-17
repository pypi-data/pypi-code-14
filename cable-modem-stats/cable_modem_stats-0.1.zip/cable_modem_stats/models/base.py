# -*- coding: utf-8 -*-
"""
Defines the BaseModem class that all other Modem classes should subclass.

Created by phillip on 11/16/2016
"""

import bs4
import re
import requests
import six


class MetaModem(type):
    """
    Keeps track of all classes that have subclassed BaseModem. To add a new model, all you have to do is
    subclass BaseModem and it will be added to the registry here for identifying it.
    """
    KNOWN_MODELS = {}

    def __init__(cls, name, bases=None, namespace=None):
        super(MetaModem, cls).__init__(name, bases, namespace)
        name = cls.__name__
        if name not in MetaModem.KNOWN_MODELS and name[0] != '_' and name not in {'BaseModem', 'UnknownModem'}:
            MetaModem.KNOWN_MODELS[name] = cls


@six.add_metaclass(MetaModem)
class BaseModem(object):
    """
    Base class to all Modem classes. To add a custom modem, just subclass this and implement the attributes you want.
    """
    def __init__(self, host_or_ip):
        """
        Not the best way to create a new modem. See `BaseModem.modem_from_address` instead.

        :param host_or_ip: the IP or hostname of this modem.
        """
        if not host_or_ip.startswith(('http://', 'https://')):
            host_or_ip = "http://%s" % host_or_ip
        self.host = host_or_ip

    @classmethod
    def modem_from_address(cls, host_or_ip):
        """
        Given a hostname or IP address, identify the modem model and return the class for it.

        :param host_or_ip: the host or IP address of the modem you want stats for
        :return: `UnknownModem` if the model is unrecognized, otherwise the specific Modem class for your modem
        """
        if not host_or_ip.startswith(('http://', 'https://')):
            host_or_ip = 'http://%s' % host_or_ip
        session = requests.session()
        response = session.get(host_or_ip)
        soup = bs4.BeautifulSoup(response.text.lower(), 'html.parser')
        # we're looking for a special tag in the HTML that makes
        # the browser refresh to a new location (basically a 301 redirect)
        refresh_tag = soup.find('meta', attrs={'http-equiv': 'refresh'})
        if refresh_tag:
            match = re.search(r'url=(.+)$', refresh_tag['content'])
            destination = match.group(1)
            response = session.get("%s%s" % (host_or_ip, destination))

        for typename, modem_type in MetaModem.KNOWN_MODELS.items():
            if modem_type.is_modem_type(response):
                model = modem_type
                break
        else:
            model = UnknownModem
        return model(host_or_ip)

    @classmethod
    def is_modem_type(cls, http_response):
        raise NotImplementedError()

    @property
    def downstreams(self):
        raise NotImplementedError()

    @property
    def upstreams(self):
        raise NotImplementedError()

    def get_downstream(self, name):
        raise NotImplementedError

    def get_upstream(self, name):
        raise NotImplementedError()

    def __str__(self):
        return "%s Modem at %s" % (self.__class__.__name__, self.host)


class UnknownModem(BaseModem):
    """
    Returned by modem_from_address when the Modem could not be identified.
    """
    pass


def connect(ip_or_host):
    """
    A convenience function for easily getting stats from a modem right away.

    :param ip_or_host: the hostname or IP address of the modem you want stats for
    :return: a Modem class with stats about the modem at this address
    """
    return BaseModem.modem_from_address(ip_or_host)
