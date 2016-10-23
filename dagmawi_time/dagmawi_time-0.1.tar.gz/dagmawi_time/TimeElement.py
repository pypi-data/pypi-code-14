class TimeElement:
    '''class definition for a time element'''

    def __init__(self,name, val, max):
        '''Initializer for a time element'''
        self.__name = name

        self.setMax(max)
        self.setVal(val)
        self.setCarryOut( 0 )
        self.setCarryIn( 0 )

    # Typically, access methods defined in python with @ decorator instead of
    # gettet/setter but this makes more sense for non-pythonians
    def setMax(self, max):
        if (self.checkValid( max, type(90),"") ):
            self.__max = max
        else:
            print 'Max not set for instance',self.getName()

    def getMax(self):
        return self.__max

    def setVal(self, val):
        if self.checkValid( val, type(90), self.getMax()):
            self.__val = val
        else:
            print 'Val not set for instance',self.getName()

    def getVal(self):
        return self.__val

    def setCarryOut(self, carryOut):
        if self.checkValid(carryOut,type(90),self.getMax()):
            self.__carryOut = carryOut
        else:
            print 'Carry Out not set for instance',self.getName()

    def getCarryOut(self):
        return self.__carryOut

    def setCarryIn(self, carryIn):
        if self.checkValid(carryIn,type(90),self.getMax()):
            self.__carryIn = carryIn
        else:
            print 'Carry In not set for instance',self.getName()

    def getCarryIn(self):
        return self.__carryIn

    def getName(self):
        return self.__name

    def increment(self):
        nextVal  = self.getVal() + 1
        self.setCarryOut( nextVal / self.getMax() )
        self.setVal( nextVal % self.getMax() )

    def decrement(self):
        nextVal  = self.getVal() - 1
        self.setVal( (nextVal + self.getMax()) % self.getMax() )
        if nextVal == -1 : self.setCarryIn(1);

    def checkValid(self, val, m_type, max):

        if( type(val) != m_type ):
            # raise Exception("Type incorrect")
            return False
        if max:
            if ( val > max ):
                # raise Exception("Value greater than max")
                return False
        return True






if __name__ == '__main__':
    DGTime = TimeElement("Test",0,70)
    print DGTime.getMax()
    print DGTime.getVal()
    print DGTime.getName()
    print DGTime.checkValid( 40, type(90), 50)
