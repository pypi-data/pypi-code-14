# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from lineage.controlpanels.testing import LINEAGE_CONTROLPANELS_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that lineage.controlpanels is properly installed."""

    layer = LINEAGE_CONTROLPANELS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if lineage.controlpanels is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'lineage.controlpanels'))

    def test_browserlayer(self):
        """Test that IBrowserLayer is registered."""
        from lineage.controlpanels.interfaces import IBrowserLayer
        from plone.browserlayer import utils
        self.assertIn(IBrowserLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = LINEAGE_CONTROLPANELS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['lineage.controlpanels'])

    def test_product_uninstalled(self):
        """Test if lineage.controlpanels is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'lineage.controlpanels'))

    def test_browserlayer_removed(self):
        """Test that IBrowserLayer is removed."""
        from lineage.controlpanels.interfaces import IBrowserLayer
        from plone.browserlayer import utils
        self.assertNotIn(IBrowserLayer, utils.registered_layers())
