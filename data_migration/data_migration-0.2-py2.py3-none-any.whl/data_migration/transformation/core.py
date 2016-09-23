from patch.core import getpatch
from patch.core import Patch
from lang.json import JsonSchema

class Transformation(object):

    def __init__(self, schema):

        super(Transformation, self).__init__()

        self.schema = schema
        self.patch = getpatch(self.schema, self.schema['patch'])

    @property
    def input(self):

        return self.schema['input']

    @property
    def output(self):

        return self.schema['output']

    @property
    def filtre(self):

        return self.schema['filter']

    def select_data(self, filter, input):

        data = getresource(input)
        db.data.find(filter)

        return data

    def apply_patch(self, data=None):

        if data is None:

            data = self.select_data(self.filter, self.input)

        return self.patch.process(data, self.schema)

    def save(self, output):

        raise NotImplementedError()