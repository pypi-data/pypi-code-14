from zorg.driver import Driver


class MotorShield(Driver):
    """
    Driver for the Seeed Motor Shield.
    """

    def __init__(self, options, connection):
        super(MotorShield, self).__init__(options, connection)

        self.pins = {
            'right_motor_speed': 10,
            'right_motor': [12, 13],
            'left_motor_speed': 9,
            'left_motor': [8, 11]
        }

        self.right_motor_speed = 0
        self.left_motor_speed = 0

        self.commands += [
            'set_right_motor_speed',
            'get_right_motor_speed',
            'set_right_motor_direction',
            'set_left_motor_speed',
            'get_left_motor_speed',
            'set_left_motor_direction'
        ]

    def set_right_motor_speed(self, speed):
        """
        Set the speed of the right side motor.
        Speed should be an integer 0 to 255.
        """
        self.right_motor_speed = speed
        self.connection.pwm_write(
            self.pins['right_motor_speed'],
            speed
        )

    def get_right_motor_speed(self):
        return self.right_motor_speed

    def set_right_motor_direction(self, direction):
        """
        Takes a 0 or a 1 value to set the motor direction
        clockwise or counter-clockwise.
        """
        if direction == 0:
            # Set the motor direction clockwise
            self.connection.digital_write(self.pins['right_motor'][0], 0)
            self.connection.digital_write(self.pins['right_motor'][1], 1)
        elif direction == 1:
            # Set the motor direction counter-clockwise
            self.connection.digital_write(self.pins['right_motor'][0], 1)
            self.connection.digital_write(self.pins['right_motor'][1], 0)
        else:
            # Stop the motor
            self.connection.digital_write(self.pins['right_motor'][0], 0)
            self.connection.digital_write(self.pins['right_motor'][1], 0)

    def set_left_motor_speed(self, speed):
        """
        Set the speed of the left side motor.
        Speed should be an integer 0 to 255.
        """
        self.left_motor_speed = speed
        self.connection.pwm_write(
            self.pins['left_motor_speed'],
            speed
        )

    def get_left_motor_speed(self):
        return self.left_motor_speed

    def set_left_motor_direction(self, direction):
        """
        Takes a 0 or a 1 value to set the motor direction
        clockwise or counter-clockwise.
        """
        if direction == 0:
            # Set the motor direction clockwise
            self.connection.digital_write(self.pins['left_motor'][0], 0)
            self.connection.digital_write(self.pins['left_motor'][1], 1)
        elif direction == 1:
            # Set the motor direction counter-clockwise
            self.connection.digital_write(self.pins['left_motor'][0], 1)
            self.connection.digital_write(self.pins['left_motor'][1], 0)
        else:
            # Stop the motor
            self.connection.digital_write(self.pins['left_motor'][0], 0)
            self.connection.digital_write(self.pins['left_motor'][1], 0)

