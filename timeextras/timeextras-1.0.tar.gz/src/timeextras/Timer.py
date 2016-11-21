__author__ = 'Sharon Lev'
__email__ = 'sharon_lev@yahoo.com'
__date__ = '11/5/16'

from time import time, sleep

class Timer(object):
  """
  a class to provide timer functionality for dealing with timeouts in an easy way
  """

  def __init__(self, timeout=0):
    """
    """
    self.restart()
    self._timeout = timeout

  def __nonzero__(self):
    return time() < self._startTime + self._timeout

  @property
  def expired(self):
    """
    :return: True if timer has expired, False otherwise
    """
    return not self.__nonzero__()

  @property
  def timeout(self):
    """
    :return: current set timeout
    """
    return self._timeout

  def extend_by(self, seconds):
    """
    :param seconds: (float) how many seconds to extend timeout by
    :returns: updated timeout
    """
    self._timeout += seconds
    return self.timeout

  def restart(self):
    """
    resets and restarts the timer from now
    """
    self._startTime = time()
    self._final = None

  def stop(self):
    """
    stops the timer, and maintain the current run time
    """
    self._final = self.__float__()

  def resume(self):
    """
    resumes a stopped timer and continues the timer
    :return:
    """
    self._final = None

  def sleep(self, seconds):
    """
    puts the process on delay
    :param seconds: (float) how many seconds to sleep for
    """
    sleep(seconds)

  def __float__(self):
    return self._final or time() - self._startTime

  def __str__(self):
    return '%.3f' % self.__float__() if not self.expired else 'expired'

