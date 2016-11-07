# -*- coding: utf-8 -*-

from Products.CMFPlone import interfaces as plone_interfaces
from Products.CMFQuickInstallerTool import interfaces as qi_interfaces
from zope.interface import implementer

PROJECTNAME = 'brasil.gov.portlets'


@implementer(qi_interfaces.INonInstallable)
class HiddenProducts(object):

    def getNonInstallableProducts(self):
        return [
            u'brasil.gov.portlets.upgrades.v1000',
            u'brasil.gov.portlets.upgrades.v1001',
            u'brasil.gov.portlets.upgrades.v1002',
        ]


@implementer(plone_interfaces.INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        return [
            u'brasil.gov.portlets:uninstall',
            u'brasil.gov.portlets:testfixture',
            u'brasil.gov.portlets.upgrades.v1000:default',
            u'brasil.gov.portlets.upgrades.v1001:default',
            u'brasil.gov.portlets.upgrades.v1002:default',
        ]
