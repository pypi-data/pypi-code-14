from PyQt4.QtCore import *
from PyQt4.QtGui import  *


import logging
import os

import cv2

import config
import utils

LOGGER = logging.getLogger(__name__)

VIDEO_W = 1200
VIDEO_H = 400

CAP_VIDEO_W = 400
CAP_VIDEO_H = 400


class CustomVideoCapture(QWidget):
    def __init__(self, fps, src, parent=None, init_recorder=True):
        super(CustomVideoCapture, self).__init__(parent)

        self._fps = fps
        self._src = src
        self._capture = None
        self._capturing = False
        self._writer = None
        self._record = True
        self.frame_width = None
        self.frame_height = None

       # if init_recorder:
            # self.set_writer()

        # Set the timer
        self._timer = QTimer()
        self._timer.timeout.connect(self.next_frame)

        # Gui part
        self._video_frame = QLabel()
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        layout = QVBoxLayout()
        layout.setMargin(0)
        layout.addWidget(self._video_frame)
        self.setLayout(layout)

    def set_writer(self):
        """
        video writer
        :return:
        """
        fourcc = config.Config()['video_format']
        LOGGER.info(fourcc)
        fourcc = cv2.cv.CV_FOURCC(*fourcc)

        file_name = utils.gen_filename('capture')
        path = utils.join_path(
            config.Config().get_path_exp('artifacts_path'),
            file_name
        )

        path += '.avi'

        LOGGER.info('{}, {}'.format(self.frame_width, self.frame_height))
        LOGGER.info('fps - {}'.format(self.fps))
        self._writer = cv2.VideoWriter(
            filename=path,
            fourcc=fourcc,
            fps=self.fps,
            frameSize=(self.frame_width, self.frame_height),
            isColor=True
        )

    def sizeHint(self):
        size = QSize(CAP_VIDEO_W, CAP_VIDEO_H)
        return size

    @property
    def record(self):
        return self._record

    @record.setter
    def record(self, data):
        self._record = data

    @property
    def fps(self):
        return self._fps

    @fps.setter
    def fps(self, new_value):
        self._fps = new_value

    @property
    def src(self):
        return self._src

    @src.setter
    def src(self, new_value):
        self._src = new_value

    @property
    def capturing(self):
        return self._capturing

    @capturing.setter
    def capturing(self, new_value):
        self._capturing = new_value

    def next_frame(self):
        success, frame = self._capture.read()

        if not success:
            LOGGER.debug('Failed to read from camera {}'.format(self.src))
            return
        # flip the colors (camera dependent)


        w = self.frameGeometry().width()
        h = self.frameGeometry().height()

        #TODO: split the size of the frame in gui, from the size of the recorded video

        # write to file
        if self.record:
            if self._writer:
                self._writer.write(frame)
            else:
                LOGGER.debug('writer is not available')

        frame = cv2.cvtColor(frame, cv2.cv.CV_BGR2RGB)

        w = w - (w % 100)
        h = h - (h % 100)

        frame = cv2.resize(frame, (w, h))

        img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pix = QPixmap.fromImage(img)
        self._video_frame.setPixmap(pix)

    def set_spec(self):
        #self.fps = self._capture.get(cv2.cv.CV_CAP_PROP_FPS)
        self.frame_width = int(self._capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self._capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))

    def start(self):
        if self._capture is None:
            self._capture = cv2.VideoCapture(self.src)

        self.set_spec()
        self.set_writer()
        LOGGER.debug('Start capturing from device {}'.format(self.src))
        self.capturing = True
        self._timer.start(1000 / self.fps)

    def stop(self):
        if not self.capturing:
            return

        LOGGER.debug('Stop capturing from device {}'.format(self.src))
        #self._release()
        self.capturing = False
        self._timer.stop()
        self._writer.release()

    def _release(self):
        if not self._capture:
            return

        self._capture.release()
        self._capture = None

    def delete_later(self):
        self._release()
        super(QWidget, self).deleteLater()


class CustomVideoPlay(QWidget):
    def __init__(self, parent=None):
        super(CustomVideoPlay, self).__init__(parent)

        self._src = None
        self._capture = None
        self._capturing = False
        self._playing = False
        self._fps = 60

        # Gui part

        self._video_frame = QLabel()
        self._video_frame.setGeometry(0, 0, VIDEO_W, VIDEO_H)

        layout = QVBoxLayout()
        layout.setMargin(0)
        layout.addWidget(self._video_frame)
        self.setLayout(layout)

    def sizeHint(self):
        size = QSize(600, 400)
        return size

    @property
    def src(self):
        return self._src

    @src.setter
    def src(self, new_value):
        self._src = new_value

    @property
    def fps(self):
        return self._fps

    @fps.setter
    def fps(self, new_value):
        self._fps = new_value

    def _play(self):

        while self._playing and self._capture.isOpened():
            success, frame = self._capture.read()

            if not success:
                LOGGER.debug('Failed to read from {}'.format(self.src))
                return
            # flip the colors (camera dependent)
            # frame = cv2.cvtColor(frame, cv2.cv.CV_BGR2RGB)
            frame = cv2.resize(frame, (self.frameGeometry().width(), self.frameGeometry().height()))

            img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pix = QPixmap.fromImage(img)
            self._video_frame.setPixmap(pix)
            cv2.waitKey(self.fps / 1000)

    def start(self):
        LOGGER.debug('Start Playing {}'.format(self.src))
        self._playing = True
        self._play()

    def stop(self):
        LOGGER.debug('Stop Playing {}'.format(self.src))
        if self._capture:
            self._capture.release()
        LOGGER.debug('Released video {}'.format(self.src))
        self._playing = False

    def pause(self):
        LOGGER.debug('Pausing {}'.format(self.src))
        self._playing = False

    def next_video(self, next_vid):
        self.stop()
        self.src = next_vid
        self._capture = cv2.VideoCapture(self.src)
        self.fps = 25
        self.start()


class ControlVideoPlay(QWidget):
    def __init__(self, parent=None):
        super(ControlVideoPlay, self).__init__(parent=parent)

        self._capture = CustomVideoPlay(parent=self)

        self.stop_btn = QPushButton('Stop', parent=self)
        self.stop_btn.clicked.connect(self.stop)

        self.next_btn = QPushButton('Next', parent=self)
        self.next_btn.clicked.connect(self.next_video)

        self.btn_layout = QHBoxLayout()
        self.btn_layout.addWidget(self.next_btn)
        self.btn_layout.addWidget(self.stop_btn)

        # Gui part

        layout = QVBoxLayout()
        layout.addWidget(self._capture)
        layout.addLayout(self.btn_layout)
        self.setLayout(layout)

    def next_video(self, path):
        self._capture.next_video(path)

    def stop(self):
        self._capture.stop()

    def pause(self):
        self._capture.pause()


class ControlWindow(QWidget):
    def __init__(self, parent=None):
        super(ControlWindow, self).__init__(parent)

        self.capture = self._get_capture_device(20, 0)

        self.start_btn = QPushButton('Start', parent=self)
        self.start_btn.clicked.connect(self.start_capture)

        self.stop_btn = QPushButton('Stop', parent=self)
        self.stop_btn.clicked.connect(self.stop_capture)

        self.btn_layout = QHBoxLayout()
        self.btn_layout.addWidget(self.start_btn)
        self.btn_layout.addWidget(self.stop_btn)

        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        # Gui part

        layout = QVBoxLayout()
        layout.addWidget(self.capture)
        layout.addLayout(self.btn_layout)
        self.setLayout(layout)

    def sizeHint(self):
        size = QSize(CAP_VIDEO_W, CAP_VIDEO_H + self.start_btn.frameGeometry().height())
        return size

    def _get_capture_device(self, fps, src):
        dev = CustomVideoCapture(fps, src, parent=self)
        if not dev:
            LOGGER.debug('device {} is not available'.format(src))

        return dev

    def start_capture(self):
        if not self.capture.capturing:
            self.capture.start()

    def stop_capture(self):
        if self.capture and self.capture.capturing:
            self.capture.stop()


class CVVideo(QWidget):
    def __init__(self):
        super(CVVideo, self).__init__()

        layout = QVBoxLayout()

        self.image = QPixmap()
        self.label = QLabel()

        layout.addWidget(self.label)

        self.setLayout(layout)


    def capture(self):

        cap = cv2.VideoCapture(0)

        while (True):

            # Capture frame-by-frame
            ret, frame = cap.read()


            # Our operations on the frame come here
            #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Display the resulting frame
          #  cv2.imshow('frame', gray)

            frame = cv2.cvtColor(frame, cv2.cv.CV_BGR2RGB)

            img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pix = QPixmap.fromImage(img)
            self.label.setPixmap(pix)

            #self.image.loadFromData(gray)
            #self.label.setPixmap(self.image)

            if cv2.waitKey(16) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        cap.release()
        #cv2.destroyAllWindows()
