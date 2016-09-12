from Gecko import GeckoIO

class moisture(GeckoIO.Boards.ControlAnything.Pins.Analog):

    # This is optional and typically used during devlopment.
    # if this doesn't exist, 
    cik = '66e6e18d941feae76462f7b30e49c23b1f8080b9'


    # Pin identifier on the board
    pin_id = 0

    # Report rate in seconds
    # Must be a multiple of read_rate, else will be rounded up to read rate.
    # default is 10 seconds
    report_rate = 5

    # description of sensor
    description = "Monitors the moisture content of the soil for the plant in the office"

    def translation(self, input):
        '''
        Translation to apply to the incoming data, inputted value is voltage and output is
        value that will be sent to be post processed.
        '''
        return input

    def preprocess(self, board):
        '''
        do things before the sensor is read (power on sensors, read other sensors)
        return false if processing should stop (default is true)
        '''

        return True
        

    def postprocess(self, board, input):
        '''
        return a dictionary of key values to write to Exosite.
        If you don't want to send anything, return None.

        Default behavior is to write the input value to a dataport with the same name as
        this class is named
        '''
        # Data is sent before the report rate interval if this threshold is crossed
        # evaluated after data is ran through optional translation function
        #high_threshold = 12

        # Data is sent before the report rate interval if this threshold is crossed
        # evaluated after data is ran through optional translation function
        #low_threshold = 10

        #vals_to_write = {   
        #                    self.__class__.__name__ :   input, 
        #                    "some_alert" :              "Something Happened!"
        #                }

        vals_to_write = {   
                            self.__class__.__name__ :   input
                        }

        return vals_to_write

class lightsensor(GeckoIO.Boards.ControlAnything.Pins.Analog):

    # This is optional and typically used during devlopment.
    # if this doesn't exist, 
    cik = '66e6e18d941feae76462f7b30e49c23b1f8080b9'


    # Pin identifier on the board
    pin_id = 1

    # Report rate in seconds
    # Must be a multiple of read_rate, else will be rounded up to read rate.
    # default is 10 seconds
    report_rate = 5

    # description of sensor
    description = "Monitors the moisture content of the soil for the plant in the office"

    def translation(self, input):
        '''
        Translation to apply to the incoming data, inputted value is voltage and output is
        value that will be sent to be post processed.
        '''
        return input

    def preprocess(self, board):
        '''
        do things before the sensor is read (power on sensors, read other sensors)
        return false if processing should stop (default is true)
        '''

        return True
        

    def postprocess(self, board, input):
        '''
        return a dictionary of key values to write to Exosite.
        If you don't want to send anything, return None.

        Default behavior is to write the input value to a dataport with the same name as
        this class is named
        '''
        # Data is sent before the report rate interval if this threshold is crossed
        # evaluated after data is ran through optional translation function
        #high_threshold = 12

        # Data is sent before the report rate interval if this threshold is crossed
        # evaluated after data is ran through optional translation function
        #low_threshold = 10

        #vals_to_write = {   
        #                    self.__class__.__name__ :   input, 
        #                    "some_alert" :              "Something Happened!"
        #                }

        vals_to_write = {   
                            self.__class__.__name__ :   input
                        }

        return vals_to_write

class temperature(GeckoIO.Boards.ControlAnything.Pins.Analog):

    # This is optional and typically used during devlopment.
    # if this doesn't exist, 
    cik = '66e6e18d941feae76462f7b30e49c23b1f8080b9'


    # Pin identifier on the board
    pin_id = 2

    # Report rate in seconds
    # Must be a multiple of read_rate, else will be rounded up to read rate.
    # default is 10 seconds
    report_rate = 5

    # description of sensor
    description = "Monitors the moisture content of the soil for the plant in the office"

    def translation(self, input):
        '''
        Translation to apply to the incoming data, inputted value is voltage and output is
        value that will be sent to be post processed.
        '''
        return input

    def preprocess(self, board):
        '''
        do things before the sensor is read (power on sensors, read other sensors)
        return false if processing should stop (default is true)
        '''

        return True
        

    def postprocess(self, board, input):
        '''
        return a dictionary of key values to write to Exosite.
        If you don't want to send anything, return None.

        Default behavior is to write the input value to a dataport with the same name as
        this class is named
        '''
        # Data is sent before the report rate interval if this threshold is crossed
        # evaluated after data is ran through optional translation function
        #high_threshold = 12

        # Data is sent before the report rate interval if this threshold is crossed
        # evaluated after data is ran through optional translation function
        #low_threshold = 10

        #vals_to_write = {   
        #                    self.__class__.__name__ :   input, 
        #                    "some_alert" :              "Something Happened!"
        #                }

        vals_to_write = {   
                            self.__class__.__name__ :   input
                        }

        return vals_to_write

