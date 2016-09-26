import pygtkhelpers as pgh
import pygtkhelpers.schema

if __name__ == '__main__':
    schema = {'type': 'object', 'properties': {'foo': {'type': 'integer', 'default': 0}}}
    pgh.schema.schema_dialog(schema, device_name=False, long_desc='Enter comma-separated list of channels:    \n')
