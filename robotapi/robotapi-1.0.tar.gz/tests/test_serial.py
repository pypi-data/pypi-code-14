import unittest
import mock
import sys
import os

module_path = os.path.dirname(os.path.curdir + "." + os.path.sep)
sys.path.insert(0, os.path.abspath(module_path+"/source"))

from serial_connection import serial_port_connection, serial_open
from roboapi import Atmega, Buzzer

# Creating an instance object for testing
Test_object = Atmega(9600)


class Serialtest(unittest.TestCase):
    """ Testing serial.open(), serial.write() and serail port exceptions
    """

    @mock.patch('serial_connection.serial.Serial')
    @mock.patch('serial_connection.glob')
    def Test_serial_port_connection(self, mock_glob, mock_serial_port):
        """
        test for correct serial port initialization
        checking whether serial_port_connection is
        called with the right arguments
        """
        self.portdetect = ['ttyUSB0', 'ttyUSB1']
        self.baudrate = 9600
        mock_glob('ttyUSB0')
        serial_port_connection(self.portdetect, baudrate=self.baudrate)
        mock_serial_port.assert_called_with(self.portdetect[0], self.baudrate)

    @mock.patch('serial_connection.serial.sys.exit')
    @mock.patch('serial_connection.glob')
    @mock.patch('serial_connection.serial.Serial')
    def Test_serial_open(self, mock_serial_port,
                         mock_serial_port_path, mock_sys_call):
        """test to check for serial port exception
        if a serial port is open no exception should be thrown
        """
        mock_serial_port_path('ttyUSB0')
        self.portdetect = ['ttyUSB0', 'ttyUSB1']
        self.baudrate = 9600
        mock_serial_port_path('ttyUSB0')
        serial_port_connection(self.portdetect, baudrate=self.baudrate)
        # checking whether sys.exit(0) is called or not
        mock_sys_call.assert_not_called()

    @mock.patch('serial_connection.serial.Serial')
    def Test_serial_write(self, mock_serial_port):
        """
        test for serial port write calls
        """
        self.portdetect = ['ttyUSB0', 'ttyUSB1']
        self.baudrate = 9600
        port = serial_port_connection(self.portdetect, baudrate=self.baudrate)
        # serial_write called with a dummy character
        Test_object.serial_write('p')
        """
        testing whether serial.write of the Pyserial api
        is called with right arguments
        """
        mock_serial_port.return_value.write.assert_called_once_with('p')
        data_buffer = []
        """
        calling config register and checking whether
        serial.write of Pyserial has appropriate calls
        """
        data_buffer = Test_object.config_register('DDRA', Pins=[3],
                                                  set_pins=True)
        expected = [mock.call(x) for x in data_buffer]
        port.write.assert_has_calls(expected)

    @mock.patch('serial_connection.sys')
    @mock.patch('serial_connection.serial.Serial.isOpen')
    def Test_serial_close_exception(self, mock_serial_port, mock_system_call):
        '''check for exit call when the port is closed'''
        self.portdetect = ['ttyUSB0', 'ttyUSB1']
        self.baudrate = 9600
        serial_open(self.baudrate)
        mock_system_call.exit.assert_called()
