"""
Includes the worker that prints tweets from a queue to standard output.
"""

import threading
import queue
import pprint


class PrintWorker(threading.Thread):
    """
    This Worker will print new tweets returned from the Twitter Search API to standard output.
    The tweets have to be placed in the :mod:`queue` that is passed to the worker at construction time.
    """

    def __init__(self, config, q):
        """
        Constructs a new PrintWorker.

        :param config: A :mod:`configparser` instance containing the application's loaded config data.
        :param q: The :mod:`queue` that will contain tweets to be printed.
        """
        super().__init__()
        self.config = config
        self.queue = q
        self.stopped = False

    def run(self):
        """
        Launches the worker on a new thread.
        """
        print('Starting the printer worker')
        while not self.stopped:
            try:
                tweet = self.queue.get(timeout=1)
                self.print_tweet(tweet)
            except queue.Empty:
                pass

    @staticmethod
    def print_tweet(tweet):
        """
        Prints a tweet to standard output. Doesn't do anything with entities, just prints the screen name and text.

        :param tweet: A tweet, as returned by the Twitter Search API.
        """
        # print('\n@' + tweet['user']['screen_name'])
        # print(tweet['text'])

        pprint.pprint(tweet)

    def stop(self):
        """
        Stops the worker. Note that the run loop may be stuck waiting for a new tweet in the queue and the thread may
        not actually exit until the wait timeout occurs.
        """
        self.stopped = True
