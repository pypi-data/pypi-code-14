# coding=utf-8
"""
vCloud Air Python SDK Package
=============================

A lightweight SDK for vCloud Air. Currently not meant to handle exhaustive
operations against VMs, vDCs, edges, etc, but only some of the more common
operations.

This is aimed more towards using newer APIs (ANS, metrics, etc) than classic
(vCD) APIs, as those are far more heavy due to the use of XML.

"""

__title__ = 'vcloudair'
__version__ = '0.5'
__author__ = 'Scott Schaefer'
__license__ = 'MIT'
__copyright__ = 'Copyright 2016 Scott Schaefer'

from .session import VCASession, VCAODSession
from .metrics import Metrics
from .query import (VMQuery,
                    EdgeGatewayQuery,
                    VAppQuery,
                    VAppTemplateQuery,
                    OrgVdcQuery)
from .ans import ANSFirewall, ANSNat, ANSIPSec
from .dr import DisasterRecovery
