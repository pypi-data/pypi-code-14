# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import datetime

from flask import request, Response
from flask._compat import text_type, string_types

from palmer.utils import http_statuses


class APIResponse(Response):

    def __init__(self, content=None, *args, **kwargs):
        super(APIResponse, self).__init__(None, *args, **kwargs)
        self.response_at = datetime.datetime.utcnow()

        media_type = None
        if isinstance(content, (list, dict, text_type, string_types)):
            renderer = request.renderer
            media_type = renderer.media_type
            if self.status_code == http_statuses.HTTP_204_NO_CONTENT:
                self.status_code = http_statuses.HTTP_200_OK
            content = self.get_cleaned_content(content)
            content = renderer.render(content, media_type)

        if content is None:
            content = []
        if isinstance(content, (text_type, bytes, bytearray)):
            self.set_data(content)
        else:
            self.response = content

        if media_type is not None:
            self.headers['Content-Type'] = str(media_type)

    def get_cleaned_content(self, content):
        return dict(
            request_at=request.request_at,
            response_at=self.response_at,
            status_code=self.status_code,
            result=content
        )
