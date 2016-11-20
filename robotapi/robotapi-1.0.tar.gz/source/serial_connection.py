
import serial
import time
from glob import glob
import sys

# Global Variable declaration
global port
global port_detect


def serial_port_connection(port_detect, baudrate):
    """
    serial_port_connection(port_detect)

    Function: Multiple serial devices may be connected to system.
    This function list down all connected serial ports
    and ask user to select a desired port

    Parameters:

      1.port_detect = list
          list of all serial ports detected
      2.baudrate = Named Argument
          Baudrate for serial communication

    """
    global port

    port = serial.Serial(port_detect[0], baudrate)
    print "connected to: ", port_detect[0], "Baud rate = ", baudrate

    return port


def serial_open(baudrate):
    """
    Searches all serially connected devices.
    List all devices recognized as ttyUSB* (for Linux)

    """
    # stores all /dev/ttyUSB* into a list port_detect
    port_detect = glob("/dev/ttyUSB*")

    try:   # pragma: no cover
        port = serial_port_connection(port_detect, baudrate)
        if port.isOpen() == True:
            print "Port is open"
        else:
            port = serial_port_connection(port_detect, baudrate)

    except:
        print "No USB port detected....check connection"
        sys.exit(0)     # stop program execution when exception occur
