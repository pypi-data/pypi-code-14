
__author__ = u'Hywel Thomas'
__copyright__ = u'Copyright (C) 2016 Hywel Thomas'


class Switch(object):

    ON = True
    OFF = False

    def __init__(self,
                 state = OFF):

        self.__state = True if state else False

    def on(self):
        self.__state = True

    def off(self):
        self.__state = False

    def __nonzero__(self):
        return self.__state

    @property
    def state(self):
        return self.ON if self else self.OFF
