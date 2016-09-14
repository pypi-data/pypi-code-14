
__author__ = u'Hywel Thomas'
__copyright__ = u'Copyright (C) 2016 Hywel Thomas'


def ascii_safe(string):
    return ''.join([c if ord(c) < 128 else '?' for c in string])


def file_safe(string):
    return ''.join([c if c in '1234567890-_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
                    else '_'
                    for c in string])
