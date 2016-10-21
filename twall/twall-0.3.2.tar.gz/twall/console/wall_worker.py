import threading
import datetime
import time
from ..twitter import load_tweets, twitter_session


class WallWorker(threading.Thread):
    def __init__(self, config, queue, query, interval, result_type, initial_count=10):
        super().__init__()
        self.config = config
        self.queue = queue
        self.query = query
        self.result_type = result_type
        self.initial_count = initial_count
        self.interval = datetime.timedelta(seconds=interval)
        self.stopped = False

    def run(self):
        print('Starting the wall worker')
        session = twitter_session(self.config)
        count = self.initial_count
        max_tweet_id = None
        last_request_time = datetime.datetime.fromtimestamp(0)

        while not self.stopped:

            elapsed = datetime.datetime.now() - last_request_time
            if elapsed < self.interval:
                time.sleep(1)
            else:
                tweets = load_tweets(session, self.config, self.query, self.result_type, count, max_tweet_id)
                for tw in tweets:
                    self.queue.put(tw)

                if len(tweets) > 0:
                    max_tweet_id = max(tweets, key=lambda t: t['id'])['id']

                last_request_time = datetime.datetime.now()
                count = None

    def stop(self):
        self.stopped = True
