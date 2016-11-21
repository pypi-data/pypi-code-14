__author__ = 'Sharon Lev'
__email__ = 'sharon_lev@yahoo.com'
__date__ = '11/5/16'

from unittest import TestCase
from src.timeextras import Timer
from time import time, sleep

class test_Timer(TestCase):
  """
  """

  def test_zero_init_timesout(self):
    """
    verify default timer expires immediately following init
    """
    timer = Timer()
    self.assertTrue(timer.expired)

  def test_timing_out(self, timeout=0.02):
    """
    verify timed timer expires when expected
    """
    timer = Timer(timeout)
    self.assertFalse(timer.expired)
    sleep(timeout)
    self.assertTrue(timer.expired)

  def test_extend_timer(self, timeout=0.02, extention=0.02):
    """
    verify expiration timeout can be extended
    """
    timer = Timer(timeout=timeout)
    sleep(timeout)
    self.assertTrue(timer.expired)
    timer.extend_by(extention)
    self.assertFalse(timer.expired)
    sleep(extention)
    self.assertTrue(timer.expired)
    self.assertEqual(timeout + extention, timer.timeout)

  def test_as_float(self, wait=0.02):
    """
    verify float casting returns a float with the expected value
    """
    timer = Timer()
    self.assertGreater(wait, float(timer))
    sleep(wait)
    self.assertLess(wait, float(timer))

  def test_as_string(self):
    """
    verify string casting prints the expected format of x.xxx (microsecond resolution)
    """
    timer = Timer(1.2)
    self.assertRegexpMatches(str(timer), '0.00\d')
    sleep(1.12)
    self.assertRegexpMatches(str(timer), '1.12\d')
    sleep(0.1)
    self.assertEqual('expired', str(timer))

  def test_stop(self):
    """
    verify stopped timers do not continue measuring time
    """
    timer = Timer(1)
    sleep(0.02)
    timer.stop()
    value = float(timer)
    sleep(0.02)
    self.assertEqual(value, float(timer))

  def test_restart(self):
    """
    verify restarted timers re-measure original set timeout
    """
    timer = Timer(0.02)
    sleep(0.02)
    self.assertTrue(timer.expired)
    timer.restart()
    sleep(0.01)
    self.assertFalse(timer.expired)
    self.assertAlmostEqual(0.01, float(timer), places=2)

  def test_resume(self):
    """
    verify stopped timers can be resumed
    """
    timer = Timer(0.02)
    timer.stop()
    value = float(timer)
    sleep(0.01)
    self.assertEqual(value, float(timer))
    timer.resume()
    sleep(0.01)
    self.assertTrue(timer.expired)

