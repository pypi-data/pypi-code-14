"""
Includes the worker that periodically polls the Twitter API for new tweets and saves them in a queue.
"""

import threading
import datetime
import time
from twall.twitter import load_tweets, twitter_session


class WallWorker(threading.Thread):
    """
    This worker will periodically load tweets from the Twitter Search API. The first request will load a specified
    number of old tweets, each subsequent request will only fetch tweets more recent than the most recent tweet that
    has already been returned. The tweets will be placed in the :mod:`queue` that is passed to the worker at
    construction time.
    """

    def __init__(self, config, queue, query, interval, result_type, initial_count=10):
        """
        Constructs a new WallWorker.

        :param config: A :mod:`configparser` instance containing the application's loaded config data.
        :param queue: The :mod:`queue` that will contain loaded tweets.
        :param query: The search query.
        :param interval: The interval between each successive Twitter API request in seconds.
        :param result_type: One of ``recent``, ``mixed`` or ``popular``, specifying which type of tweets should be returned.
        :param initial_count: The number of older tweets to load at startup.
        """

        super().__init__()
        self.config = config
        self.queue = queue
        self.query = query
        self.result_type = result_type
        self.count = initial_count
        self.interval = datetime.timedelta(seconds=interval)
        self.stopped = False
        self.max_tweet_id = None

    def run(self):
        """
        Launches the worker on a new thread.
        """
        print('Starting the wall worker')
        session = twitter_session(self.config)
        last_request_time = datetime.datetime.fromtimestamp(0)

        while not self.stopped:

            elapsed = datetime.datetime.now() - last_request_time
            if elapsed < self.interval:
                time.sleep(1)
            else:
                self._load_tweets(session)
                last_request_time = datetime.datetime.now()

    def _load_tweets(self, session):
        tweets = load_tweets(session, self.config, self.query, self.result_type, self.count, self.max_tweet_id)
        for tw in tweets:
            self.queue.put(tw)

        if len(tweets) > 0:
            self.max_tweet_id = max(tweets, key=lambda t: t['id'])['id']

        self.count = None

    def stop(self):
        """
        Stops the worker. Note that the run loop may be stuck waiting for a response or sleeping and the thread may
        not actually exit until the blocking operation finishes.
        """
        self.stopped = True
