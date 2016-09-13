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


class Version(Model):
    """A multipart-numeric version number.

    :param major: the leftmost number of the version
    :type major: int
    :param minor: the second leftmost number of the version
    :type minor: int
    :param build: the third number of the version
    :type build: int
    :param revision: the fourth number of the version
    :type revision: int
    :param major_revision: the MSW of the fourth part
    :type major_revision: int
    :param minor_revision: the LSW of the fourth part
    :type minor_revision: int
    """ 

    _attribute_map = {
        'major': {'key': 'major', 'type': 'int'},
        'minor': {'key': 'minor', 'type': 'int'},
        'build': {'key': 'build', 'type': 'int'},
        'revision': {'key': 'revision', 'type': 'int'},
        'major_revision': {'key': 'majorRevision', 'type': 'int'},
        'minor_revision': {'key': 'minorRevision', 'type': 'int'},
    }

    def __init__(self, major=None, minor=None, build=None, revision=None, major_revision=None, minor_revision=None):
        self.major = major
        self.minor = minor
        self.build = build
        self.revision = revision
        self.major_revision = major_revision
        self.minor_revision = minor_revision
