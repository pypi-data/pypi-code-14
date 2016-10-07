"""
    flask_responseext.response

    Contains Response subclass of Flask Response object
"""


import json

from flask import Response as FlaskResponse
from flask import json as flask_json


class Response(FlaskResponse):
    """Flask Response subclass providing ability to chain
    setter methods"""
    
    JSON_MIMETYPE = 'application/json'

    def __init__(self, rv=None, **kwargs):
        self.ext_paylod = rv
        FlaskResponse.__init__(self, rv, **kwargs)

    def set_status(self, status_code):
        self.status_code = status_code

        return self

    def set_headers(self, headers):
        """Set dict of headers on Response object"""
        for key, val in headers.iteritems():
            # See https://github.com/pallets/flask/issues/287
            self.headers.add(key, val)

        return self

    def to_json(self):
        """Return serialize ready dictionary"""
        indent = None
        separators = (',', ':')

        self.data = flask_json.dumps(self.ext_paylod, indent=indent, separators=separators)
        self.mimetype = self.JSON_MIMETYPE
        
        return self
