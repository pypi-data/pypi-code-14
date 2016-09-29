class Error:
    def errorText(self):
        return 'Error'

class Error_Require(Error):
    def __init__(self,param):
        self.param = param
    def errorText(self):
        fmt = '{0} is required'
        return fmt.format( self.param.name )
class Error_Int(Error):
    def __init__(self,param):
        self.param = param
    def errorText(self):
        fmt = '{0}={1} should be integer'
        return fmt.format( self.param.name , self.param.text )
class Error_IntMin(Error):
    def __init__(self,param):
        self.param = param
    def errorText(self):
        fmt = '{0}={1} should be integer >= {2}'
        return fmt.format( self.param.name, self.param.text, self.param.min)
class Error_IntMax(Error):
    def __init__(self,param):
        self.param = param
    def errorText(self):
        fmt = '{0}={1} should be integer <= {2}'
        return fmt.format( self.param.name, self.param.text, self.param.max)
class Error_IntRange(Error):
    def __init__(self,param):
        self.param = param
    def errorText(self):
        fmt = '{0}={1} should be integer in range {2}-{3}'
        return fmt.format( self.param.name, self.param.text, self.param.min, self.param.max)
class Error_Val(Error):
    def __init__(self,param):
        self.param = param
    def errorText(self):
        fmt = '{0}={1} should be one of {2}'
        return fmt.format( self.param.name, self.param.text, ','.join(self.param._values))

class Error_Bool(Error):
    def __init__(self,param):
        self.param = param
    def errorText(self):
        fmt = '{0}={1} should be boolean value : 1,on,true,0,off,false'
        return fmt.format( self.param.name, self.param.text)