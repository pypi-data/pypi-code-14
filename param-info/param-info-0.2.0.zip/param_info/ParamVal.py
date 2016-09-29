from .Param import *
from .      import Errors

class ParamVal(Param):
    def __init__(self,name,values,default = None):
        super().__init__(name,default)
        self._values = values

    def parse(self,text=None):
        if not self.setValue(text):
            return self
        if not self._given:
            self._value = self._values[self._value]
        if self._value not in self._values:
            self._value = None
            return self.setError( Errors.Error_Val(self) )
        return self.setValid()
