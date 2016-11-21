__author__ = 'Sharon Lev'
__email__ = 'sharon_lev@yahoo.com'
__date__ = '11/5/16'

from unittest import TestCase
from time import sleep
from src.timeextras import StopWatch

accuracy = 1

class test_StopWatch(TestCase):
  """
  """
  def setUp(self):
    self.sw = StopWatch()

  def tearDown(self):
    del self.sw

  def test_elapsed(self):
    """
    validate simple elapsed functionality
    """
    sw = StopWatch()
    sleep(0.1)
    self.assertAlmostEqual(0.10, sw.elapsed, places=accuracy)

  def test_stop(self):
    """
    verify stopping a StopWatch stops it
    """
    sw = StopWatch()
    sleep(0.1)
    sw.stop()
    sleep(0.1)
    self.assertAlmostEqual(0.10, sw.elapsed, places=accuracy)

  def test_go_again(self):
    """
    verify calling go on a stopped StopWatch continues its tracking
    """
    sw = StopWatch()
    sleep(0.1)
    sw.stop()
    sleep(0.1)
    sw.go()
    sleep(0.1)
    self.assertAlmostEqual(0.20, sw.elapsed, places=accuracy)

  def test_go_go_go(self):
    """
    make sure that calling go on a running StopWatch doesn't break its functionality
    """
    sw = StopWatch()
    sleep(0.1)
    sw.go()
    sleep(0.1)
    sw.go()
    sleep(0.1)
    self.assertAlmostEqual(0.30, sw.elapsed, places=accuracy)

  def test_elapsed_by_id(self):
    """
    validate the use of multiple sub StopWatches independently
    """
    sw = StopWatch()
    sleep(0.1)
    sw.a.stop()
    sleep(0.1)
    sw.b.stop()
    sleep(0.1)
    sw.b.go()
    sleep(0.1)
    self.assertAlmostEqual(0.40, sw.elapsed, places=accuracy)
    self.assertAlmostEqual(0.10, sw.a.elapsed, places=accuracy)
    self.assertAlmostEqual(0.30, sw.b.elapsed, places=accuracy)

  def test_as_float(self):
    """
    verify float value of a StopWatch matches the expected elapsed time
    """
    sw = StopWatch()
    sleep(0.1)
    self.assertAlmostEqual(0.1, float(sw), places=accuracy)

  def test_as_string(self):
    """
    verify StopWatch as string is following the readable format of HH:MM:SS.mmm
    """
    self.sw._startTime -= ((1 * 3600) + (2 * 60) + 34 + 0.567)
    self.sw.stop()
    self.assertEqual('01:02:34.567', str(self.sw))

  def test_prop_micro(self):
    """
    verify the micro property returns the micro seconds portion of the StopWatch
    """
    self.sw._startTime -= 1.234
    self.sw.stop()
    string = str(self.sw)
    self.assertEqual('%d' % self.sw.micro, string.split('.')[-1])

  def test_prop_seconds(self):
    """
    verify the seconds property returns the seconds portion of the elapsed time (minus hours and minutes)
    """
    self.sw._startTime -= 61
    self.sw.stop()
    self.assertEqual(self.sw.seconds, 1)

  def test_prop_minutes(self):
    """
    verify the minutes property returns the minutes portion of the elapsed time (minus hours and seconds)
    """
    self.sw._startTime -= 61
    self.sw.stop()
    self.assertEqual(self.sw.minutes, 1)

  def test_prop_hours(self):
    """
    verify the hours property returns the hours portion of the elapsed time (minus hours and minutes)
    """
    self.sw._startTime -= 4000.123
    self.assertEqual(self.sw.hours, 1)
