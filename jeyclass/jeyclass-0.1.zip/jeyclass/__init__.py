#Class with object

class jeyclass:
    num = 100 #public variable
    __num1 = 10 #private variable

    def func(self):
        print "hello"
    def retfunc(self,num2):
      return self.num + num2+10 + self.__num1

    #init oobject,variables x and y are created as init called
    
    def __init__(self,xval,yval):
        self.x = xval
        self.y = yval

