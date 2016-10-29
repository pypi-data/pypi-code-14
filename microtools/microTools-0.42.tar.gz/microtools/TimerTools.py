import threading
import time
from abc import ABCMeta, abstractmethod, abstractproperty
class TimerWrapper(object):
    def __init__(self):
        self.stopped = False
    def stop(self):
        """method to stop current timer"""
        self.stopped = True

class SimpleTimerObject(TimerWrapper):
    def __init__(self, timer):
        self.timer = timer
        super(SimpleTimerObject, self).__init__()

    def stop(self):
        self.timer.cancel()
        super(SimpleTimerObject, self).stop()

class DelayTimerObject(TimerWrapper):
    def __init__(self):
        self.setStart()
        super(DelayTimerObject, self).__init__()

    def setStart(self):
        self.start = getMicroTime()

    def delayReached(self, delay):
        if (getMicroTime() - self.start) >= delay * 1000:
            self.setStart()
            return True
        else:
            return False

def getMicroTime():
    return int(round(time.time() * 1000))


def setTimeout(fn, timeout=None):
    """

    :param fn:
    :type fn: function
    :param timeout: timeout before function starts
    :type timeout: int
    :return:
    :rtype: TimeObject
    """
    timer = threading.Timer(timeout, fn)
    timer.start()
    return SimpleTimerObject(timer)

__counter = 0
def setDelay(fn, delay=None):
    """

    :param fn:
    :type fn: function
    :param delay: delay between last function ends and new function starts
    :type delay: int
    :return:
    :rtype: TimeObject
    """
    global __counter
    __counter += 1
    def wrapper():
        while True:
            timeObject.setStart()
            while (not timeObject.delayReached(delay)) and not timeObject.stopped:
                time.sleep(0.01)
            if timeObject.stopped:
                return
            fn()

    timer = threading.Thread(target=wrapper, name="Timer_thread_" + str(__counter))
    timeObject = DelayTimerObject()
    timer.start()
    return timeObject

def setInterval(fn, interval=None):
    """

    :param fn:
    :type fn: function
    :param interval: interval between last function starts and new function starts
    :type interval: int
    :return:
    :rtype: TimeObject
    """
    global __counter
    __counter += 1
    def wrapper():
        timeObject.setStart()
        while True:
            while (not timeObject.delayReached(interval)) and not timeObject.stopped:
                time.sleep(0.01)
            if timeObject.stopped:
                return
            timeObject.setStart()
            fn()

    timer = threading.Thread(target=wrapper, name="Timer_thread_" + str(__counter))
    timeObject = DelayTimerObject()
    timer.start()
    return timeObject