import copy
import jsonschema

from ..repo import scheduler as rmodel_sched


req_body = copy.deepcopy(rmodel_sched.insert)
req_body['required'].remove('author')
req_body['properties'].pop('author')
req = {'body': req_body}

res_header = {
    'type': 'object',
    'required': ['Location'],
    'properties': {
        'Location': {
            'type': 'string',
            'pattern': '^\/scheduler\/[a-fA-F0-9]{24}$'
        }
    }
}
res = {'header': res_header}


def validate_post(item):
    jsonschema.validate(item, req_body)
