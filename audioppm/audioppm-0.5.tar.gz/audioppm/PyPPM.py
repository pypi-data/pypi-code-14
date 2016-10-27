import math
import pyaudio
import threading
import time


class ppmGenerator (threading.Thread):   

    def __init__(self):
        threading.Thread.__init__(self)
        self.BITRATE = 44100 #samples per second    
        self.MINVALUE = 0
        self.MAXVALUE = 255
        self.lengths = [0,0,0,0,0,0,0,0]
        self.stopped = False
        self.framemaker()
        self.p = pyaudio.PyAudio()
        print self.p.get_default_output_device_info()
        self.stream = self.p.open(format = self.p.get_format_from_width(1),
           channels = 1,
           rate = self.BITRATE,
           output = True)

    def run(self):
        while(not self.stopped):
            self.write()
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def stop(self):
        self.stopped = True    #writes the current frame to the stream

    def write(self):
        self.stream.write(self.frame)    #sets the channel values

    def set_channel_values(self,lengths):
        self.lengths = lengths
        self.framemaker()    #makes string that will set the level of the output for a certain length of time, in milliseconds

    def set_channel_value(self, channel, value):
        self.lengths[channel] = value

    def halfpulsemaker(self,length,level):
        r = ''
        l = (length  * self.BITRATE)/1000
        for i in range(int(l)):
            r += chr(level)
        return r    #makes a pulse of a given length, in milliseconds

    def pulsemaker(self,length):
        return self.halfpulsemaker(0.25,self.MINVALUE) + self.halfpulsemaker(length - .25, self.MAXVALUE)    #takes in an array of pulse lengths, makes a full frame out of them

    def framemaker(self):
        totallength = 0
        r = ''
        for i in range(0,8):
            totallength += self.lengths[i]
            r += self.pulsemaker(self.lengths[i])
        totallength += 1
        r += self.pulsemaker(1)
        r = self.halfpulsemaker(22.5 - totallength,128) + r
        self.frame = r

    def write_multiframe(self, n):
        frames = self.frame*n
        self.stream.write(frames)