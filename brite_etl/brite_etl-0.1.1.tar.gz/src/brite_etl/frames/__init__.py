"""
.. py:module:: brite_etl.frames

This is where frames are stored.

Each frame inherits from the base :class:`brite_etl.abstracts.Frame`.

Each frame class is imported into the ``brite_etl.frames`` namespace,
so while you can do ``from brite_etl.frames.claims import Claims``,
you can also do ``from brite_etl.frames import Claims``.

Prepared frames can be accessed in the :mod:`brite_etl.frames.prepared <brite_etl.frames.prepared>` submodule.
"""

# flake8: noqa
from __future__ import division, absolute_import, print_function

#
# For various reasons I decided against dynamic importing
#
# def all_frames(include_prepared=False, path_only=False):
#     _frames = []
#     import os, sys, importlib, inspect
#     dirlist = sorted(os.listdir(os.path.dirname(__file__)))
#     import_files = [d for d in dirlist if d.endswith('.py') and not d.startswith('__init__')]
#
#     for d in import_files:
#         module = importlib.import_module(
#             'brite_etl.frames.{0}'.format(d.replace('.py', ''))
#         )
#
#         for name, obj in inspect.getmembers(module):
#             if inspect.isclass(obj) and name != 'Frame':
#                 if not path_only:
#                     _frames.append(obj)
#                 else:
#                     _frames.append('brite_etl.frames.{0}'.format(d.replace('.py', '')))
#
#     if include_prepared:
#         from .prepared import all_frames as all_prepared_frames
#         _frames.extend(all_prepared_frames(path_only))
#
#     return _frames

from . import prepared

from .account_history import AccountHistory
from .additional_interests import AdditionalInterests
from .addresses import Addresses
from .agencies import Agencies
from .builder_obj import BuilderObj
from .builder_obj_parsed import BuilderObjParsed
from .catastrophes import Catastrophes
from .claim_items import ClaimItems
from .claims import Claims
from .claims_changes import ClaimsChanges
from .claims_contacts import ClaimsContacts
from .claims_payments import ClaimsPayments
from .claims_payments_item_amounts import ClaimsPaymentsItemAmounts
from .claims_perils import ClaimsPerils
from .claims_recoveries import ClaimsRecoveries
from .commission_accounting import CommissionAccounting
from .commission_payments import CommissionPayments
from .committed_revisions import CommittedRevisions
from .committed_revisions_all import CommittedRevisionsAll
from .credit_reports import CreditReports
from .custom_data import CustomData
from .emails import Emails
from .files import Files
from .inactive_claims import InactiveClaims
from .inspectors import Inspectors
from .item_questions import ItemQuestions
from .lines import Lines
from .losses_incurred import LossesIncurred
from .losses_incurred_items import LossesIncurredItems
from .mortgagees import Mortgagees
from .phones import Phones
from .policies import Policies
from .policy_change_log import PolicyChangeLog
from .policy_payments import PolicyPayments
from .policy_terms import PolicyTerms
from .policy_types import PolicyTypes
from .policyholders import Policyholders
from .premium_records import PremiumRecords
from .properties import Properties
from .property_items import PropertyItems
from .quotes import Quotes
from .quoting_revisions import QuotingRevisions
from .recovery_history import RecoveryHistory
from .recovery_history_snapshot import RecoveryHistorySnapshot
from .return_premiums import ReturnPremiums
from .revision_items import RevisionItems
from .revisions import Revisions
from .x_report_locations import XReportLocations

__all__ = (
    'AccountHistory',
    'AdditionalInterests',
    'Addresses',
    'Agencies',
    'BuilderObj',
    'BuilderObjParsed',
    'Catastrophes',
    'ClaimItems',
    'Claims',
    'ClaimsChanges',
    'ClaimsContacts',
    'ClaimsPayments',
    'ClaimsPaymentsItemAmounts',
    'ClaimsPerils',
    'ClaimsRecoveries',
    'CommissionAccounting',
    'CommissionPayments',
    'CommittedRevisions',
    'CommittedRevisionsAll',
    'CreditReports',
    'CustomData',
    'Emails',
    'Files',
    'InactiveClaims',
    'Inspectors',
    'ItemQuestions',
    'Lines',
    'LossesIncurred',
    'LossesIncurredItems',
    'Mortgagees',
    'Phones',
    'Policies',
    'PolicyChangeLog',
    'PolicyPayments',
    'PolicyTerms',
    'PolicyTypes',
    'Policyholders',
    'PremiumRecords',
    'Properties',
    'PropertyItems',
    'Quotes',
    'QuotingRevisions',
    'RecoveryHistory',
    'RecoveryHistorySnapshot',
    'ReturnPremiums',
    'RevisionItems',
    'Revisions',
    'XReportLocations'
)
