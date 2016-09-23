from patch.core import Patch, registerpatch
from lang.json import JsonSchema

import jsonpatch
import json


@registerpatch(JsonSchema)
class JSONPatch(Patch):

    def process(self, data, schema):
        """define the correct process to return the patch
        in the correct form and apply it on data"""

        patch = schema['patch']
        pa = []

        for element in patch:
            pa.append(patch[element])

        p = jsonpatch.JsonPatch(pa)
        result = p.apply(data)

        return result

    def save(self, new_data, output):

        with open('output', "w") as f:
            jdon.dump(new_data, output, sort_keys = True, indent = 2, separators = (',', ':'))
