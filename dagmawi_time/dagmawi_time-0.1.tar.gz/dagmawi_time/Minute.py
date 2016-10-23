from TimeElement import TimeElement

class Minute( TimeElement ):
    'Class definition for a minute time element'
    def __init__(self,val):
        TimeElement.__init__(self,"Minute", val, 60 )


if __name__ == '__main__':
    DGTime = Minute(0)
    print DGTime.getMax()
    print DGTime.getVal()
    print DGTime.__doc__