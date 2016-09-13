# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class PolicySetResult(Model):
    """Result of a policy set evaluation.

    :param has_error: A value indicating whether this policy set evaluation
     has discovered violations.
    :type has_error: bool
    :param policy_violations: The list of policy violations.
    :type policy_violations: list of :class:`PolicyViolation
     <azure.mgmt.devtestlabs.models.PolicyViolation>`
    """ 

    _attribute_map = {
        'has_error': {'key': 'hasError', 'type': 'bool'},
        'policy_violations': {'key': 'policyViolations', 'type': '[PolicyViolation]'},
    }

    def __init__(self, has_error=None, policy_violations=None):
        self.has_error = has_error
        self.policy_violations = policy_violations
