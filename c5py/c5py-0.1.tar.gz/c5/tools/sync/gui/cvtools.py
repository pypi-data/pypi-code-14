import cv
import sys
import os.path

from PyQt4 import QtCore, QtGui

class IplQImage(QtGui.QImage):
    """
    http://matthewshotton.wordpress.com/2011/03/31/python-opencv-iplimage-to-pyqt-qimage/
    A class for converting iplimages to qimages
    """

    def __init__(self,iplimage, frame_nr):
        # Rough-n-ready but it works dammit
        alpha = cv.CreateMat(iplimage.height,iplimage.width, cv.CV_8UC1) #@UndefinedVariable
        cv.Rectangle(alpha, (0, 0), (iplimage.width,iplimage.height), cv.ScalarAll(255) ,-1) #@UndefinedVariable
        rgba = cv.CreateMat(iplimage.height, iplimage.width, cv.CV_8UC4) #@UndefinedVariable
        cv.Set(rgba, (1, 2, 3, 4)) #@UndefinedVariable
        cv.MixChannels([iplimage, alpha],[rgba], [ #@UndefinedVariable
        (0, 0), # rgba[0] -> bgr[2]
        (1, 1), # rgba[1] -> bgr[1]
        (2, 2), # rgba[2] -> bgr[0]
        (3, 3)  # rgba[3] -> alpha[0]
        ])
        self.__imagedata = rgba.tostring()
        super(IplQImage,self).__init__(self.__imagedata, iplimage.width, iplimage.height, QtGui.QImage.Format_RGB32)
        self._frame = frame_nr

    def get_frame(self):
        return self._frame

class CVVideo():
    def __init__(self, parent = None):
        self._buffer = {}
        self._store = {}
        self.parent = parent

    def set_capture(self, path):
        self._capture = cv.CaptureFromFile(path) #@UndefinedVariable
        # Take one frame to query height
        frame = cv.QueryFrame(self._capture) #@UndefinedVariable
        self._frame = None
        self._image = self._build_image(frame)
        self._current = self._get_current_frame()
        self.path = path

    def _build_image(self, frame):
        if not self._frame:
            self._frame = cv.CreateImage((frame.width, frame.height), cv.IPL_DEPTH_8U, frame.nChannels) #@UndefinedVariable
        if frame.origin == cv.IPL_ORIGIN_TL: #@UndefinedVariable
            cv.Copy(frame, self._frame) #@UndefinedVariable
        else:
            cv.Flip(frame, self._frame, 0) #@UndefinedVariable
        return IplQImage(self._frame, self._get_current_frame())

    def _get_current_frame(self):
        return cv.GetCaptureProperty(self._capture, cv.CV_CAP_PROP_POS_FRAMES) #@UndefinedVariable

    def get_current_frame(self):
        if self._current < 0:
            return self._get_current_frame()
        else:
            return self._current

    def store_images(self, frame_list):
        self._store.clear()
        for nr in frame_list:
            self.set_current_frame(nr, show=False)
            self._store[nr] = self._buffer[nr]
        return self._store

    def save_images(self, frame_list, destination):
        frame_list = sorted(frame_list)
        filename = os.path.basename(self.path)
        imgs = self.store_images(frame_list)
        for frame, img in imgs.items():
            img.save("%s/%s.%i.png" % (destination,filename, frame), "PNG")

    def set_current_frame(self, value, show=True):
        #print value
        if value not in self._buffer.keys():
            self._buffer.clear()
            frame_number = max(0, value - 100)
            cv.SetCaptureProperty(self._capture, cv.CV_CAP_PROP_POS_FRAMES, frame_number) #@UndefinedVariable
            frame = cv.QueryFrame(self._capture) #@UndefinedVariable
            while (self._get_current_frame() > (value - 50)):
                cv.SetCaptureProperty(self._capture, cv.CV_CAP_PROP_POS_FRAMES, frame_number) #@UndefinedVariable
                frame = cv.QueryFrame(self._capture) #@UndefinedVariable
                frame_number = max (0, frame_number-1)
            while (self._get_current_frame() < (value - 50) ): frame = cv.QueryFrame(self._capture) #@UndefinedVariable
            for i in range(100):
                frame = cv.QueryFrame(self._capture) #@UndefinedVariable
                self._buffer[self._get_current_frame()] = self._build_image(frame)

            #print self._buffer.keys()
        self._current = value
        if show is True:
            self._image = self._buffer[self._current]
            if self.parent is not None:
                self.parent.update()

    def frame_step(self, reverse=False):
        if reverse is True:
            self._current -= 1
        else:
            self._current += 1

        if self._current not in self._buffer.keys():
            self.set_current_frame(self._current)
        else:
            self._image = self._buffer[self._current]
            if self.parent is not None:
                self.parent.update()

    def get_current_image(self):
        return self._image
