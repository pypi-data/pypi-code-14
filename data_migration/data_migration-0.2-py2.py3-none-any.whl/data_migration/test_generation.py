import schema_generation
import json


schema = schema_generation.generateSchemaJson('data2', {"patch":[{
            "path": "/test",
            "value": "TT",
            "op": "add"
        }]})

path = '/home/julie/Documents/dm/etc/schema/new_generate.json'

with open(path, "w") as f:
    json.dump(schema, f, indent=4)