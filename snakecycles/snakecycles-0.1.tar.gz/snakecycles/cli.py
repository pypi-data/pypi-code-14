# -*- coding: utf-8 -*-
"""Core shell application.
Parse arguments and logger, use translated strings.
"""
from __future__ import unicode_literals

import codecs
import re
import sys

from networkx import DiGraph, simple_cycles

__author__ = 'mgallet'

__all__ = ['main']


def str_or_none(value):
    if value == 'None':
        return None
    return value[1:-1]


def parse_line(line):
    """Parse a single output line
    looks like "(('/home/user/projects/name', 'script.py'), (None, None))"

    :param line:
    :return:
    """
    matcher = re.match(r"\(\(('.*'|None), ('.*'|None)\), \(('.*'|None), ('.*'|None)\)\)", line)
    if not matcher:
        raise ValueError('Invalid line: %s' % line)
    values = matcher.groups()
    return (str_or_none(x) for x in values)


def main():
    graph = DiGraph()
    stdin = sys.stdin
    if sys.version_info[0] == 2 and sys.stdin.encoding:
        stdin = codecs.getreader(sys.stdin.encoding)(sys.stdin)
    for line in stdin:
        src_dir, src_file, dst_dir, dst_file = parse_line(line)
        if None in (src_dir, src_file, dst_dir, dst_file):
            continue
        src = '%s/%s' % (src_dir, src_file)
        dst = '%s/%s' % (dst_dir, dst_file)
        graph.add_edge(src, dst)
    cycles = simple_cycles(graph)
    for cycle in cycles:
        print(' -- '.join(cycle))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
