from __future__ import absolute_import

from core import Schema

import json
from jsonschema import validate

class JsonSchema(Schema):

    def getresource(self, path):

        with open(path, "r") as f:
            _rsc = json.load(f)

        return _rsc

    def validate(self, data):

        return validate(data, self._rsc)

    def __getitem__(self, key):
        #take key in argument and make Schema.get(key) dictionary methode

        return self._rsc[key]

    def __setitem__(self, key, value):
        #take key in argument and make Schema[key] = value dictionary methode

        self._rsc[key] = value

    def __delitem__(self, key):
        #take key in argument and make del Schema[key] dictionary methode

        del self._rsc[key]

    def save(self, data, output):
        #save json data in the correct folder

        with open(output, "w") as f:
            json.dump(data, f, indent=4)