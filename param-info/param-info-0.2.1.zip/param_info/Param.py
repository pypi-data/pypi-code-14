from . import Errors

class Param:
    def __init__(self,name,default = None):
        self._name      = name
        self._text      = None
        self._value     = None
        self._default   = default
        self._given     = False
        self._error     = None

    def parse(self,text):
        return self

    def find(self,values):
        return self.parse(values.get(self._name))

    def setError(self,error):
        self._error     = error
        self._errorText = self._error.errorText()
        return self

    def setValid(self):
        self._error     = None
        self._errorText = ''
        return self

    def setValue(self,value):
        self._text = value
        if self._text != None:
            self._value = self._text
            self._given = True
            return True
        self._given = False
        if self._default != None:
            self._value = self._default
            return True
        self.setError( Errors.Error_Require(self) )
        return False


    @property
    def name(self):
        return self._name
    @property
    def text(self):
        return self._text
    @property
    def value(self):
        return self._value
    @property
    def default(self):
        return self._default
    @property
    def given(self):
        return self._given
    @property
    def valid(self):
        return self._error == None
    @property
    def error(self):
        return self._error
    @property
    def errorText(self):
        return self._errorText
