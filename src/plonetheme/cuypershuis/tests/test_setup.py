# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plonetheme.cuypershuis.testing import PLONETHEME_MODERNBASE_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that plonetheme.cuypershuis is properly installed."""

    layer = PLONETHEME_MODERNBASE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if plonetheme.cuypershuis is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'plonetheme.cuypershuis'))

    def test_browserlayer(self):
        """Test that IPlonethemecuypershuisLayer is registered."""
        from plonetheme.cuypershuis.interfaces import (
            IPlonethemeModernBaseLayer)
        from plone.browserlayer import utils
        self.assertIn(IPlonethemeModernBaseLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = PLONETHEME_MODERNBASE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['plonetheme.cuypershuis'])

    def test_product_uninstalled(self):
        """Test if plonetheme.cuypershuis is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'plonetheme.cuypershuis'))

    def test_browserlayer_removed(self):
        """Test that IPlonethemecuypershuisLayer is removed."""
        from plonetheme.cuypershuis.interfaces import IPlonethemeModernBaseLayer
        from plone.browserlayer import utils
        self.assertNotIn(IPlonethemeModernBaseLayer, utils.registered_layers())
