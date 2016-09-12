﻿import serial
from serial.tools import list_ports
import logging
import sys
import time

from threading import Lock

logger = logging.getLogger('gecko')


CONTROL_ANYTHING = "ControlAnything"
GROVEPI = "GrovePi"

GrovePi_write_address = 0x08
GrovePi_read_address = 0x09


class GeckoObjectNotInstantiated(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)


def a2s(arr):
    """ Array of integer byte values --> binary string
    """
    return ''.join(chr(b) for b in arr)

class ControlAnything(object):
    '''
    Represents the Control anything board https://www.controlanything.com/Relay/Relay/USB_AD
    '''
    ser = None

    # Used to control access to the serial port.
    lock = Lock()
    def __init__(self, serial):
        self.ser = serial
        return super(ControlAnything, self).__init__()

    @staticmethod
    def ca_sendCommand(ser, commandArray, responseLength):
        ser.write(a2s(commandArray))
        # flip endianess
        b = ser.read(responseLength)[::-1]
        val = b.encode('hex')
        return val

       

    def readAnalog(self, pin, samples_per_read = 1):
        self.lock.acquire()
        try:
            # flush out any existing stuff
            self.ser.read(100)

            samples = []

            # This loop is for if we want to do any averaging.
            b = None
            for i in range(samples_per_read):
                # it seems that some voltage was lingering around from the previous
                # make request to read 12 bit adc at specified port
                self.ser.write(a2s([254,199,pin]))
                # flip endianess
                b = self.ser.read(2)[::-1]

                if b == None:
                    logger.error("Unable to read adc port: " + str(pin))

                # convert to a number
                adc_counts = int(b.encode('hex'),16)
                # convert to voltage
                scaler = (5/float((2 ** 12)))
                voltage = scaler * adc_counts
                samples.append(voltage)
                
            # If we're only reading one sample, return the raw value
            if samples_per_read == 1:
                return samples[0]
            
            return samples
        finally:
            self.lock.release() # release lock
            

class GrovePi(object):
    '''
    Represents a GrovePi board (Attached via a BP)
    '''
    ser = None
    def __getPort():
        '''

        '''
        if Gecko.deviceList == None:
            raise GeckoObjectNotInstantiated
        Gecko.deviceList

    @staticmethod
    def isBusPirate(ser):
        '''
        Put Buspirate into binary mode
        '''
        # clear buffer
        ser.read(100)
        # enter bitbang mode
        tries = 0
        while tries < 20:
            logger.debug('attempt ' + str(ser))
            ser.write(a2s([int('00000000', 2)]))
            a = ser.read(5)
            if a == "BBIO1":
                return True
        
            tries = tries + 1
        return False


    def __init__(self, serial):
        '''
        Initializes the bus pirate into i2c mode and turns on the buspirate 
        power supplies and i2c pullups
        '''
        self.ser = serial
        if self.__bp_enterI2CMode(self.ser) == False:
            raise Exception("Failed to put bus pirate into i2c mode")
        if self.__bp_enablePsuPu(self.ser) == False:
            raise Exception("Failed to turn on ps pu")

        self.__bp_setSpeed(self.ser, 100)
        return super(GrovePi, self).__init__()


    def __bp_enterBBMode(self, port):
        '''
        Put Buspirate into binary mode
        '''
        # clear buffer
        port.read(100)
        # enter bitbang mode
        tries = 0
        while tries < 20:
            port.write(a2s([int('00000000', 2)]))
            a = port.read(5)
            if a == "BBIO1":
                return True
        
            tries = tries + 1
        return False

    def __bp_enterI2CMode(self, ser):
        '''
        Put Buspirate in I2C mode
        '''
        x = ser.read(100)
        # get to known state (Bitbang mode)
        ser.write(a2s([int('00000000', 2)]))
        b = ser.read(5)
        if b != "BBIO1":
            raise Exception("Unable to get into bit bang mode")

        # get int I2C mode
        ser.write(a2s([int('00000010', 2)]))
        b = ser.read(4)
        if b == "I2C1":
                return True

        raise Exception("Unable to get into bit bang mode")


    def __bp_sendStartBit(self, ser):
        '''
        Sends an i2c startbit
        '''
        ser.write(a2s([int('00000010', 2)]))
        b = ser.read(1)
        if b == "\x01":
            return True

        return False
    
    
    def __bp_sendStopBit(self, ser):
        '''
        Sends an i2c stop bit
        '''
        ser.write(a2s([int('00000011', 2)]))
        b = ser.read(1)
        if b == "\x01":
            return True

        return False

    
    
    def __bp_setSpeed(self, ser, khz):
        '''
        Set the i2c bus speed
        '''
        if khz == 100:
            ser.write(a2s([int('01100000', 2)]))
            b = ser.read(1)
        if b == "\x01":
            return True

        return False
    

    def __bp_enablePsuPu(self, ser):
        '''Enables power supplies and pull ups on the bus pirate
        '''
        ser.write(a2s([int('01001100', 2)]))
        b = ser.read(1)
        if b == "\x01":
            logger.debug('psupu on')
            return True

        return False
    
    
    
    def __bp_writeData(self, ser, arr):
        '''
        Sets up bus pirate to write data on the i2c port
        '''
        length = len(arr) - 1
        ser.write(a2s([int('00010000', 2) + length]))
        b = ser.read(1)
        if b != "\x01":
            logger.error("Unable to setup write data")
        
        bytes = a2s(arr)
        
        for byte in bytes:
            ser.write(byte)
            b = ser.read(1)
            if b == "\x00":
                logger.debug("ack received")
            if b == "\x01":
                logger.warning("byte was nacked")

    def __bp_readData(self, ser, address, numBytesToRead):
        results = []

        self.__bp_writeData(self.ser, [GrovePi_read_address])

        for i in range(numBytesToRead):
            # read byte
            ser.write(a2s([int('00000100', 2)]))
            results.append(ser.read(1))

            if (i != (numBytesToRead - 1)):
                ser.write(a2s([int('00000110', 2)]))
                b = ser.read(1)
                if b != "\x01":
                    logger.error("ack failed")
            else:
                ser.write(a2s([int('00000111', 2)]))
                b = ser.read(1)
                if b != "\x01":
                    logger.debug("nack failed")

        return results

        
        
        bytes = a2s(arr)
        
        for byte in bytes:
            ser.write(byte)
            b = ser.read(1)
            if b == "\x00":
                logger.debug("ack received")
            if b == "\x01":
                logger.warning("byte was nacked")


    def writeDigital(self, pin, value):
        '''
        Write to a digital port on the GrovePi
        '''
        writeVal = 0
        if value == 0:
            writeVal = 0
        else:
            writeVal = 1
        self.__bp_sendStartBit(self.ser)
        self.__bp_writeData(self.ser, [GrovePi_write_address,0x01,0x02,pin,writeVal,0x00])
        self.__bp_sendStopBit(self.ser)
        pass

    def readDigital(self, pin):
        writeVal = 0
      
        # Send read command
        self.__bp_sendStartBit(self.ser)
        self.__bp_writeData(self.ser, [GrovePi_write_address, 0x01, 0x01, pin, 0x00, 0x00])
        self.__bp_sendStopBit(self.ser)

        # wait for results to get loaded
        time.sleep(0.1)
        
        # Read results
        self.__bp_sendStartBit(self.ser)
        results = self.__bp_readData(self.ser, GrovePi_read_address, 2)
        self.__bp_sendStopBit(self.ser)

        if results == 0:
            return self.PIN_LEVEL.LOW
        else:
            return self.PIN_LEVEL.HIGH

        

    def writeAnalog(self, pin, value):
        """
        Value of pin to be 0-255
        Only works on digital ports 3, 5, 6
        ou do not need to call pinMode() to set the pin as an output before calling analogWrite().
        """
        if pin != 3 and pin != 5 and pin != 6:
            raise Exception("Only digital ports 3, 5, and 6 support analog writes")
        if value < 0 or value > 255:
            raise Exception("Value out of range (must be 0-255).")
        
        self.__bp_sendStartBit(self.ser)
        self.__bp_writeData(self.ser, [0x08,0x01,0x04,pin,value,0x00])
        self.__bp_sendStopBit(self.ser)


    class PIN_LEVEL():
        HIGH  = 1
        LOW   = 0
        #define HIGH 0x1
        #define LOW  0x0

    class PIN_MODES():
        INPUT           = 0
        OUTPUT          = 1
        INPUT_PULLUP    = 2


        #define INPUT 0x0
        #define OUTPUT 0x1
        #define INPUT_PULLUP 0x2


    def setPinMode(self, pin, mode):
        self.__bp_sendStartBit(self.ser)
        self.__bp_writeData(self.ser, [0x08,0x01,0x05,pin,mode,0x00])
        self.__bp_sendStopBit(self.ser)

    


class Gecko(object):
    # List of found devices
    deviceList = []

    def __init__(self):
        # For now, we're  going to assume that the user will only have one
        # Grove Pi and/or one Control anything board attached.  These are to make
        # it easier to access them.
        self.GrovePi = None
        self.ControlAnything = None

        # Go look for devices
        self.initGecko()
        return super(Gecko, self).__init__()

    def getDeviceList(self):
        return self.deviceList

    def initGecko(self):
        # Look for ftdi devices
        potentialPorts = []
        for port in list_ports.comports():
            if '0403' in port[2] and '6001' in port[2]:
                potentialPorts.append(port)

        for port in potentialPorts:
            # check if this is a control anything board
            error = None
            ser = None
            try:
                ser = serial.Serial(port[0], baudrate='115200', timeout=.05)
            except serial.serialutil.SerialException as e:
                error = e
                #logger.warning("Error connecting to port: " + str(e))

            logger.info("Connecting to port: " + str(port))
            if error == None:
                val = ControlAnything.ca_sendCommand(ser, [254,33], 1)
                
                try:
                    if int(val) == 55:
                        logger.info("Device found: " + CONTROL_ANYTHING)
                        dev = ControlAnything(ser)
                        self.deviceList.append(dev)
                        if self.ControlAnything == None:
                            self.ControlAnything = dev
                        continue
                except ValueError:
                    # not a control anything device
                    pass
                if GrovePi.isBusPirate(ser):
                    # check if there is a bus pirate attached.
                    # setup the bus pirate 
                   
                    logger.info("Device found: " + GROVEPI)
                    dev = GrovePi(ser)
                    self.deviceList.append(dev)
                    if self.GrovePi == None:
                        # Set the first one we see
                        self.GrovePi = dev
                    # self.deviceList.append({"port":ser,"type":GROVEPI})
                    continue

                else:
                    # Didn't find anything, close the port
                    ser.close()
                    
