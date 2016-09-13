#!/usr/bin/env python
# encoding: utf-8


import datetime
import time

__author__ = u'Hywel Thomas'
__copyright__ = u'Copyright (C) 2016 Hywel Thomas'


SECOND      = 1
TEN_SECONDS = 10 * SECOND
MINUTE      = 60
TEN_MINUTES = 10 * MINUTE
ONE_HOUR    = 60 * MINUTE

UTC = datetime.datetime.utcnow()
NOW = datetime.datetime.now()

tz_adjust = (NOW - UTC).seconds


class Timeout(object):

    def __init__(self,
                 seconds = None,
                 start_time_offset = 0,
                 start_in_an_expired_state = False):
        """
        initialise with s+ms < 0 for an infinite timeout
        """
        self.__timeout_length = self.seconds_to_timedelta(seconds)

        self.__start_time = (datetime.datetime.now() +
                             self.seconds_to_timedelta(start_time_offset))

        self.__end_time = self.__start_time
        if not start_in_an_expired_state:
            self.__end_time += self.__timeout_length

        self.__expired = None

    @staticmethod
    def seconds_to_timedelta(seconds):
        seconds = seconds if (seconds is not None and seconds >= 0) else 0
        microseconds = (seconds - int(seconds)) * 1000000
        return datetime.timedelta(seconds = int(seconds),
                                  microseconds = int(microseconds))

    @property
    def expired(self):
        if not self.__expired:
            self.__expired = datetime.datetime.now() >= self.__end_time
        return self.__expired

    def expire(self):
        if not self.__expired:
            self.__end_time = self.__start_time
            self.__expired = True

    def restart(self):
        self.__start_time = datetime.datetime.now()
        self.__end_time   = self.__start_time + self.__timeout_length
        self.__expired = False

    @property
    def elapsed_time(self):
        return datetime.datetime.now() - self.__start_time

    @property
    def time_remaining(self):
        if self.__expired:
            return datetime.timedelta(seconds = 0)
        time_remaining = self.__end_time - datetime.datetime.now()

        if time_remaining > self.__timeout_length:
            self.__expired = True
            return datetime.timedelta(seconds=0)
        return time_remaining

    @property
    def seconds_remaining(self):
        time_remaining = self.time_remaining
        try:
            return time_remaining.seconds + time_remaining.microseconds/1000000.0
        except AttributeError:
            return time_remaining
            
    def wait(self,
             message = None):

        if message is None:
            while not self.expired:
                #print('>%s'%self.seconds_remaining)
                time.sleep(self.seconds_remaining)
        else:
            while not self.expired:
                remaining = self.time_remaining.seconds

                # print rather than log as this gives a live
                # progress to the user for very long intervals
                # but is not relevant in logs.
                print(u'{message} in {minutes}m {seconds}s.'
                      .format(message = message,
                              minutes = remaining / 60,
                              seconds = remaining % 60))

                if remaining > ONE_HOUR:
                    if remaining > ONE_HOUR + TEN_MINUTES:
                        Timeout(ONE_HOUR).wait()
                    else:
                        Timeout(ONE_HOUR - TEN_MINUTES)

                elif remaining > TEN_MINUTES:
                    Timeout(TEN_MINUTES).wait()

                elif remaining > MINUTE:
                    Timeout(MINUTE).wait()

                else:
                    Timeout(TEN_SECONDS if remaining >= TEN_SECONDS else SECOND).wait()


class Stopwatch(object):

    def __init__(self):
        self.reset()
    
    def reset(self):
        self.__stop_time = None
        self.__laps = []
        self.__start_time = datetime.datetime.now()
    
    def stop(self):
        if self.__stop_time is None:
            self.__stop_time = datetime.datetime.now()
            return self.glance
        else:
            return self.__stop_time
        
    def lap(self):
        lap_end_time = datetime.datetime.now()
        lap_start_time = (self.__start_time
                          if not self.__laps
                          else self.__laps[-1][u'lap_end_time'])
        self.__laps.append({u'lap_start_time' : lap_start_time,
                            u'lap_end_time'   : lap_end_time,
                            u'lap_time'       : lap_end_time - lap_start_time,
                            })
        return self.__laps[-1][u'lap_time']

    @property
    def lap_times(self):
        return self.__laps

    @property
    def glance(self):
        if self.__stop_time:
            return self.__stop_time - self.__start_time
        else:
            return datetime.datetime.now() - self.__start_time


if __name__ == u"__main__":

    timeout = Timeout(-1)
    assert timeout.seconds_remaining <= 0, timeout.seconds_remaining
    assert timeout.time_remaining == datetime.timedelta(seconds=0), timeout.time_remaining
    assert timeout.expired

    timeout = Timeout(0)
    assert timeout.seconds_remaining == 0, timeout.seconds_remaining
    assert timeout.time_remaining == datetime.timedelta(seconds=0), timeout.time_remaining
    assert timeout.expired

    start_time = datetime.datetime.now()    
    Timeout(5).wait()
    assert datetime.datetime.now() >= datetime.timedelta(seconds=5) + start_time

    start_time = datetime.datetime.now()
    Timeout(0.5).wait()
    assert datetime.datetime.now() >= datetime.timedelta(milliseconds=500) + start_time
    assert datetime.datetime.now() < datetime.timedelta(milliseconds=600) + start_time

    start_time = datetime.datetime.now()
    timeout = Timeout(10)
    while not timeout.expired:
        time.sleep(1)
        print timeout.elapsed_time, timeout.time_remaining
        print timeout.seconds_remaining

    assert datetime.datetime.now() >= datetime.timedelta(seconds=10) + start_time

    stopwatch = Stopwatch()
    for _ in xrange(3):
        time.sleep(1)
        print stopwatch.lap()
    print stopwatch.stop()
