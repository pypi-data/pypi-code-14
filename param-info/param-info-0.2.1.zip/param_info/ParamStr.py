from .Param import *

class ParamStr(Param):
    def __init__(self,name,default = None):
        super().__init__(name,default)

    def parse(self,text=None):
        if not self.setValue(text):
            return self
        self._value = self._value.strip()
        return self.setValid()
