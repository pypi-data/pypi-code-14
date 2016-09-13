import unittest

from stateutil import switch

__author__ = u'Hywel Thomas'
__copyright__ = u'Copyright (C) 2016 Hywel Thomas'


class TestSwitch(unittest.TestCase):

    def setUp(self):
        self.sw = switch.Switch(switch.Switch.ON)

    def tearDown(self):
        pass

    def test_switch_on(self):
        self.assertTrue(self.sw.ON)

    def test_switch_off(self):
        self.assertFalse(self.sw.OFF)

    def test_state_on(self):

        self.sw.on()
        state = self.sw.state

        self.assertEqual(self.sw.ON, state, msg=u'Failed to switch on')

    def test_state_off(self):

        self.sw.off()
        state = self.sw.state

        self.assertEqual(self.sw.OFF, state, msg=u'Failed to switch off')


if __name__ == u'__main__':
    unittest.main()
