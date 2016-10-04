__author__ = 'marcoantonioalberoalbero'

from jsonschema import validate, Draft4Validator


class JsonValidator:
    def __init__(self):
        pass

    @staticmethod
    def validate(json, schema):
        result = {}
        v = Draft4Validator(schema)
        err = sorted(v.iter_errors(json), key=str)
        result['errors'] = err
        if not len(err):
            result['valid'] = True
        else:
            result['valid'] = False
        return result
