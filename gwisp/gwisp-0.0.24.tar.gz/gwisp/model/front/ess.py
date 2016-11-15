#: Response result from invoking token
token = {
    'type': 'object',
    'additionalProperties': False,
    'required': [
        'access_token', 'token_type', 'expires_in', 'refresh_token'
    ],
    'properties': {
        'access_token': {'type': 'string'},
        'token_type': {'type': 'string', 'pattern': '^Bearer$'},
        'expires_in': {'type': 'integer'},
        'refresh_token': {'type': 'string'}
    }
}
