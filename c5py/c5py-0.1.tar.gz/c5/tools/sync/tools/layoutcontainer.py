import subprocess
import sys
import threading
import time
import os.path

class MoviePreparator(threading.Thread):
    def prepareMovie(self, movie, imageformat):
        self.__movie = movie
        self.__format = imageformat

    def run(self):
        self.__movie.prepare()

class ImageMerger(threading.Thread):    
    def setOffset(self, offset):
        self.__offset = offset

    def setMovies(self, movies):
        self.__movies = movies

    def setRange(self, begin, end):
        self.__begin = begin
        self.__end = end

    def setSize(self, width, height):
        self.__width = width
        self.__height = height

    def setFileInfo(self, temp_folder, file_name, iformat):
        self.tempfolder = temp_folder
        self.imageformat = iformat
        self.filename = file_name

    def run(self):
        for i in range(self.__begin, self.__end):
            #sys.stdout.write("\r Merge: %i done..." % (int((i-self.__begin)*100/self.__end-self.__begin)))
            #sys.stdout.flush()
            if os.path.exists(self.tempfolder + "/" + self.filename + "." + str(i+1) + "." + self.imageformat) is True:
                continue

            imagemagick_cmd = "convert -size " + str(self.__width) + "x" + str(self.__height)
            imagemagick_cmd += " xc:black"
            for movie in self.__movies:
                if movie.getImage(i+1,self.__offset) is None:
                    continue
                imagemagick_cmd += " -draw "
                imagemagick_cmd += "\"image over "
                imagemagick_cmd += str(movie.pos_x) + "," + str(movie.pos_y) + " 0,0 \'"
                imagemagick_cmd += movie.getImage(i+1,self.__offset)
                imagemagick_cmd +=  "\'\""
            imagemagick_cmd += " " + self.tempfolder + "/" + self.filename + "." + str(i+1) + "." + self.imageformat
            #print imagemagick_cmd
            subprocess.call(imagemagick_cmd, shell=True)

class MagickCaller(threading.Thread):
    def set_command(self, command):
        self.command = command

    def run(self):
        subprocess.call(self.command, shell=True)


class LayoutContainer(object):
    def __init__(self, file_path, width, height, delete_temp = True):
        self.path = file_path
        self.filename = os.path.basename(file_path)
        self.tempfolder = os.path.dirname(file_path) + "/.tmp_" + self.filename
        self.imageformat = "png"
        self.__width = width
        self.__height = height
        self.__movies = []
        self.__audio = []
        self.__offset = 0
        self.__delete_tmp = delete_temp
        self.__thread_container = []
        self.__jobs = 1
        self.__reference = None
        # create temp folder:
        subprocess.call(["mkdir", "-p", self.tempfolder])

    def clear(self):
        if self.__delete_tmp is True:
            for movie in self.__movies:
                movie.clear()
            try:
                print "delete tmp files"
                subprocess.call(["rm", "-R", self.tempfolder])
            except subprocess.CalledProcessError:
                print 'vmerge: warning, could not remove temp folder.'

    def create_movie(self):
        # turn images into a video:
        ffmpeg_call = "ffmpeg -f image2 -r 25 -i " + self.tempfolder + "/" + self.filename + ".%d." + self.imageformat
        audiostreams = 0

        for movie in self.__movies:
            audioname = movie.prepareAudio(self.__offset, skipAudioSync=True)
            if audioname is not None:
                ffmpeg_call += " -i %s" % (audioname)
                audiostreams += 1

        for audio in self.__audio:
            audio.createSoundFile(self.__offset/25.0)
            ffmpeg_call += " -i %s" % (audio.getAudioName())
            audiostreams += 1

        ffmpeg_call += " -map 0:0"
        for idx in range(audiostreams):
            ffmpeg_call += " -map %i:0" % ((idx+1))

        ffmpeg_call += " -c:v libx264 -preset slow -pix_fmt yuv420p -y " + self.path
        print ffmpeg_call
        subprocess.check_call(ffmpeg_call, shell=True)

    def setReference(self, movie):
        self.__reference = movie

    def merge_images(self):
        # determine minimal frame count:
        max_frame_count = 0
        max_sync_frame = 0

        if self.__reference is not None:
            ref_diff = self.__reference.getSyncFrames()[1] - self.__reference.getSyncFrames()[0]
        else:
            ref_diff = 0

        for movie in self.__movies:
            if ref_diff > 0:
                diff = movie.getSyncFrames()[1] - movie.getSyncFrames()[0]
                movie.alterStepSize(float(diff)/ref_diff)
            if max_sync_frame < movie.getSyncFrames()[0]:
                max_sync_frame = movie.getSyncFrames()[0]
        self.__offset = max_sync_frame

        for movie in self.__movies:
            frames_after_sync = movie.getImageCount() - movie.getSyncFrames()[0]
            if max_frame_count < frames_after_sync:
                max_frame_count = frames_after_sync

        max_frame_count += max_sync_frame

        print 'vmerge: max frame count of input videos: ' + str(max_frame_count)
        print 'vmerge: max sync frame: ' + str(max_sync_frame)

        # merge images:
        print 'vmerge: merging images (this may take a while)'

        steps = max_frame_count/(self.__jobs*2)

        for i in range(max_frame_count):
            if os.path.exists(self.tempfolder + "/" + self.filename + "." + str(i+1) + "." + self.imageformat) is True:
                continue
            imagemagick_cmd = "convert -size " + str(self.__width) + "x" + str(self.__height)
            imagemagick_cmd += " xc:black"
            for movie in self.__movies:
                if movie.getImage(i+1,self.__offset) is None:
                    continue
                imagemagick_cmd += " -draw "
                imagemagick_cmd += "\"image over "
                imagemagick_cmd += str(movie.pos_x) + "," + str(movie.pos_y) + " 0,0 \'"
                imagemagick_cmd += movie.getImage(i+1,self.__offset)
                imagemagick_cmd +=  "\'\""
            imagemagick_cmd += " " + self.tempfolder + "/" + self.filename + "." + str(i+1) + "." + self.imageformat
            caller = MagickCaller()
            caller.set_command(imagemagick_cmd)
            caller.start()
            while (threading.active_count() > 8):
                time.sleep(0.3)

    def prepareMovies(self, jobs):
        self.__jobs = jobs
        # prepare video files:
        self.__thread_container = []

        for movie in self.__movies:
            while (len(self.__thread_container) >= self.__jobs):
                for thread in self.__thread_container:
                    if thread.isAlive() is False:
                        self.__thread_container.remove(thread)
                        del thread
                    else:
                        time.sleep(1)
            thread = MoviePreparator()
            thread.prepareMovie(movie, self.imageformat)
            self.__thread_container.append(thread)
            thread.start()

        while len(self.__thread_container) > 0:
            for thread in self.__thread_container:
                if thread.isAlive() is True:
                    thread.join()
                self.__thread_container.remove(thread)
                del thread

    def generate(self, jobs):
        self.prepareMovies(jobs)
        self.merge_images()
        self.create_movie()

    def addMovie(self, movie_container_object, pos_x, pos_y):
        self.__movies.append(movie_container_object)
        movie_container_object.pos_x = pos_x
        movie_container_object.pos_y = pos_y

    def addAudio(self, container_object):
        self.__audio.append(container_object)
