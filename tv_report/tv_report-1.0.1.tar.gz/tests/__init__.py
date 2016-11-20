import unittest
import tv_report

class tv_report_tests(unittest.TestCase):

    def test_is_video(self):
        video_filenames = ["test file 123x124 - name.avi",
                           "test file 123x124 - name.mkv",
                           "test file 123x124 - name.mp4",
                           "test file 123x124 - name.mpg",
                           "test file 123x124 - name.mpeg",
                           "test file 123x124 - name.mov",
                           "test file 123x124 - name.m4v",
                           "test file 123x124 - name.flv",
                           "test file 123x124 - name.ts",
                           "test file 123x124 - name.wmv",
        ]

        non_video_filenames = ["test file 123x124 - name.foo",
                               "test file 123x124 - name.bar",
                               "test file 123x124 - name.txt",
                               "test file 123x124 - name.jpg",
        ]
        
        for filename in video_filenames:
            self.assertTrue(tv_report.is_video(filename))

        for filename in non_video_filenames:
            self.assertFalse(tv_report.is_video(filename))

    def test_get_videos_in_list(self):
        filenames = ["test file - 01x02 - foo bar.mkv",
                     "test file - 01x02 - foo bar.mp4",
                     "test file - 01x02 - foo bar.avi",
                     "test file - 01x02 - foo bar.wmv",
                     "test file - 01x02 - foo bar.jpg",
                    ]

        videos = tv_report.get_videos_in_list(filenames)
        self.assertEqual(len(videos), 4)
