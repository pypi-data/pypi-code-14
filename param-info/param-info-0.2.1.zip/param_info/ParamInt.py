from . import Errors
from . import helpers
from .Param import *



class ParamInt(Param):
    def __init__(self,name,default = None, min=None,max=None):
        super().__init__(name,default)
        self.min = min
        self.max = max

    def parse(self,text=None):
        if not self.setValue(text):
            return self
        return self.validate( helpers.parseInt(self.value) )

    def validate(self,kk):
        self._value = kk
        if self.min != None and self.max != None:
            if kk == None or  kk < self.min or kk > self.max:
                return self.setError( Errors.Error_IntRange(self) )
        elif self.min != None:
            if kk == None or kk < self.min:
                return self.setError( Errors.Error_IntMin(self) )
        elif self.max != None:
            if kk == None or kk > self.max:
                return self.setError( Errors.Error_IntMax(self) )
        else:
            if kk == None:
                return self.setError( Errors.Error_Int(self) )
        return self.setValid()
