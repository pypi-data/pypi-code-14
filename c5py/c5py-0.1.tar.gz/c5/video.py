import cv2
import c5.config
from c5.config import VOL_PATH, STUDIES, FILE_NAMES


class VideoPlayer():
    def __init__(self, file_path):
        self.file_path = file_path
        self.cap = cv2.VideoCapture(self.file_path)
        self.buffer = []
        self.buffer_length = 20
        self.idx = 0
        self.img = None
        if self.cap.isOpened():
            self.fps = self.cap.get(cv2.cv.CV_CAP_PROP_FPS)
            _ = self.next()
        else:
            raise Exception("ERROR: no video at %s" % self.file_path)
 
    # CV_CAP_PROP_POS_FRAMES
    # CV_CAP_PROP_POS_MSEC
    def set_timestamp(self, timestamp):
        self.cap.set(cv2.cv.CV_CAP_PROP_POS_MSEC, timestamp - 1000);
        ret, tmp = self.cap.read()
        t = self.cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
        while t < timestamp - self.fps:
            ret, tmp = self.cap.read()
            t = self.cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
        self.img = cv2.cvtColor(tmp, cv2.COLOR_BGR2RGB)

    def set_frame(self, frame):
        self.cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, frame-10);
        ret, tmp = self.cap.read()
        t = self.cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
        while t < frame:
            ret, tmp = self.cap.read()
            t = self.cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
        print t
        self.img = cv2.cvtColor(tmp, cv2.COLOR_BGR2RGB)

    def get(self):
        return self.img

    def next(self):
        ret, tmp = self.cap.read()
        self.img = cv2.cvtColor(tmp, cv2.COLOR_BGR2RGB)
        return self.img


def get_video(timestamp, trial=None):
    conf, trial = c5.config.get_config(timestamp, trial)
    fname = FILE_NAMES['video_all'] % (trial % 100)
    player = VideoPlayer("{0}/{1}/trial{2}/{3}".format(VOL_PATH, STUDIES[trial/100-1], trial, fname))
    player.set(timestamp - conf.get('trial.start'))
    return player



