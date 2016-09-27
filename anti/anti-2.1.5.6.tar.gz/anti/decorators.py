# -*- coding:utf-8 -*-

import time
import logging

TSLEEP = 10
NUMBER_OF_EXCEPTIONS = 1


def fail_counter(fn):
    def wrapped(self, *args, **kwargs):
        self.exceptions = 0
        while self.exceptions < NUMBER_OF_EXCEPTIONS:
            try:
                return fn(self, *args, **kwargs)
            except Exception:
                logging.warning('DecoratorError: number of exceptions is %d' % self.exceptions)
                self.exceptions += 1
                if self.exceptions == NUMBER_OF_EXCEPTIONS:
                    raise
                time.sleep(TSLEEP)
    return wrapped
