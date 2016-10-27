#!/usr/bin/python

DOCUMENTATION = '''
---
module: dcos_token
short_description: Get DCOS token
'''

EXAMPLES = '''
- name: Get DCOS token
  dcos_token:
    register: "dcos_token"
'''

from ansible.module_utils.basic import *
from ansible.module_utils import dcos


def dcos_token_present(params):


def main():
    global module
    module = AnsibleModule(argument_spec={
        'uid': { 'type': 'str', 'required': True },
        'password': { 'type': 'str', 'required': False },
        'description': { 'type': 'str', 'required': False },
        'reset_password': { 'type': 'bool', 'required': False, 'default': False },
        'state': {
            'type': 'str',
            'required': False,
            'default': 'present',
            'choices': [ 'present', 'absent' ]
        },
    })
    dcos_token_get(module.params)


if __name__ == '__main__':
    main()
