__author__ = 'Inga'
from cloudshell.networking.cisco.cisco_handler_base import CiscoHandlerBase
from cloudshell.shell.core.context_utils import get_resource_name
from cloudshell.networking.networking_utils import *
from collections import OrderedDict


class CiscoIOSXRHandler(CiscoHandlerBase):
    def __init__(self):
        CiscoHandlerBase.__init__(self)
        self.supported_os = ['IOS-XR', 'IOS XR', 'IOSXR']




