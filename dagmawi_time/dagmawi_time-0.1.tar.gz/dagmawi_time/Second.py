from TimeElement import TimeElement

class Second( TimeElement ):
    'Class definition for a "second" time element'
    def __init__(self,val):
        TimeElement.__init__(self,"Second", val, 60 )


if __name__ == '__main__':
    DGTime = Second(0)
    print DGTime.getMax()
    print DGTime.getVal()
    print DGTime.__doc__
    print DGTime.getName()