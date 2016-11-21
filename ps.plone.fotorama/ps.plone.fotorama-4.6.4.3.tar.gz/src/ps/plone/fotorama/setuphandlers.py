# -*- coding: utf-8 -*-
"""Post install import steps for ps.plone.fotorama."""

# zope imports
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'ps.plone.fotorama:install-base',
            'ps.plone.fotorama:uninstall',
            'ps.plone.fotorama:uninstall-base',
        ]
