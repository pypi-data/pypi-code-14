import os.path

from ..model import itemmodel as im
from ..gui import main_view, cvtools
import videotools
from ..tools import layoutcontainer, moviecontainer
import threading
import time


class DispatcherThread(threading.Thread):

    def __init__(self, controller):
        threading.Thread.__init__(self)
        self.tasks=[]
        self.is_running = True
        self.controller = controller
        self._is_busy = False

    def stop(self):
        self.is_running = False

    def add_task(self, task_nr):
        self.tasks.append(task_nr)


    def run(self):
        while (self.is_running):
            if len(self.tasks) > 0:
                self._is_busy = True
                task = self.tasks.pop(0)
                if task == 0:
                    self.controller._merge_files()
                elif task == 1:
                    self.controller._detect_syncs()
                elif task == 2:
                    self.controller._create_movies()
                self._is_busy = False
            else:
                time.sleep(1)

    def is_busy(self):
        return self._is_busy

class ItemController:
    def __init__(self, model):
        self.model = model
        self.gui = main_view.MainWindow(self.model)
        self.gui.set_listener(self)
        self.dispatcher = DispatcherThread(self)
        self.dispatcher.start()

    def restart_gui(self):
        self.gui = main_view.MainWindow(self.model)
        self.gui.set_listener(self)
        if self.dispatcher.is_busy():
            self.gui.set_busy()

    def gui_shutdown(self):
        self.gui = None

    def add_file(self, container, file_path):
        container.add_file(file_path)

    def remove_file(self, container, a_file):
        container.remove_file(a_file)

    def create_set(self, set_name, layout_name):
        new_set = im.SetItem(set_name)
        new_set.set_layout(self.model.get_layout(layout_name))
        self.model.add_set(new_set)
        new_set.update_status()

    def set_layout(self, set_name, layout_name):
        self.model.get_set(set_name).set_layout(self.model.get_layout(layout_name))

    def merge_files(self):
        self.dispatcher.add_task(0)
        if self.gui is not None: self.gui.set_busy()

    def _merge_files(self):
        for set_name in self.model.get_set_names():
            a_set = self.model.get_set(set_name)
            for container_name in a_set.get_layout().get_container_names():
                container = a_set.get_container(container_name)
                if container.get_status() == 0:
                    file_list = []
                    destination = os.path.join(self.model.get_path(), str(a_set.get_name() + "_" + container.get_name()+".mp4").replace(" ","_"))
                    for idx in range(container.get_file_count()):
                        file_list.append(container.get_file(idx).get_path())
                    container.set_status(1)
                    result = videotools.prepare_videos(file_list, destination, container.use_original())
                    if result is True:
                        container.set_status(2)
                    else:
                        container.set_status(0)
                elif container.get_status() < 0:
                    print "WARNING %s of %s IS NOT VALID! Most likely a file is missing" % (container_name, set_name)

    def sync_video(self,container):
        video = os.path.join(self.model.get_path(), str(container.parent().get_name()+ "_" + container.get_name() + ".mp4").replace(" ","_"))
        container.path = video
        container.set_status(3)
        events = videotools.get_syncs(video)
        for key, value in events.items():
            container.add_sync_event(key, value)
        use = sorted(events, cmp=lambda x,y: cmp (events[x], events[y]), reverse = True)[:2]
        container.set_used_events(sorted(use))
        video_widget = cvtools.CVVideo()
        video_widget.set_capture(video)
        video_widget.save_images(container.get_sync_events().keys(), self.model.get_path())
        container.set_status(4)

    def sync_audio(self, audio, initial_guess = None, force_exact_time = False):
        if audio.container is None:
            print "create container"
            container = tools.audiocontainer.AudioContainer(audio.get_path())
            container.prepare()
            container.init(cut_factor=2)
            if audio.get_status() < 4:
                container.detectSignal(sync_events = 1)
                audio.set_events(container.getSyncTimes())
            audio.container = container
        if force_exact_time is True:
            audio.set_sync(initial_guess)
            audio.container.set_used_sync(initial_guess)
        elif initial_guess is None:
            audio.set_sync(audio.get_events()[0])
            audio.container.set_used_sync(audio.get_events()[0])
        else:
            times = audio.get_events()
            diff = map(lambda x: abs(initial_guess - x), times)
            idxmin = diff.index(sorted(diff)[0])
            audio.set_sync(times[idxmin])
            audio.container.set_used_sync(audio.get_events()[0])
        audio.set_status(4)
        tools.audiocontainer.extractAudioSample(audio.get_path(), audio.get_sync(), 10, audio.get_path()+".sync.wav")

    def detect_syncs(self):
        self.dispatcher.add_task(1)
        if self.gui is not None: self.gui.set_busy()

    def _detect_syncs(self):
        for set_name in self.model.get_set_names():
            a_set = self.model.get_set(set_name)
            for container_name in a_set.get_layout().get_container_names():
                container = a_set.get_container(container_name)
                if container.get_status() == 2:
                    self.sync_video(container)
                elif container.get_status() < 2:
                    print "WARNING %s of %s IS NOT PREPARED!" % (container_name, set_name)

            for audio in a_set.get_audios():
                self.sync_audio(audio)

    def is_busy(self):
        return self.dispatcher.is_busy()

    def create_movies(self):
        self.dispatcher.add_task(2)
        if self.gui is not None: self.gui.set_busy()

    def _create_movies(self):
        for set_name in self.model.get_set_names():
            a_set = self.model.get_set(set_name)
            slayout =  a_set.get_layout()
            path = str(self.model.get_path() + "/" + set_name+".mp4").replace(" ","_")
            vid = layoutcontainer.LayoutContainer(
            str(path),
            slayout.get_width(),
            slayout.get_height(), delete_temp=True)

            for container_name in a_set.get_layout().get_container_names():
                container = a_set.get_container(container_name)
                clayout = slayout.get_container(container_name)
                path = str(self.model.get_path() + "/" + set_name+"_"+container_name + ".mp4").replace(" ","_")
                part = moviecontainer.MovieContainer(str(path))
                part.setImageFormat("png")
                part.setSize(clayout.get_width(), clayout.get_height())
                part.setCrop(0, 0, 0, 0)
                part.set_sync_frames(container.get_used_events())
                vid.addMovie(part, clayout.get_pos_x(), clayout.get_pos_y())
                if container_name == slayout.get_ref_name():
                    print "Reference is " + container_name
                    vid.setReference(part)
                if clayout.use_audio() is True: part.useAudio()

            for audio in a_set.get_audios():
                if audio.container is None:
                    audio.container = tools.audiocontainer.AudioContainer(audio.get_path())
                    audio.container.prepare()
                    audio.container.set_used_sync(audio.get_sync())
                vid.addAudio(audio.container)

            vid.generate(jobs=4)
            vid.clear()
            del vid
