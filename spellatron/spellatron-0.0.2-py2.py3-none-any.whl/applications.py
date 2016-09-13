import os
import logging

from tornado.web import Application

here = lambda *x: os.path.join(os.path.dirname(__file__), *x)


class DefaultApplication(Application):

    def __init__(self, **kwargs):
        handlers = []
        super(DefaultApplication, self).__init__(handlers, **kwargs)
