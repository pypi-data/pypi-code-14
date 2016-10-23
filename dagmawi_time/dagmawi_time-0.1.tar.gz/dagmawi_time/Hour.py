from TimeElement import *

class Hour( TimeElement ):
    'Definition of a hour time element'
    def __init__(self,val):
        TimeElement.__init__(self,"Hour",val,24)


if __name__ == '__main__':
    DGTime = Hour(10)
    print DGTime.getMax()
    print DGTime.getVal()
    print DGTime.__doc__