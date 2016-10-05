import subprocess
import os.path

from audiocontainer import AudioContainer


class MovieContainer(object):
    def __init__(self, path):
        self.__path = path
        self.__moviename = os.path.basename(path)
        self.pos_x = 0
        self.pos_y = 0
        self.__imageformat = "png"
        self.__tempfolder =  os.path.dirname(path) + "/.tmp_" + self.__moviename
        self.__width = None
        self.__height = None
        self.__crop_left = self.__crop_top = self.__crop_right = self.__crop_botton = 0
        self.__imageCount = 0
        self.__syncframes = []
        self.__audio = None
        self.__stepsize = 1
        subprocess.call(["mkdir", "-p", self.__tempfolder])

    def setSize(self, width, height):
        self.__width = width
        self.__height = height

    def setImageFormat(self, imageformat):
        self.__imageformat = imageformat

    def useAudio(self):
        self.__audio = AudioContainer(self.__path)

    def prepareAudio(self, offset, skipAudioSync = False):
        if self.__audio is None:
            return None
        self.__audio.prepare()

        if skipAudioSync is True:
            sync = False
        else:
            self.__audio.init(2)
            sync = self.__audio.detectSignal()

        if sync is True:
            self.__audio.createSoundFile(offset/25.0)
        else:
            self.__audio.createSoundFile((offset-self.__syncframes[0])/25.0)

        return self.__audio.getAudioName()

    def setCrop(self, left, top, right, bottom):
        self.__crop_left = left
        self.__crop_top = top
        self.__crop_right = right
        self.__crop_botton = bottom


    def cropAndResize(self, createImages=True):
        if os.path.exists("%s/%s.1.%s" % (self.__tempfolder,self.__moviename,self.__imageformat)) is True:
            print "found extracted images... skipping"
            return

        width_cut = self.__crop_left + self.__crop_right
        height_cut = self.__crop_top + self.__crop_botton

        cmd = ["ffmpeg", "-i", self.__path,
        "-vf", "crop=iw-%d:ih-%d:%d:%d,scale=%d:%d" % (width_cut, height_cut, self.__crop_left, self.__crop_top, self.__width, self.__height),
        "{0}/{1}.%d.{2}".format(self.__tempfolder,self.__moviename,self.__imageformat)]
        print cmd
        subprocess.call(cmd)
        self.analyzeData()

    def analyzeData(self):
        ## get image count
        call = subprocess.Popen(["find " +  self.__tempfolder + " -iname \"*." + self.__imageformat + "\" |  grep -c . "],shell=True,stdout=subprocess.PIPE)
        output = call.communicate()
        self.__imageCount = int(output[0])
        print "vmerge: " + str(self.__imageCount) + " frames exported from file " + self.__moviename
        ## calculate size
        call = subprocess.Popen(["du -ch " + self.__tempfolder], shell=True, stdout=subprocess.PIPE)
        call.wait()
        output = call.communicate()
        size = output[0].split()[0]
        print "vmerge: disk space used: " + str(size)

    def clear(self):
        print "delete movie"
        try:
            subprocess.call(["rm", "-R", self.__tempfolder])
        except subprocess.CalledProcessError:
            print 'vmerge: warning, could not remove temp folder.'

    def prepare(self):
        print "prepare movie %s ..." % (self.__moviename)
        self.cropAndResize()
        self.analyzeData()


    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def alterStepSize(self, stepsize):
        self.__stepsize = stepsize
        self.__syncframes = map(lambda x:x/stepsize,self.__syncframes)

    def getImage(self, imagenumber, offset):
        imagenumber = int((imagenumber - offset + self.__syncframes[0]) * self.__stepsize)
        #print imagenumber
        if (imagenumber > 0 and imagenumber < self.__imageCount):
            return "%s/%s.%d.%s" % (self.__tempfolder, self.__moviename, imagenumber, self.__imageformat)
        else:
            return None

    def getImageCount(self):
        return int(self.__imageCount/self.__stepsize)

    def set_sync_frames(self, frames):
        self.__syncframes = frames

    def getSyncFrames(self):
        syncs = map(lambda x:int(x),self.__syncframes)
        return syncs

    def getMovieName(self):
        return self.__moviename

    def getTempfolderName(self):
        return self.__tempfolder
