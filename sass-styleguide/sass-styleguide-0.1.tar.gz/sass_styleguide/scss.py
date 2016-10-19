#!/usr/bin/env python
import logging
import os

from collections import defaultdict, OrderedDict

from jinja2 import Template

from . import (
    COLOUR_NAMES,
    _startswith_one_of,
)


def get_variables(text, variables=None):
    variables = variables or defaultdict(dict)
    for line in text.split(';'):
        # ignore comments and other non-variable declarations
        line = line.strip()
        if (
            _startswith_one_of(line, ['/*', '*', '//']) or
            ':' not in line or
            '$' not in line or
            '@' in line
        ):
            continue

        try:
            attr, value = line.split(':')
            attr = attr.strip()
            value = value.strip()

            if attr.startswith('$'):
                key = 'colors' if is_color(value) else 'other'
                variables[key][attr.replace('$', '')] = value.replace(';', '')
        except ValueError as e:
            logging.debug(e)

    return variables


def is_color(value):
    return (
        _startswith_one_of(value, ['#', 'rgb', 'rgba', 'hsl', 'hsla']) or
        value in COLOUR_NAMES
    )


def render_html(variables):
    path = os.path.realpath(__file__)
    dirname = os.path.dirname(path)
    with open(os.path.join(dirname, 'templates/index.html')) as f:
        template = Template(f.read())
        return template.render(variables=variables)


def traverse_files(path='.'):
    sass = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.scss'):
                sass.append(os.path.join(root, file))

    return sass


def get_project_variables():
    variables = defaultdict(dict)
    for file in traverse_files():
        with open(file) as f:
            variables.update(get_variables(f.read(), variables=variables))

    return variables


def write_file(path='./styleguide.html'):
    with open(path, 'w+') as f:
        variables = get_project_variables()
        for k, v in variables.iteritems():
            variables[k] = OrderedDict(sorted(v.items()))
        html = render_html(variables)
        f.write(html)
        print('File generated: {}'.format(f.name))


if __name__ == '__main__':
    write_file()
