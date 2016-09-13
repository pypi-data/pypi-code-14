import collections
import os
import re

from tornado.web import Application
from tornado.options import options

from . import checker
from . import handlers as api_handlers

here = lambda *x: os.path.join(os.path.dirname(__file__), *x)


class DefaultApplication(Application):

    def get_data_path(self):
        return options.path or here('data', 'data.txt')

    def setup(self):
        data_path = self.get_data_path()

        with open(data_path) as f:
            raw_data = re.findall(r'\w+', f.read().lower())
            dictionary = collections.Counter(raw_data)

        self.correction_service = checker.CorrectionService(dictionary)

    def __init__(self, **kwargs):
        handlers = [
            (r'/correction/', api_handlers.CorrectionHandler),
        ]
        super(DefaultApplication, self).__init__(handlers, **kwargs)
