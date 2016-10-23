from Second import *
from Hour import *
from Minute import *
from ElementConnector import *


class DagmawiTime():
    '''Main module for instance of time'''

    def __init__(self,second, minute, hour):
        self.__second = Second(second)
        self.__minute = Minute(minute)
        self.__hour = Hour(hour)
        self.__connector = ElementConnector()

    def getTime(self):
        return (self.__second.getVal(), self.__minute.getVal(), self.__hour.getVal())

    def dispTime(self):
        time = self.getTime()
        print "%02d:%02d:%02d" % (time[2], time[1], time[0])
        return "%02d:%02d:%02d" % (time[2], time[1], time[0])

    def getTimeStandard(self):
        return (self.__second.getVal(), self.__minute.getVal(), (self.__hour.getVal() % 12))

    def dispTimeStandard(self):
        time = self.getTimeStandard()
        print "%02d:%02d:%02d" % (time[2], time[1], time[0])
        return "%02d:%02d:%02d" % (time[2], time[1], time[0])

    def incSec(self):
        self.__second.increment()
        self.__connector.checkForRollOver(self.__second, self.__minute)
        self.__connector.checkForRollOver(self.__minute, self.__hour)

    def decSec(self):
        self.__second.decrement()
        self.__connector.checkForRollUnder(self.__second, self.__minute)
        self.__connector.checkForRollUnder(self.__minute, self.__hour)

    def incMin(self):
        self.__minute.increment()
        self.__connector.checkForRollOver(self.__minute, self.__hour)

    def decMin(self):
        self.__minute.decrement()
        self.__connector.checkForRollUnder(self.__minute, self.__hour)

    def incHour(self):
        self.__hour.increment()

    def decHour(self):
        self.__hour.decrement()


if __name__ == '__main__':
    DGTime = DagmawiTime(23,590,590)
    DGTime.dispTime()
    print dir(DGTime)
