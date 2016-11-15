res_body = {
    'type': 'object',
    'additionalProperties': False,
    'required': [
        'name', 'notes', 'version', 'source', 'doc',
        'num_user', 'num_sched'
    ],
    'properties': {
        'name': {'type': 'string'},
        'notes': {'type': 'string'},
        'version': {
            'type': 'string',
            'pattern': '^[0-9]+\.[0-9]+\.[0-9]+$',
        },
        'source': {'type': 'string'},
        'doc': {'type': 'string'},
        'num_user': {'type': 'integer'},
        'num_sched': {'type': 'integer'}
    }
}

res = {'body': res_body}
