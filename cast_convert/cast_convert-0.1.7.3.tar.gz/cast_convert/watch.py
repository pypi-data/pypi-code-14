from concurrent.futures import ThreadPoolExecutor as TPE
from os.path import getsize
from queue import Queue
from time import sleep

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from cast_convert.preferences import FILESIZE_CHECK_WAIT
from .convert import convert_video
from .media_info import is_video


def wait_for_stable_size(filename: str, wait: float = FILESIZE_CHECK_WAIT, previous: int = -1):
    while True:
        sleep(wait)

        filesize = getsize(filename)

        if filesize == previous:
            return filesize

        previous = filesize


def consume_video_queue(queue: Queue, debug: bool = False):
    while True:
        filename = queue.get()

        if debug:
            print("Getting filesize")

        filesize = wait_for_stable_size(filename)
        file_is_vid = is_video(filename)

        if debug:
            print(filesize)
            print(file_is_vid)

        if file_is_vid:
            print(convert_video(filename))

        else:
            print(filename, 'not video')


class AddedFileHandler(PatternMatchingEventHandler):
    def __init__(self, queue: Queue, *args, debug: bool=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = queue
        self.debug = debug

    def on_moved(self, event):
        if event.is_directory:
            return

        if self.debug:
            print(event)

        self.queue.put(event.dest_path)

    def on_created(self, event):
        if event.is_directory:
            return

        if self.debug:
            print(event)

        self.queue.put(event.src_path)


def watch_directory(directory: str, ignore_patterns: tuple=tuple(), debug: bool=True):
    observer = Observer()
    queue = Queue()
    handler = AddedFileHandler(queue, ignore_patterns=ignore_patterns, debug=debug)

    thread_pool = TPE(1)
    converter_future = thread_pool.submit(consume_video_queue, queue)

    print("Watching %s for new videos..." % directory)

    observer.schedule(handler, directory, recursive=True)
    observer.start()

    try:
        while True:
            sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    try:
        observer.join()
        queue.join()
        converter_future.cancel()
        thread_pool.shutdown(wait=0.1)

    except KeyboardInterrupt:
        exit()

