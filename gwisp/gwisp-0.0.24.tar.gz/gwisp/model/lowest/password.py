from .ess import base_64
from .account import attr_id as account_id


#: Account identity corresponding with password hash
attr_id = account_id

#: Password hash
attr_password_hash = base_64

#: Created date. It will nerver changed
attr_created_date = {
    'type': 'string',
    'format': 'date-time'
}

#: Modified date. It will updated when password changed
attr_modified_date = {
    'type': 'string',
    'format': 'date-time'
}

#: Model store in database
storage = {
    'type': 'object',
    'additionalProperties': False,
    'required': ['_id', 'password_hash', 'created_date', 'modified_date'],
    'properties': {
        '_id': attr_id,
        'password_hash': attr_password_hash,
        'created_date': attr_created_date,
        'modified_date': attr_modified_date
    }
}
