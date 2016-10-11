#!/usr/bin/env python3


import sys


gen = {
    'end': 0,
    'error': 1,
    'bold': 1,
    'italic': 3,
    'underline': 4,
    'strike': 9,
    'dblack': 30,
    'dred': 31,
    'dgreen': 32,
    'dyellow': 33,
    'dblue': 34,
    'dpurple': 35,
    'dteal': 36,
    'dwhite': 37,
    '_dblack': 40,
    '_dred': 41,
    '_dgreen': 42,
    '_dyellow': 43,
    '_dblue': 44,
    '_dpurple': 45,
    '_dteal': 46,
    '_black': 99,
    '_grey': 100,
    '_red': 101,
    '_green': 102,
    '_yellow': 103,
    '_blue': 104,
    '_purple': 105,
    '_cyan': 106,
    '_white': 107,
    '_dwhite': 47,
    'black': 90,
    'red': 91,
    'green': 92,
    'yellow': 93,
    'blue': 94,
    'purple': 95,
    'teal': 96,
    'white': 97
}

colors = {x: '\033[{}m'.format(gen[x]) for x in gen}


def cprint(text, prefix='', suffix='[end]\n', file=sys.stdout):
    output = ''
    text = prefix + text + suffix
    c = []
    color = [x[:x.find(']')] if '/' in x else x[:x.find(']')] for x in
             text.split('[') if x[:x.find(']')].replace('/', '') in colors]
    for col in color:
        if col.startswith('/'):
            c.reverse()
            del c[c.index(col[1:])]
            c.reverse()
        else:
            c.append(col)
        text = (text.replace('[' + col + ']', colors['end'] +
                ''.join(colors[x.replace('/', '')] for x in c))
                if col.startswith('/') else text.replace('[' + col + ']',
                colors[col]))
    print( text, end='', file=file)
    return None
