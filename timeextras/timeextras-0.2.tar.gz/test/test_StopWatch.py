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
    sw = StopWatch()
    sleep(0.1)
    self.assertAlmostEqual(0.1, float(sw), places=accuracy)

  def test_as_string(self):
    sw = StopWatch()
    sleep(0.1)
    self.assertEqual(str(sw), '%.2f' % sw)
