import cv2
import numpy as np
import scipy.signal


class VisualAnalysis:

    @staticmethod
    def detect_sync(file_name, stepsize=30):
        #hist = VisualAnalysis.calc_hist(file_name)
        hist = np.loadtxt("/Volumes/Elements/c5/2014-04_ARInterception/trial506/trial506_cam3.mp4.log")
        y = VisualAnalysis.sync_function()
        z = np.zeros((hist.shape[0]-y.shape[0]+1))
        for i in range(3):
            z = z + VisualAnalysis.calc_channel_corr(hist[:,i], y[:,i])

        sync_at = np.where(z > 2)[0]
        events = {}
        last = 0
        for s in sync_at:
            if (s-last) > 10:
                events[s*2] = 3.0
                last = s
        return events

    @staticmethod
    def sync_function(width=8):
        framesize = 45
        pen = -1
        enh = 3
        result = np.ones((framesize, 3)) * pen
        result[0:0+width/2,0] = enh;
        result[15-width/2:15+width/2,1] = enh;
        result[30-width/2:30+width/2,2] = enh;
        return result;

    @staticmethod
    def calc_channel_corr(channel, ref):
        idx = scipy.signal.find_peaks_cwt(channel, np.arange(2,5), min_snr=3)
        peaks = np.zeros((channel.shape[0]))
        peaks[idx] = 1
        corr = np.correlate(peaks, ref, mode='valid')
        return scipy.stats.threshold(corr, threshmax=1, newval=1)

    @staticmethod
    def calc_hist(file_name):
        res = []
        capture = cv2.VideoCapture(file_name)
        idx = 0
        while capture.isOpened():
            if idx % 2 == 0:
                ret, img = capture.read()
                if img is not None:
                    res.append(calc_val(img,15))
                else:
                    break
            else:
                capture.grab()
            idx += 1
        hist = np.array(res)
        with open(file_name + '.log', 'w') as f:
            np.savetxt(f, hist)
        return hist


def calc_val(img, size=20):
    height, width = img.shape[:2]
    img_reduced = cv2.resize(img, (width/5, height/5), interpolation=cv2.INTER_AREA)
    height, width = img_reduced.shape[:2]
    img_roi = img_reduced[height/3:height/3*2, width/3:width/3*2]
    b,g,r = cv2.split(img_roi)
    hist_r = cv2.calcHist([r],[0],None,[size],[0,255])
    hist_g = cv2.calcHist([g],[0],None,[size],[0,255])
    hist_b = cv2.calcHist([b],[0],None,[size],[0,255])
    return hist_r[-2:].sum(), hist_g[-2:].sum(), hist_b[-2:].sum()
