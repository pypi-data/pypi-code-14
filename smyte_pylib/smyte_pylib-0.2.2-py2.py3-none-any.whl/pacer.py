from __future__ import absolute_import

import time


class Pacer(object):
    'Ensure we commit every `limit` numbers or `timeout` seconds'

    def __init__(self, limit, timeout):
        self.limit = limit
        self.timeout = timeout
        self.current = limit if limit else 0
        self.next_commit = time.time()

    def test(self):
        self.current += 1

        if (
            (time.time() > self.next_commit) or
            (self.limit and self.current >= self.limit)
        ):
            self.current = 0
            self.next_commit = time.time() + self.timeout
            return True
        return False
