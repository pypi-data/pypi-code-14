__author__ = 'Sharon Lev'
__email__ = 'sharon_lev@yahoo.com'
__date__ = '11/5/16'

from time import time

class StopWatch(object):
  """
  a class to provide time tracking functionality
  """

  def __init__(self):
    """
    """
    self._cumulative = 0.0
    self._startTime = 0.0
    self._endTime = None
    self._subStopWatches = {}
    self.go()

  @property
  def elapsed(self):
    return self._cumulative + ((self._endTime or time()) - self._startTime)

  @property
  def hours(self):
    return int(self.elapsed) / 3600
  
  @property
  def minutes(self):
    return int(self.elapsed) % 3600 / 60

  @property
  def seconds(self):
    return int(self.elapsed) % 60
  
  @property
  def micro(self):
    return (self.elapsed % 1) * 1000

  def go(self):
    self._cumulative = self._cumulative + ((self._endTime or time()) - self._startTime if self._startTime else 0.0)
    self._endTime = None
    self._startTime = time()

  def stop(self):
    self._endTime = time()

  def __getattr__(self, item):
    if getattr(super(StopWatch, self), item, None):
      return item
    else:
      if item not in self._subStopWatches:
        self._subStopWatches[item] = _SubStopWatch(startTime=self._startTime, cumulative=self._cumulative)
      return self._subStopWatches[item]

  def __float__(self):
    return self.elapsed

  def __str__(self):
    return '%02d:%02d:%02d.%03d' % (self.hours, self.minutes, self.seconds, self.micro)


class _SubStopWatch(StopWatch):
  def __init__(self, startTime, cumulative=0.0):
    self._cumulative = cumulative
    self._startTime = startTime
    self._subStopWatches = None # do not allow sub stop watches for a sub stop watch
