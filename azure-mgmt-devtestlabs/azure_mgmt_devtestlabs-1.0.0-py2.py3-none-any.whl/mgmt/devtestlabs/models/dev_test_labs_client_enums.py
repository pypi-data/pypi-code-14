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

from enum import Enum


class SourceControlType(Enum):

    vso_git = "VsoGit"
    git_hub = "GitHub"


class EnableStatus(Enum):

    enabled = "Enabled"
    disabled = "Disabled"


class LabCostType(Enum):

    unavailable = "Unavailable"
    reported = "Reported"
    projected = "Projected"


class WindowsOsState(Enum):

    non_sysprepped = "NonSysprepped"
    sysprep_requested = "SysprepRequested"
    sysprep_applied = "SysprepApplied"


class LinuxOsState(Enum):

    non_deprovisioned = "NonDeprovisioned"
    deprovision_requested = "DeprovisionRequested"
    deprovision_applied = "DeprovisionApplied"


class CustomImageOsType(Enum):

    windows = "Windows"
    linux = "Linux"
    none = "None"


class LabStorageType(Enum):

    standard = "Standard"
    premium = "Premium"


class PolicyStatus(Enum):

    enabled = "Enabled"
    disabled = "Disabled"


class PolicyFactName(Enum):

    user_owned_lab_vm_count = "UserOwnedLabVmCount"
    lab_vm_count = "LabVmCount"
    lab_vm_size = "LabVmSize"
    gallery_image = "GalleryImage"
    user_owned_lab_vm_count_in_subnet = "UserOwnedLabVmCountInSubnet"


class PolicyEvaluatorType(Enum):

    allowed_values_policy = "AllowedValuesPolicy"
    max_value_policy = "MaxValuePolicy"


class UsagePermissionType(Enum):

    default = "Default"
    deny = "Deny"
    allow = "Allow"


class SubscriptionNotificationState(Enum):

    not_defined = "NotDefined"
    registered = "Registered"
    unregistered = "Unregistered"
    warned = "Warned"
    suspended = "Suspended"
    deleted = "Deleted"
