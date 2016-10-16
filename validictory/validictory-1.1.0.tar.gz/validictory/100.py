import validictory

data = {
    'tests': {
        'default': {
            'timeout_status': 'amber',
            'sensor': 'http',
            'modules': {
                'statuscode': {'200': 'red'}
            }
        },
        'tgoogle': {
            'sensor': 'http',
            'modules': {
                'statuscode': {
                    '200': 'green',
                    'foo': 'bar',
                },
            },
            'timeout_status': 'amber'
        }
    },
    # ... more besides key tests
}

SCHEMA = {
    'type': 'object',
    'properties': {
        'tests': {
            'additionalProperties': {
                'type': 'object',
                'properties': {
                    'timeout_status': {
                        'enum': ['amber', 'yellow', 'green', 'red'],
                        'type': 'string'
                    },
                    'sensor': {
                        'pattern': '^\S+$',
                        'type': 'string'
                    },
                    'modules': {
                        'additionalProperties': False,
                        'type': 'object',
                        'properties': {
                            'statuscode': {
                                'additionalProperties': False,
                                'required': False,
                                'type': 'object',
                                'patternProperties': {
                                    '^[0-9x]{3}': {
                                        'enum': ['amber', 'yellow', 'green', 'red'],
                                        'type': 'string',
                                    }
                                }
                            }
                            # ... more available test modules
                        }
                    }
                }
            },
            'type': 'object'
        },
        # ... more besides key tests
    }
}

#validictory.validate(data, SCHEMA) #<- this fails as expected at foo
validictory.validate(data, SCHEMA, fail_fast=False) #<- this throws the exception from below

