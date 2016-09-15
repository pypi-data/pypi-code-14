# -*- coding: utf-8 -*-

from datetime import datetime
from pytz import timezone
import requests

class AxessPacket():
    error_dict = {'00': 'OK', '33': 'Invalid card','34': 'Invalid reason','35': 'Disabled user','36': 'Disabled card','37': 'Expired user','38': 'Not authorized','39': 'User out of time',
                    '41': 'Missing auth group','42': 'Missing Timemod','44': 'Invalid pincode','45': 'Invalid day','48': 'Invalid edition',
                    '51': 'Biometric check 1:1 failed / User not found in biometric archive','52': 'Expired card','53': 'Missing CARDS.TXT and CARDRNGE.TXT','54': 'Missing AUTHGRP.TXT',
                    '55': 'Missing AUTH.TXT', '56': 'Missing TIMEMOD.TXT','59': 'Invalid common code','60': 'Transaction refused by host in online mode'
                }
                
    ack = "ack=1"
    keepalive = "beep=100"
                
    def __init__(self):
        self.mac_address = ""
        self.card_id = ""
        self.direction = ""
        self.timestamp = ""
        self.reason = ""
        self.error = ""
        
    def __str__(self):
        return self.mac_address+", "+repr(self.timestamp)+", "+self.direction+", "+self.card_id+", "+self.reason+", "+self.error
        
    def parsePacket(self, params):
        self.mac_address = params.get('mac')
        payload = ""
        if(params.get('trsn') is not None):
            payload = params.get('trsn')
        elif(params.get('badge') is not None):
            payload = params.get('badge')
    
        data = payload.split(",")
        self.card_id = data[4]
        if(data[2] == '0'):
            self.direction = "OUT"
        elif(data[2] == '1'):
            self.direction = "IN"

        self.timestamp = datetime(int(data[0][:4]),int(data[0][4:6]), int(data[0][6:]), int(data[1][:2]), int(data[1][2:4]), int(data[1][4:]))
        self.timestamp = timezone('Europe/Rome').localize(self.timestamp)
        print self.timestamp
        self.reason = data[3]
        self.error = self.error_dict[data[5]]
        
        self.checkPacket()
        return self
      
    def checkPacket(self):
        if(self.mac_address is None or self.mac_address==""):
            raise MacAddressError('Missing mac address')
        if(self.card_id is None or self.card_id==""):
            raise CardError('Missing card id')
        if(self.direction is None or (self.direction!="OUT" and self.direction!="IN")):
            raise ValueError('Invalid or missing direction')
        if(not(isinstance(self.timestamp, datetime))):
            raise TypeError('Invalid or missing timestamp')
     
    def message(self, msg, beep=100, show=2):
        return "beep="+beep+"\nscreen=\f"+msg+"\nshow="+show
     
    def sendKeepAlive(self, url, username, password):
        requests.get(url+'/keepalive_req.cgi', auth=(username,password))

        
class MacAddressError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
        
class CardError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)       