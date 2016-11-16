# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import datetime

from flask import Request

from palmer.config import default_config


class APIRequest(Request):
    renderer_class = default_config.RENDERER_CLASS

    def __init__(self, *args, **kwargs):
        self.request_at = datetime.datetime.utcnow()
        super(APIRequest, self).__init__(*args, **kwargs)

    @property
    def form_data(self):
        data = self.form.copy()
        if self.files:
            data.update(self.files)
        return data

    @property
    def renderer(self):
        if not hasattr(self, '_renderer'):
            self._renderer = self.renderer_class()
        return self._renderer

    @renderer.setter
    def renderer(self, renderer):
        self._renderer = renderer
