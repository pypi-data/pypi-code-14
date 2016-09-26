#!/usr/bin/env python
# coding: utf-8


from opsviewclient.v2.client import Client as ClientV2


def Client(*args, **kwds):
    """Version is currently ignored but may be used in future releases if
    API versioning is implemented in this library.
    """
    return ClientV2(*args, **kwds)
