from .Param import *
from .      import Errors

class ParamBool(Param):
    def __init__(self,name,default = None):
        super().__init__(name,default)

    def parse(self,text=None):
        if not self.setValue(text):
            return self
        if self._value in ['1' , 'on'  , 'true' ]:
            self._value = True
            return self.setValid()
        if self._value in ['0' , 'off' , 'false']:
            self._value = False
            return self.setValid()
        if not self.given and isinstance(self.default,bool):
            return self.setValid()
        self._value = None
        return self.setError( Errors.Error_Bool(self) )
