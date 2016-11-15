#: Object identity
object_id = {}

#: Account identity
account_id = object_id

#: Account name
account_name = {
    'type': 'string',
    'pattern': '^[a-z0-9-]{1,64}$'
}

#: Account header, use as references
account_header = {
    'type': 'object',
    'additionalProperties': False,
    'required': ['_id', 'name'],
    'additionalProperties': False,
    'properties': {
        '_id': account_id,
        'name': account_name
    }
}

#: Email
email = {
    'type': 'string',
    'pattern': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
}

#: URL
url = {
    'type': 'string',
    'pattern': '^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$'
}

#: Base 64 string
base_64 = {
    'type': 'string',
    'pattern': '^[a-zA-Z0-9+/]+={0,2}$'
}
