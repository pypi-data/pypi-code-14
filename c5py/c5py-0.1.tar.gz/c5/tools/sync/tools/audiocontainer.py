import numpy
import subprocess
import os
import wave
from scipy import signal
import struct
import getopt
import sys
import time

class AudioContainer:
    def __init__(self, filename, stepsize=120):
        self.__sample = None
        self.__filename =  filename
        self.__tempfile =  ".tmp_audio/" + os.path.splitext(os.path.split(filename)[1])[0] + ".wav"
        self.__data = None
        self.__maxima = []
        self.__energy = None
        self.__kernel = None
        self.__filter = None
        self.__stepsize = stepsize
        self.__frames_to_read = 0
        self.__compression = 0
        self.__kernelsize = 0
        self.__storagesize = 0
        self.__synctimes = [[0,0]]
        self.used_sync = 0

    def prepare(self):
        #create temp folder
        try:

            subprocess.call(["mkdir", "-p", ".tmp_audio"])
        except subprocess.CalledProcessError:
            print "vmerge: could not create audio folder"

    def init(self, cut_factor = 1):
        try:
            subprocess.check_call(["ffmpeg","-i",self.__filename,"-ac","1","-ar","16000","-y",self.__tempfile])
        except:
            print "vmerge: could not create audio tempfile"
            return
        self.__sample = wave.open(self.__tempfile,"r")
        self.__kernel = self.kernel_func(3,54,540)
        self.__compression = self.getSampleRate()/441
        self.__kernelsize = self.__kernel.size * self.__compression
        self.__stepsize = self.__stepsize * self.getSampleRate()
        self.__stepsize = min(self.__stepsize, (self.getSampleCount()-self.__kernelsize))
        self.__storagesize = self.__stepsize + self.__kernelsize

        print "kernelsize: %i" % self.__kernelsize
        print "stepsize: %i" % self.__stepsize
        print "storesize: %i" % self.__storagesize
        print "compression: %i" % self.__compression
        print "bins: %i" % (self.__storagesize / self.__compression)

        #print self.__stepsize
        self.__data = numpy.zeros(self.__storagesize,numpy.dtype('h'))
        if (self.getSampleCount() > self.__storagesize*cut_factor):
            self.__frames_to_read = self.getSampleCount()/cut_factor
        #self.__maxima = numpy.zeros(self.getSampleCount()/self.__stepsize,2)
        bin = self.__sample.readframes(self.__storagesize)
        self.__data = struct.unpack_from("%dh" % (self.__storagesize), bin)
        self.__frames_to_read -= (self.__storagesize)
        del bin

    def setBandPass(self, length, frequency, band):
        nyquist = self.getSampleRate()/2
        freq = frequency / float(nyquist)
        ba = band / float(nyquist)
        wp = [freq - ba, freq + ba]
        ws = [numpy.max([0,wp[0]- 0.1]) , numpy.min([wp[1] + 0.1,1])]
        self.__filter = signal.iirdesign(wp, ws, gstop= 60, gpass=1)

    def loadNext(self):
        if self.__frames_to_read < self.__stepsize:
            return False
        self.__data[0:self.__kernelsize] = self.__data[self.__data.size-self.__kernelsize:]
        bin = self.__sample.readframes(self.__stepsize)
        self.__data[self.__kernelsize:] = struct.unpack_from("%dh" % self.__stepsize, bin)
        del bin
        self.__frames_to_read -= self.__stepsize
        print "%i frames to read" % self.__frames_to_read
        return True

    def close(self):
        self.__sample.close()

    def getData(self):
        return self.__data

    def getSampleCount(self):
        return self.__sample.getnframes()

    def getSampleRate(self):
        return self.__sample.getframerate()

    def getChannelCount(self):
        return self.__sample.getnchannels()

    def getAudioName(self):
        return self.__tempfile

    def calcEnergy(self, steps = 1,  cutoff = 1500):
        self.__energy = numpy.zeros(self.__storagesize / steps,numpy.float64)
        for i in range(0,self.__storagesize / steps):
            ran = self.__data[i*steps:(i+1)*steps]
            ran = numpy.abs(ran)
            val = numpy.sum(numpy.abs(ran))
            self.__energy[i] = min(cutoff, val)

    def kernel_func(self, os_count,width, distance, negative=True):
        generated = numpy.zeros((os_count-1) * distance + width)
        window = signal.triang(width)
        nwindow = signal.triang(7*width)
        for i in range(os_count):
            spot = i * distance
            generated[spot:spot+width] = window
            if negative is True and (i < os_count - 1):
                spot += 0.5 * distance
                generated[spot-3*width:spot+4*width] = -nwindow
        return generated;

    def detectSignal(self, sync_events = 1):
        self.setBandPass(1001,2870,50)
        self.detectionStep()
        while self.loadNext() is True:
            self.detectionStep()

        self.__synctimes = []
        for idx,val in enumerate(self.__maxima):
                key = (val[0] * self.__compression + idx*(self.__stepsize)) / float(self.getSampleRate())
                val = val[1]
                self.__synctimes.append((key,val))
        self.__synctimes = sorted(self.__synctimes,key=lambda x: x[1],reverse=True)
        print self.__synctimes
        print self.__maxima
        self.used_sync = self.__synctimes[0][0]

    def detectionStep(self):
        self.__data = signal.lfilter(self.__filter[0],self.__filter[1],self.__data)
        self.calcEnergy(self.__compression)
        res = signal.convolve(self.__energy,self.__kernel)
        idx = numpy.argmax(res)
        self.__maxima.append([(idx-self.__kernel.size),res[idx]])


    def getSyncTimes(self):
        return list(numpy.array(self.__synctimes)[:,0])

    def set_used_sync(self, time):
        self.used_sync = time

    def createSoundFile(self, offset):
        try:
            print self.__synctimes
            subprocess.check_call(["ffmpeg","-i",self.__filename,"-y",self.__tempfile])
            time.sleep(2)
            if (offset > self.used_sync):
                cl = ["sox",self.__tempfile, ".tmp_audio/long.wav", "pad", str((offset-self.used_sync))]
                print cl
                subprocess.check_call(cl)
                subprocess.check_call(["mv",".tmp_audio/long.wav",self.__tempfile])
        except subprocess.CalledProcessError:
            print "vmerge: could not create audio tempfile"

def extractAudioSample(filename,offset,duration,destination):
    path = os.path.split(filename)
    cmd = ["ffmpeg","-i", filename,"-ss",str(offset-(duration/2.0)),"-t",str(duration),"-acodec","copy","-vn","-y",destination]
    print cmd
    subprocess.call(cmd)

def usage():
    print "have to write usage some day"
    sys.exit(1)

def main(argv):
    import sys
    import pylab

    use_pylab = ("pylab" in sys.modules)

    first_frame = last_frame = 0
    try:
        opts, args = getopt.getopt(argv, "hf:", ["help", "filename="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-f", "--filename"):
            filename = arg
    try:
        filename
    except NameError:
        print "you have to pass the wav file path"
        usage()
        sys.exit(1)

    a1 = AudioContainer(filename)
    a1.prepare()
    a1.init(cut_factor=2)
    a1.detectSignal(sync_events = 1)
    print a1.getSyncTimes()[0]

if __name__ == "__main__":
    main(sys.argv[1:])
