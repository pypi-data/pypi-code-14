from concurrent.futures import ThreadPoolExecutor as TPE
from queue import Queue
from time import sleep, time

from os.path import getsize
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .media_info import is_video
from .convert import convert_video


SIZE_CHECK_WAIT = 0.5


def file_size_stable(filename: str, wait: float = SIZE_CHECK_WAIT, previous: int = 0):
    while True:
        sleep(wait)
        filesize = getsize(filename)

        if filesize == previous:
            print(filesize)
            return

        previous = filesize


def consume_video_queue(queue: Queue):
    while True:
        filename = queue.get()

        file_size_stable(filename)


        if is_video(filename):
            convert_video(filename)

        else:
            print(filename, 'not video')


class AddedFileHandler(FileSystemEventHandler):
    def __init__(self, queue: Queue):
        super().__init__()
        self.queue = queue

    def on_created(self, event):
        print(event)

        if event.is_directory:
            return

        self.queue.put(event.src_path)

    def on_moved(self, event):
        self.on_created(event)

    def on_modified(self, event):
        self.on_created(event)


def watch_directory(directory: str):
    observer = Observer()
    queue = Queue()
    handler = AddedFileHandler(queue)

    thread_pool = TPE(1)
    converter_future = thread_pool.submit(consume_video_queue, queue)

    observer.schedule(handler, directory, recursive=True)
    observer.start()

    try:
        while True:
            sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()
    queue.join()
    converter_future.cancel()
    thread_pool.shutdown()

