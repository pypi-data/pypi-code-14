import time
import yaml
import os
import sys

# Singleton metaclass

class Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class EggTimer:
    def __init__(self, timeout):
        self.timeout = timeout

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, *_):
        pass

    def elapsed(self):
        return (time.time() - self.start_time) > self.timeout


def do_in_intervals(timeout, interval, report_interval, action, sleep_func):
    with EggTimer(timeout) as timer:
        time_left = timeout * report_interval
        while not timer.elapsed():
            action(
                int((time_left / report_interval) + 1)
            )
            sleep_func(interval)
            time_left -= interval


def yaml_from_file(path):
    with open(path, 'rt') as f:
        return yaml.load(f)


def timestamp_with_offset(offset=None):
    if not offset:
        offset = time.time()

    def gen_time_stamp():
        now = time.time()
        return now, now - offset

    return gen_time_stamp


def gen_filename(base_name):
    return '{}.{}'.format(
            base_name,
            time.strftime("%Y%m%d%H%M%S")
    )


def join_path(path, base_name):
    if not os.path.exists(path):
        os.mkdir(path)

    return os.path.join(
        path,
        base_name
    )


def get_os():
    if sys.platform.startswith('linux'):  # for Linux using the X Server
        return 'linux'
    elif sys.platform == "win32":  # for Windows
        return 'windows'
    elif sys.platform == "darwin":  # for MacOS
        return 'mac'
