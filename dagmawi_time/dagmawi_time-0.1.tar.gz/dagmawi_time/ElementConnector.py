class ElementConnector:

    def __init__(self):
        '''Module for connection between time elements'''

    def checkForRollOver(self, smallerTimeElement, greaterTimeElement):
        if ( smallerTimeElement.getCarryOut() > 0 ):
            greaterTimeElement.increment()
            smallerTimeElement.setCarryOut(0)

    def checkForRollUnder(self, smallerTimeElement, greaterTimeElement):

        if ( smallerTimeElement.getCarryIn() > 0 ):
            greaterTimeElement.decrement()
            smallerTimeElement.setCarryIn(0)


if __name__ == "__main__":
    p = ElementConnector
    print str(p)
    # p.checkForRollOver(wef,wef)

