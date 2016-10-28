from msc import int_to_bitarray
from mot import HeaderParameter, encode_absolute_time, decode_absolute_time
from bitarray import bitarray

class TriggerTime(HeaderParameter):
    
    NOW = None
    
    def __init__(self, trigger=NOW):
        HeaderParameter.__init__(self, 5)
        self.trigger = trigger
        
    def encode_data(self):
        return encode_absolute_time(self.trigger)
    
    def __str__(self):
        return self.trigger.isoformat() if self.trigger is not None else 'NOW'
    
    def __repr__(self):
        return '<TriggerTime: %s>' % str(self)
    
    @staticmethod
    def decode_data(data):
        return TriggerTime(decode_absolute_time(data))

class UrlParameter(HeaderParameter):
    '''Abstract URL parameter'''
    
    ISO_IEC_10646 = 15
    
    def __init__(self, url, param):
        HeaderParameter.__init__(self, param) 
        self.url = url
        self.charset = UrlParameter.ISO_IEC_10646
        
    def encode_data(self):
        bits = bitarray()
        bits += int_to_bitarray(self.charset, 4) # (0-3): Character set indicator
        bits += int_to_bitarray(0, 4) # (4-7): RFA
        tmp = bitarray()
        tmp.fromstring(self.url)
        bits += tmp
        return bits
    
    def __str__(self):
        return self.url
        
    def __repr__(self):
        return "<{name}: {value}>".format(name=self.__class__.__name__, value=str(self))

class AlternativeLocation(UrlParameter):

    def __init__(self, url):
        UrlParameter.__init__(self, url, 0x28)

    @staticmethod
    def decode_data(data):
        return AlternativeLocation(data[8:].tostring()) 
    
class ClickThroughLocation(UrlParameter):

    def __init__(self, url):
        UrlParameter.__init__(self, url, 0x27)

    @staticmethod
    def decode_data(data):
        return ClickThroughLocation(data[8:].tostring()) 

HeaderParameter.decoders[5] = TriggerTime.decode_data
HeaderParameter.decoders[0x27] = ClickThroughLocation.decode_data 
HeaderParameter.decoders[0x28] = AlternativeLocation.decode_data 
