"""
Includes code that launches the console version of the application.
"""

import queue
from twall.console import PrintWorker, WallWorker
import twall
import os


def run_console(query, count, interval, result_type, auth_file):
    """
    Launches the console application that searches for tweets by a specified query string and displays them in
    the terminal in real-time. This method spawns two worker threads - :class:`~twall.console.WallWorker` for polling
    Twitter and :class:`~twall.console.PrintWorker` for printing new tweets. It waits until the character ``Q`` is
    read from standard input, then terminates both workers and itself.

    :param query: The query to Twitter's Search API.
    :param count: The number of older tweets to load at startup.
    :param interval: The polling interval for new tweets. Make sure to se this to a value that doesn't cause the application to overrun its API limits.
    :param result_type: One of ``recent``, ``mixed`` or ``popular``, specifying which type of tweets should be returned.
    :param auth_file: The location of the file containing Twitter OAuth credentials for the application to use.
    :raises FileNotFoundError: Raised if the ``auth_file`` cannot be found.
    """
    if not os.path.exists(auth_file):
        raise FileNotFoundError('Authentication file doesn\'t exist. I don\'t have Twitter OAuth data.')

    config = twall.read_config(auth_file)

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

