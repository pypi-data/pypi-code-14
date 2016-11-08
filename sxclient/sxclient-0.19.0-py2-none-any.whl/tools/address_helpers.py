'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

from __future__ import unicode_literals

from typing import List  # noqa

import socket

__all__ = ['get_addresses']


def get_addresses(host):
    # type: (str) -> List[str]
    '''For a given host, obtain its IP addresses.'''
    info = socket.getaddrinfo(host, None, 0, 0, socket.IPPROTO_TCP)
    addresses = [elt[4][0] for elt in info]
    return addresses
