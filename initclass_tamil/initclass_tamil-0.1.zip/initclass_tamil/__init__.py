#class Example
#self will always replce the mthod
import xml.etree.ElementTree
import csv
class initclass_tamil:
    num = 100    # Pun=blic variable.to acess within objects,use selff.prefix
    
    #no parammeter
    def f(self):
        print "Hello"
    #single parameter method
    def retfunc(self,num2):
        return self.num+num2+20
    #init object

    def __init__(self,xval,yval):

        self.xvalue = xval
        self.yvalue = yval
    


