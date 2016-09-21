# -*- coding: utf-8 -*-
class FeedException(Exception):
    def __init__(self, exc):
        super(FeedException, self).__init__('%s: %s' % (exc.__class__, exc))
        self.original_exception = exc
