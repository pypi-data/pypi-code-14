from __future__ import absolute_import
import collections

def group_by(records, key, value=lambda r: r):
    '''TODO docstring'''
    grouped = collections.defaultdict(list)
    for record in records:
        grouped[key(record)].append(value(record))
    return grouped

def index(records, key, value=lambda r: r):
    '''TODO docstring'''
    return {key(row): value(row) for row in records}
