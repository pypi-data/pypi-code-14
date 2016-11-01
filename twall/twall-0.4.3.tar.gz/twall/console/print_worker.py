import threading
import queue


class PrintWorker(threading.Thread):
    def __init__(self, config, q):
        super().__init__()
        self.config = config
        self.queue = q
        self.stopped = False

    def run(self):
        print('Starting the printer worker')
        while not self.stopped:
            try:
                tweet = self.queue.get(timeout=1)
                self.print_tweet(tweet)
            except queue.Empty:
                pass

    @staticmethod
    def print_tweet(tweet):
        print('\n@' + tweet['user']['screen_name'])
        print(tweet['text'])

    def stop(self):
        self.stopped = True
