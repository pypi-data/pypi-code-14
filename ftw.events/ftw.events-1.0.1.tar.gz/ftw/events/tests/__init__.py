from ftw.events.testing import FUNCTIONAL_TESTING
from ftw.events.testing import FUNCTIONAL_ZSERVER_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest2 import TestCase
import transaction


class FunctionalTestCase(TestCase):
    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def grant(self, *roles):
        setRoles(self.portal, TEST_USER_ID, list(roles))
        transaction.commit()


class RealFuncitionalTestCase(FunctionalTestCase):
    layer = FUNCTIONAL_ZSERVER_TESTING
