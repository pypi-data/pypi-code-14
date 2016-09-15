from typing import NamedTuple

Filesystem = NamedTuple('Filesystem', [
    ('name', str),
    ('fstype', str),
    ('ciphertextDirectory', str),
    ('plaintextDirectory', str)
])