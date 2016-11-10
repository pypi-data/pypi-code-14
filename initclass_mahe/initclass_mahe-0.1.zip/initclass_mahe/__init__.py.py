
#Class with object

class initclass_mahe:

    num = 100;#publicvariable. visible outside. to access within objects, use self prefix
  
    #no parameter
    def func(self):
        print "hello"

    #single parameter method
    def retfunc(self, num2):        
        #return self.num+num2+10 #use self / classname to refer local variables
        return objclass.num+num2+10


      #single parameter method
    def retfunc(self, num2):        
        #return self.num+num2+10 #use self / classname to refer local variables
        return self.x+self.y+ +num2
    

    #init object
    ##constructor . Use __Init__(self, realpart , imaginarypart)
    def __init__(self, xval, yval):        
        self.x = xval #public variable. can be used in other functions
        self.y = yval #public variable. instead of x, y..can use any name
        
