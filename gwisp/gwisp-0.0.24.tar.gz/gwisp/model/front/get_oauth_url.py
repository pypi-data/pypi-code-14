res_body = {
    'type': 'object',
    'additionalProperties': False,
    'required': ['url'],
    'properties': {
        'url': {'type': 'string'}
    }
}

res = {'body': res_body}
