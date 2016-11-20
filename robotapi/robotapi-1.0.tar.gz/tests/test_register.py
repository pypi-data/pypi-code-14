import sys
import os
import unittest
import mock

module_path = os.path.dirname(os.path.curdir + "." + os.path.sep)
sys.path.insert(0, os.path.abspath(module_path + "/source"))

from serial_connection import serial_port_connection
from roboapi import Atmega, Buzzer, Motion


# An object of Atmega class for testing ##
Test_object = Atmega(9600)


class Testconfigreg(unittest.TestCase):

    @mock.patch('serial_connection.serial.Serial')
    @mock.patch('serial_connection.glob')
    def setUp(self, mock_glob, mock_serial_port):
        """ setting up a dummy serial port object
        """
        self.portdetect = ['ttyUSB0', 'ttyUSB1']
        self.baudrate = 9600
        mock_glob('ttyUSB0')
        self.port = serial_port_connection(self.portdetect,
                                           baudrate=self.baudrate)

    def tearDown(self):
        """closing the dummy serial port
        """
        self.port.close()

    def test_configreg_raises_exceptions(self):
        """checking exception raised for invalid
        port name or pin Number
        """
        self.assertRaises(ValueError, Test_object.config_register,
                          'DDRJ', Pins=[1, 2, 8], set_pins=True)
        self.assertRaises(ValueError, Test_object.config_register,
                          'DDRZ', Pins=[1, 2, 8], set_pins=True)
        self.assertRaises(ValueError, Test_object.config_register,
                          'PORTJ', Pins=[], set_pins=False)

    def test_config_data_buffer_value_for_pin(self):
        """ pin numbers going from 0 to 7
            Testing the value of output data buffer
        """
        for i in range(0, 8):
            self.assertEqual(Test_object.config_register('DDRA', Pins=[i],
                             set_pins=True), ['\x0b', chr(2**i), '\x01'])

    def test_config_data_buffer_value_for_pincombinations(self):
        """
        different combination of pin numbers
        """
        pin_numbers = []
        pin_value = 0
        for i in range(0, 8):
            pin_numbers.append(i)
            pin_value = pin_value + 2**i
            self.assertEqual(Test_object.config_register('DDRA',
                             Pins=pin_numbers,
                             set_pins=True),
                             ['\x0b', chr(pin_value), '\x01'])

    def test_config_buffer_value_for_ports(self):
        """ Output data buffer values for Ports A-L
        """
        valid_port_names = [chr(i) for i in range(65, 77) if chr(i) != 'I']
        pin_value = 8
        pin_numbers = [3]
        for j in valid_port_names:
            port_name = 'DDR' + j
            buffer_value_port = (chr(ord(port_name[3])-54))
            self.assertEqual(Test_object.config_register(port_name,
                             Pins=pin_numbers, set_pins=True),
                             [buffer_value_port, chr(pin_value), '\x01'])


class Testbuzzer(unittest.TestCase):
    """ Testing the functionality of
        Buzzer class
    """
    @mock.patch('roboapi.Atmega.config_register')
    def Test_buzzer(self, mock_config_register):
        """checking for correct initialization of PortC
        """
        # object of class Buzzer
        x = Buzzer(9600)
        x.on()
        Registername = 'PortC'
        pins = [3]
        set_pins = True
        expected = [mock.call('DDRC', [3], True),
                    mock.call('PortC', [3], True)]
        mock_config_register.assert_has_calls(expected)
        x.off()
        expected = [mock.call('PortC', [3], False)]
        # checking whether config_register is called with correct arguments
        mock_config_register.assert_has_calls(expected)


class Testmotion(unittest.TestCase):

    @mock.patch('roboapi.Atmega.config_register')
    def Test_initialize(self, mock_config_register):
        '''tests for robot motion'''
        #object of class Motion
        x = Motion(9600)
        """
        checking whether config_register 
        has the correct calls
        """
        expected = [mock.call('DDRL', [3, 4], True),
                    mock.call('PortL', [3, 4], True),
                    mock.call('DDRA', [0, 1, 2, 3], True),
                    mock.call('PortA', [0, 1, 2, 3], False)]
        mock_config_register.assert_has_calls(expected)

    @mock.patch('roboapi.Atmega.config_register')
    def Test_motion(self, mock_config_register):
        '''tests for different motion'''
        x = Motion(9600)
        expected = [mock.call('DDRL', [3, 4], True),
                    mock.call('PortL', [3, 4], True),
                    mock.call('DDRA', [0, 1, 2, 3], True),
                    mock.call('PortA', [0, 1, 2, 3], False)]
        mock_config_register.assert_has_calls(expected)
        
        # test for forward motion
        x.forward()
        expected = [mock.call('PortA', [0], False),
                    mock.call('PortA', [1], True),
                    mock.call('PortA', [2], True),
                    mock.call('PortA', [3], False)]
        mock_config_register.assert_has_calls(expected)
        
        # test for backward motion
        x.back()
        expected = [mock.call('PortA', [0], True),
                    mock.call('PortA', [1], False),
                    mock.call('PortA', [2], False),
                    mock.call('PortA', [3], True)]
        mock_config_register.assert_has_calls(expected)
        
        # test for left direction
        x.left()
        expected = [mock.call('PortA', [0], False),
                    mock.call('PortA', [1], True),
                    mock.call('PortA', [2], False),
                    mock.call('PortA', [3], True)]
        mock_config_register.assert_has_calls(expected)
        
        # test for right direction
        x.right()
        expected = [mock.call('PortA', [0], True),
                    mock.call('PortA', [1], False),
                    mock.call('PortA', [2], True),
                    mock.call('PortA', [3], False)]
        mock_config_register.assert_has_calls(expected)
        
        # test for soft left
        x.soft_left()
        expected = [mock.call('PortA', [0], False),
                    mock.call('PortA', [1], False),
                    mock.call('PortA', [2], True),
                    mock.call('PortA', [3], False)]
        mock_config_register.assert_has_calls(expected)
        
        # test for soft right
        x.soft_right()
        expected = [mock.call('PortA', [0], False),
                    mock.call('PortA', [1], True),
                    mock.call('PortA', [2], False),
                    mock.call('PortA', [3], False)]
        mock_config_register.assert_has_calls(expected)
        
        # test for stop
        x.stop()
        expected = [mock.call('PortA', [0], False),
                    mock.call('PortA', [1], False),
                    mock.call('PortA', [2], False),
                    mock.call('PortA', [3], False)]
        mock_config_register.assert_has_calls(expected)


