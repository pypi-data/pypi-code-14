'''API for Atmega 2560 based robot control'''

import sys
import os
import serial_connection as sc
import time


class Atmega(object):
    """ A Parent class for I/O port access """
    def __init__(self, baudrate=9600):
        """ Class Constructor

        Parameter:

            baudrate: named argument
              baudrate for serial communication.
              9600 by default.
        """
        self.baudrate = baudrate
        # self.port_check=sc.serial_open(self.baudrate)

    @classmethod
    def config_register(cls, Registername, Pins=[], set_pins=None):
        """ Accessing I/O ports of the controller
            Sends a serial packet to the controller
            based on the input arguments
        Parameters:
            1.Registername = str
                  Name of the I/O Port
            2.Pins = list
                  A comma separated list of I/O pin numbers
            3.set_pins = Named Argument
                  The corresponding pin numbers set to logic '1'
                  when True; set to logic '0' when False
        Examples:
            Port J access
              >>> config_register('PortJ', Pins=[1, 2, 4], set_pins=True)
            Port A access
              >>> config_register('DDRA', Pins=[0,5,3,5], set_pins=False)
              """

        pin_value = 0
        cls.send_data_buffer = []
        # raises exception for invalid empty Pins list #
        if len(Pins) == 0:
            raise ValueError("Pins cannot be empty")
        # converting to equivalent binary weights #
        for i in Pins:
            pin_value = pin_value + 2**i
        # raises exception for invalid pin numbers#
        if Registername[0] == 'D':
            cls.check_for_valid_pin_port(Registername[3], pin_value)
            k = (chr(ord(Registername[3])-54))
        elif Registername[0] == 'P':
            cls.check_for_valid_pin_port(Registername[4], pin_value)
            k = (chr(ord(Registername[4])-65))
        # convert alphabet to characters from 0 to 9 for A to J #
        # make a serial packet of three bytes to be sent to controller #
        cls.send_data_buffer.append(k)
        cls.send_data_buffer.append((chr(pin_value)))
        cls.send_data_buffer.append(chr(1) if set_pins else chr(0))
        print cls.send_data_buffer
        # send the packet byte by byte #
        cls.serial_write(cls.send_data_buffer)
        return cls.send_data_buffer

    @classmethod
    def check_for_valid_pin_port(cls, portname, pin_value):
        """
        Check for valid pin numbers and port numbers
        raises Value Error if invalid

        Parameters:
            1.portname: str
                  Port Name given by the user
            2.pin_value: integer
                  binary wieghted decimal representation
                  of the pin numbers given by the user
        """
        valid_port_names = [chr(i) for i in range(65, 77) if chr(i) != 'I']
        if pin_value > 255:
            raise ValueError("incorrect pin numbers")
        if portname not in valid_port_names:
            raise ValueError("incorrect port name")

    @classmethod
    def serial_write(cls, data):
        """ send data on the serial port """
        for i in range(len(data)):
            sc.port.write(data[i])
            time.sleep(0.2)


class Buzzer(Atmega):
    """ Derived class from parent class Atmega.
        Provides functions to control Buzzer """
    def __init__(self, baudrate):
        """Class constructor

         baudrate: named argument
              baudrate for serial communication.
              9600 by default.

        Buzzer is connected to Port C
        Instance varaibles set accordingly

        Instance variables:
            datadirection_register = DDRC
            port_register = PortC
            pin =3
            set_pin = 3
        """
        super(Buzzer, self).__init__(baudrate)
        self.datadirection_register = 'DDRC'
        self.port_register = 'PortC'
        self.pin = [3]
        self.set_pin = True
        Atmega.config_register(self.datadirection_register, self.pin, True)

    def on(self, on_time=0):
        """ Turn ON buzzer for a specified time

        Parameters:
            on_time = float
                ON time in seconds

        Examples:
            >>> Buzzer.on(5) "5" is ON time in seconds
            >>> Buzzer.on(0.3) "0.3" is ON time in seconds
        """
        Atmega.config_register(self.port_register, self.pin, True)
        if (on_time != 0):
            time.sleep(on_time)
            Atmega.config_register(self.port_register, self.pin, False)

    def off(self):
        """ Turn OFF buzzer
        Example:
            >>> Buzzer.off()
        """
        Atmega.config_register(self.port_register, self.pin, False)


class Motion(Atmega):
    """ Derived class to control the motion of the robot

        Description:
          DC motors controlled by PortL pins 3,4
          and PortA pins 0,1,2,3
    """
    def __init__(self, baudrate):
        """Class constructor
        Parameter:
            baudrate for serial communication
            9600 by default

        Instance variables:
            Sets Port L pins 3,4 as outputs and
            sets them to logic '1'

            datadirection_register = DDRL, DDRA
            port_register_enable = PORTL, PORTA
            pin_enable = [3,4] ,[0,1,2,3]

        """
        super(Motion, self).__init__(baudrate)
        self.datadirection_register = ['DDRL', 'DDRA']
        self.port_register_enable = ['PortL', 'PortA']
        self.pin_enable = [[3, 4], [0, 1, 2, 3]]
        # Set Direction Register -- DDRL

        Atmega.config_register(self.datadirection_register[0],
                               self.pin_enable[0], True)
        # Set Port Register -- PORTL
        Atmega.config_register(self.port_register_enable[0],
                               self.pin_enable[0], True)
        # Set Direction Register -- DDRA
        Atmega.config_register(self.datadirection_register[1],
                               self.pin_enable[1], True)
        # Set Port Register -- PORTA
        Atmega.config_register(self.port_register_enable[1],
                               self.pin_enable[1], False)

    def forward(self):
        """ Take the robot in forward direction
        Example:
            >>> Motion.forward()
        """
        # Right and left wheels move in forward direction
        Atmega.config_register(self.port_register_enable[1], [0], False)
        Atmega.config_register(self.port_register_enable[1], [1], True)
        Atmega.config_register(self.port_register_enable[1], [2], True)
        Atmega.config_register(self.port_register_enable[1], [3], False)

    def back(self):
        """ Move the robot back
        Example:
            >>> Motion.back()
        """
        # Left and Right wheels move backwards
        Atmega.config_register(self.port_register_enable[1], [0], True)
        Atmega.config_register(self.port_register_enable[1], [1], False)
        Atmega.config_register(self.port_register_enable[1], [2], False)
        Atmega.config_register(self.port_register_enable[1], [3], True)

    def left(self):
        """ Move the robot left
        Example:
            >>> Motion.left()
        """
        # Left wheel back and right wheel forward
        Atmega.config_register(self.port_register_enable[1], [0], False)
        Atmega.config_register(self.port_register_enable[1], [1], True)
        Atmega.config_register(self.port_register_enable[1], [2], False)
        Atmega.config_register(self.port_register_enable[1], [3], True)

    def right(self):
        """ Move the robot right
        Example:
            >>> Motion.right()
        """
        # Right wheel back and left forward
        Atmega.config_register(self.port_register_enable[1], [0], True)
        Atmega.config_register(self.port_register_enable[1], [1], False)
        Atmega.config_register(self.port_register_enable[1], [2], True)
        Atmega.config_register(self.port_register_enable[1], [3], False)

    def soft_left(self):
        """ Small deviation in robot motion towards left
        Example:
            >>> Motion.soft_left()
        """
        # Left wheek back right wheel stationary
        Atmega.config_register(self.port_register_enable[1], [0], False)
        Atmega.config_register(self.port_register_enable[1], [1], False)
        Atmega.config_register(self.port_register_enable[1], [2], True)
        Atmega.config_register(self.port_register_enable[1], [3], False)

    def soft_right(self):
        """ Small deviation in robot motion towards right
        Example:
            >>> Motion.soft_left()
        """
        # Right wheel back left wheel stationary
        Atmega.config_register(self.port_register_enable[1], [0], False)
        Atmega.config_register(self.port_register_enable[1], [1], True)
        Atmega.config_register(self.port_register_enable[1], [2], False)
        Atmega.config_register(self.port_register_enable[1], [3], False)

    def stop(self):
        """ Stop the robot
        Example:
            >>> Motion.stop()
        """
        # Both left and Right wheels stationary
        Atmega.config_register(self.port_register_enable[1], [0], False)
        Atmega.config_register(self.port_register_enable[1], [1], False)
        Atmega.config_register(self.port_register_enable[1], [2], False)
        Atmega.config_register(self.port_register_enable[1], [3], False)
