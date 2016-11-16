# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import datetime
import decimal

import msgpack
from flask.json import dumps as json_dumps


class MessagePackEncoder(object):
    def encode(self, obj):
        if isinstance(obj, datetime.datetime):
            return {'__class__': 'datetime', 'as_str': obj.isoformat()}
        elif isinstance(obj, datetime.date):
            return {'__class__': 'date', 'as_str': obj.isoformat()}
        elif isinstance(obj, datetime.time):
            return {'__class__': 'time', 'as_str': obj.isoformat()}
        elif isinstance(obj, decimal.Decimal):
            return {'__class__': 'decimal', 'as_str': str(obj)}
        else:
            return obj


class BaseRenderer(object):
    """
    All renderers should extend this class, setting the `media_type`
    and `format` attributes, and override the `.render()` method.
    """
    media_type = None
    format = None
    charset = 'utf-8'
    render_style = 'text'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        raise NotImplementedError('Renderer class requires .render() to be implemented')


class JSONRenderer(BaseRenderer):
    """
    Renderer which serializes to JSON.
    """
    media_type = 'application/json'
    format = 'json'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into JSON, returning a bytestring.
        """
        return json_dumps(data, ensure_ascii=False)


class MessagePackRenderer(BaseRenderer):
    """
    Renderer which serializes to MessagePack.
    """
    media_type = 'application/msgpack'
    format = 'msgpack'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into MessagePack, returning a bytes.
        """
        if data is None:
            return ''
        return msgpack.packb(data, default=MessagePackEncoder().encode)
