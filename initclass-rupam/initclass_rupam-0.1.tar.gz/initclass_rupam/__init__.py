# Class with object

class initclass_rupam:

    num = 100 # public variable. to access within objects, use self. prefix

    # no parameter
    def func(self):
        print "hello"

    # single parameter method
    def retfunc(self, num2):
        
        return self.num + num2

    # init object, the variables x and y will be created as __init__ is called
    def __init__ (self, xval, yval):
        self.x = xval
        self.y = yval
   
