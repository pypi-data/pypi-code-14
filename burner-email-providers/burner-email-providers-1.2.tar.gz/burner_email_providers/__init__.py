# coding=utf-8


"""Loading this module also populates the EMAILS list once."""


import os


__all__ = ['EMAILS']


EMAILS = []


if not EMAILS:
    this_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(this_path, 'emails.txt')) as f:
        for line in f:
            stripped = line.strip()
            if stripped and stripped not in EMAILS:
                EMAILS.append(stripped)
