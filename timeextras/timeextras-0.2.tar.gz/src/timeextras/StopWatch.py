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
    return self._cumulative + ( (self._endTime or time()) - self._startTime )

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
    return '%.2f' % float(self)


class _SubStopWatch(StopWatch):
  def __init__(self, startTime, cumulative=0.0):
    self._cumulative = cumulative
    self._startTime = startTime
    self._subStopWatches = None # do not allow sub stop watches for a sub stop watch
