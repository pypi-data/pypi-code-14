from time import sleep

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from queue import Queue
from concurrent.futures import ThreadPoolExecutor as TPE

from .media_info import get_media_info, get_video_codec
from .convert import convert_video


def is_video(path: str) -> bool:
    try:
        media_info = get_media_info(path)
        print(media_info)

        return bool(get_video_codec(media_info))

    except IOError as e:
        return False


def consume_video_queue(queue: Queue):
    while True:
        video = queue.get()
        convert_video(video)


class AddedFileHandler(FileSystemEventHandler):
    def __init__(self, queue: Queue):
        self.queue = queue

    def on_created(self, event):
        if event.is_directory:
            return

        file = event.src_path

        if is_video(file):
            self.queue.put(file)


class TestHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(event, 'sleeping')
        sleep(5)
        print('woke up')


def watch_directory(dir: str):
    observer = Observer()
    queue = Queue()
    handler = AddedFileHandler(queue)
    thread_pool = TPE(1)
    future = thread_pool.submit(consume_video_queue, queue)

    observer.schedule(handler, dir, recursive=True)
    observer.start()

