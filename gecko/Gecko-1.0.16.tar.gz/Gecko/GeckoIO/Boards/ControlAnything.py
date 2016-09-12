﻿import requests
import urllib
import logging


logger = logging.getLogger('gecko')



from ..I_O import Input

class IO(object):
    '''
    Any IO on a control anything board.  This is used to identify the board type from the pin type
    '''
    pass

class Pins():
    class Analog(Input, IO):
        samples_per_read = None
        def translation(self, val):
            return val

        def preprocess(self, board):
            return True

        def postprocess(self, board, input):
            '''
            Use class name as default write key for this value.
            '''
            return {self.__class__.__name__ : input}

        @staticmethod
        def getVal (sensor, gecko, host):
            res =sensor.preprocess(gecko)
            
            # If we didn't abort during the preprocess
            if res == True:
                # get value
                if sensor.samples_per_read >= 1:
                    t = gecko.ControlAnything.readAnalog(sensor.pin_id, samples_per_read = sensor.samples_per_read)
                else:
                    logger.error("Invalid samples per read: " + str(sensor.samples_per_read))

                # Send through translation
                processedVal = sensor.translation(t)

                # post process
                valsToSend = sensor.postprocess(gecko, processedVal)
                if valsToSend != None:
                    # send data to exosite
                    name = sensor.__class__.__name__
                    # thing to send
                    if hasattr(sensor, 'cik'):
                        if sensor.cik != None:
                            # send using specified cik
                            headers = {'X-Exosite-CIK': sensor.cik,
                                       'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}

                            logger.info(sensor.__class__.__name__ + " -- Sending to Exosite: "  + str(valsToSend))
                        
                            try:
                                r = requests.post(host + '/onep:v1/stack/alias', data=valsToSend, headers=headers)
                            except requests.exceptions.RequestException as e:
                                logger.error("Error sending request: " + str(e))

                            logger.info(sensor.__class__.__name__ + " -- Send results: " + str(r.status_code))
                            if r.status_code > 299:
                                logger.error(sensor.__class__.__name__ + " -- Error writing some/all data: " + r.content)



        def __init__(self):
            # default samples per read
            if self.samples_per_read == None:
                self.samples_per_read = 1
            
    def __init__(self, stuff):
        pass