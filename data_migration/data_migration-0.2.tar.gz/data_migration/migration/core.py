import core
from lang.json import JsonSchema
from transformation.core import Transformation
from migration.factory import GLOBALFACTORY


def migrate(path_transfo):
    """the migrate function transform data and save them"""

    schema_class = JsonSchema
    transformation_class = Transformation

    schema = schema_class(path_transfo)
    transfo = transformation_class(schema)

    schema_transfo = schema.getresource(path_transfo)

    inp = schema_transfo['input']
    output = schema_transfo['output']
    path_v1 = schema_transfo['path_v1']
    path_v2 = schema_transfo['path_v2']

    schema_V1 = schema.getresource(path_v1)
    schema_V2 = schema.getresource(path_v2)

    myinp = GLOBALFACTORY.get(inp)
    data = myinp.load(inp, schema, schema_transfo['query'])
    result = []

    for item in data:
        result.append(myinp.transformation(item, transfo, schema))

    myout = GLOBALFACTORY.get(output)
    myout.save(result, output)