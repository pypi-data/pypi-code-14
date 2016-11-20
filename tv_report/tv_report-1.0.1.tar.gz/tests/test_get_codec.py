import unittest
import tv_report

class test_get_codec(unittest.TestCase):
    def test_get_codec_x265(self):
        track = lambda: None
        track.format = "HEVC"
        codec = tv_report.get_codec(track)
        self.assertEqual(codec, "x265")


    def test_get_codec_x264(self):
        track = lambda: None
        track.format = "AVC"
        codec = tv_report.get_codec(track)
        self.assertEqual(codec, "x264")


    def test_get_codec_other(self):
        track = lambda: None
        track.format = "asdfas"
        codec = tv_report.get_codec(track)
        self.assertEqual(codec, "Other")
