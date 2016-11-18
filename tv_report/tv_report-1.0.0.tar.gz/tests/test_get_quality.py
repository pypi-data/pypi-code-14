import unittest
import tv_report

class test_get_quality(unittest.TestCase):
    def test_get_quality_width_1080p(self):
        test_data = [ 1900, 1920, 1930 ]

        for width in test_data:
            track = lambda: None
            track.width = width
            track.height = 0
            quality = tv_report.get_quality(track)
            self.assertEqual(quality, "1080p")


    def test_get_quality_width_720p(self):
        test_data = [ 1200, 1280, 1290 ]

        for width in test_data:
            track = lambda: None
            track.width = width
            track.height = 0
            quality = tv_report.get_quality(track)
            self.assertEqual(quality, "720p")


    def test_get_quality_width_sd(self):
        test_data = [ 400, 800, 999 ]

        for width in test_data:
            track = lambda: None
            track.width = width
            track.height = 0
            quality = tv_report.get_quality(track)
            self.assertEqual(quality, "SD")


    def test_get_quality_width_unknown(self):
        test_data = [ 1100, 2000 ]

        for width in test_data:
            track = lambda: None
            track.width = width
            track.height = 0
            quality = tv_report.get_quality(track)
            self.assertEqual(quality, "Unknown")


    def test_get_quality_height_1080p(self):
        test_data = [ 1000, 1080, 1100 ]

        for height in test_data:
            track = lambda: None
            track.height = height
            track.width = 0
            quality = tv_report.get_quality(track)
            self.assertEqual(quality, "1080p")


    def test_get_quality_height_720p(self):
        test_data = [ 650, 720, 730 ]

        for height in test_data:
            track = lambda: None
            track.height = height
            track.width = 0
            quality = tv_report.get_quality(track)
            self.assertEqual(quality, "720p")
