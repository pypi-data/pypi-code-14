# -*- coding: utf-8 -*-


def get_bool(msg):
    result = ''
    while result.lower() not in ['y', 'n']:
        result = raw_input('\n'.join([msg, '[y/n]']))

    return result == 'y'
