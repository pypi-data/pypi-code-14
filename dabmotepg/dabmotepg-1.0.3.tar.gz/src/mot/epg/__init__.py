from mot import *
from spi import DabBearer
from spi.binary import encode_ensembleid, encode_bearer, decode_contentid

class EpgContentType():
    
    # content types 
    SERVICE_INFORMATION = ContentType(7, 0)
    PROGRAMME_INFORMATION = ContentType(7, 1)
    GROUP_INFORMATION = ContentType(7, 2)

class ScopeStart(HeaderParameter):
    
    def __init__(self, start):
        HeaderParameter.__init__(self, 0x25)
        self.start = start.replace(microsecond=0)

    def encode_data(self):
        return encode_absolute_time(self.start)
    
    def __str__(self):
        return self.start.isoformat()
    
    def __repr__(self):
        return '<ScopeStart: %s>' % str(self)
    
    @staticmethod
    def decode_data(data):
        return ScopeStart(decode_absolute_time(data))

class ScopeEnd(HeaderParameter):
    
    def __init__(self, end):
        HeaderParameter.__init__(self, 0x26)
        if not isinstance(end, datetime): raise TypeError('end must be a datetime')
        self.end = end.replace(microsecond=0)

    def encode_data(self):
        return encode_absolute_time(self.end)
    
    def __str__(self):
        return self.end.isoformat()
    
    def __repr__(self):
        return '<ScopeEnd: %s>' % str(self)
    
    @staticmethod
    def decode_data(data):
        return ScopeEnd(decode_absolute_time(data))

class ScopeId(HeaderParameter):

    def __init__(self, ecc, eid, sid=None, scids=None, xpad=None):
        HeaderParameter.__init__(self, 0x27)
        self.ecc = ecc
        self.eid = eid
        self.sid = sid
        self.scids = scids
        self.xpad = 0

    def encode_data(self):
        if self.ecc and self.eid and not self.sid and not self.scids: # ensemble ID
            return encode_ensembleid((self.ecc, self.eid))
        else: # DAB bearer ID
            return encode_bearer(DabBearer(self.ecc, self.eid, self.sid, self.scids))
    
    def __str__(self):
        result = []
        if (self.ecc and self.eid):
            return "%02x.%04x" % (self.ecc, self.eid)
        else:
            return "%02x.%04x.%04x.%x" % (self.ecc, self.eid, self.sid, self.scids)
    
    def __repr__(self):
        return '<ScopeId: %s>' % str(self)        
    
    @staticmethod
    def decode_data(data):
        return ScopeId(*decode_contentid(data))
    
HeaderParameter.decoders[0x25] = ScopeStart.decode_data
HeaderParameter.decoders[0x26] = ScopeEnd.decode_data   
HeaderParameter.decoders[0x27] = ScopeId.decode_data   
