from .ess import account_id

#: Identity
attr_id = {
    'type': 'string',
    'pattern': '^[a-zA-Z0-9]{22}$'
}

#: Account identity which is refresh token belong
attr_account_id = account_id

#: Expired date
attr_expired = {
    'type': 'integer'
}

#: Model store in database
storage = {
    'type': 'object',
    'additionalProperties': False,
    'required': ['_id', 'account_id', 'expired'],
    'properties': {
        '_id': attr_id,
        'account_id': attr_account_id,
        'expired': attr_expired
    }
}
