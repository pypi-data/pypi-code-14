import configparser
import queue
from . import PrintWorker, WallWorker
import os


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def run_console(query, count, interval, result_type, **kwargs):
    if not os.path.exists(kwargs['auth_file']):
        raise FileNotFoundError('Authentication file doesn\'t exist. I don\'t have Twitter OAuth data.')

    config = _read_config(kwargs['auth_file'])

    print('Starting the Twitter Wall with query {}. Press Q<ENTER> to exit.'.format(query))

    q = queue.Queue()
    tweet_worker = WallWorker(config, q, query, interval, result_type, count)
    print_worker = PrintWorker(config, q)

    tweet_worker.start()
    print_worker.start()

    inp = None
    while inp != 'Q':
        inp = input()

    tweet_worker.stop()
    print_worker.stop()


def _read_config(config_file_path):
    config = configparser.ConfigParser()
    config.read([config_file_path, os.path.join(__location__, '../settings.cfg')])
    return config
