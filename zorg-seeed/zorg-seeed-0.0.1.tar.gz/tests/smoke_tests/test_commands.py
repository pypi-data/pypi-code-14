from unittest import TestCase
from zorg_seeed import MotorShield


class SmokeTestCase(TestCase):

    def setUp(self):
        self.connection = None
        self.options = {}


class MotorShieldSmokeTests(SmokeTestCase):

    def test_command_method_exists(self):
        """
        Check that each command listed has a corresponding
        method on the driver class.
        """
        motor_shield = MotorShield(self.options, self.connection)

        for command in motor_shield.commands:
            self.assertIn(command, dir(motor_shield))
