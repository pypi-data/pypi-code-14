#!/usr/bin/python

from __future__ import print_function
import argparse
import json
import re
import sys
import yaml


def _mockable_print(arg):
    print(arg)


def run():
    prose_wc(setup(sys.argv[1:]))


def setup(argv):
    parser = argparse.ArgumentParser(
        description='Compute Jekyl- and prose-aware wordcounts',
        epilog='Accepted filetypes: plaintext, markdown, markdown (Jekyll)')
    parser.add_argument('-u', '--update', action='store_true',
                        help='update the jekyll file in place with the counts.'
                        ' Does nothing if the file is not a Jekyll markdown '
                        'file. Implies format=yaml, invalid with input '
                        'from STDIN and non-Jekyll files.')
    parser.add_argument('-f', '--format', nargs='?',
                        choices=['yaml', 'json', 'default'], default='default',
                        help='output format.')
    parser.add_argument('-i', '--indent', type=int, nargs='?', default=4,
                        help='indentation depth (default: 4).')
    parser.add_argument('file', type=argparse.FileType('r'),
                        help='file to count (or - for STDIN)')
    return parser.parse_args(argv)


def prose_wc(args):
    if args.file is None:
        return 1
    content = args.file.read()
    filename = args.file.name
    result = wc(filename, content)
    if (args.update and
            filename != '_stdin_' and
            result['counts']['type'] == 'jekyll'):
        update_file(filename, result, content, args.indent)
    else:
        _mockable_print({
            'yaml': yaml.dump(result, default_flow_style=False,
                              indent=args.indent),
            'json': json.dumps(result, indent=args.indent),
            'default': default_dump(result),
        }[args.format])
    return 0


def wc(filename, contents):
    # If it's Jekyll, strip frontmatter
    if contents[:3] == '---':
        fmt = 'jekyll'
        body = re.split('---+', contents, 2)[2].strip()
    else:
        fmt = 'md/txt'
        body = contents.strip()

    # Strip the body down to just words
    words = re.sub('\n', ' ', body)
    words = re.sub('\s+', ' ', words)
    words = re.sub('[^\w\s]', '', words)

    # Retrieve only non-space characters
    real_characters = re.sub('\s', '', words)

    return {
        'counts': {
            'file': filename,
            'type': fmt,
            'paragraphs': len(body.split('\n\n')),
            'words': len(words.split(' ')),
            'characters_real': len(real_characters),
            'characters_total': len(words),
        }
    }


def update_file(filename, result, content, indent):
    parts = re.split('---+', content, 2)
    frontmatter = yaml.safe_load(parts[1])
    frontmatter['counts'] = result['counts']
    parts[1] = '\n{}'.format(
        yaml.dump(frontmatter, default_flow_style=False, indent=indent))
    result = '---'.join(parts)
    with open(filename, 'w') as f:
        f.write(result)
    print('{} updated.'.format(filename))


def default_dump(result):
    result['counts']['_paragraphs'] = (
        'paragraph' if result['counts']['paragraphs'] == 1 else 'paragraphs')

    return ('{file} ({type})\t{paragraphs} {_paragraphs}\t{words} '
            'words\t{characters_real} characters (real)\t'
            '{characters_total} characters (total)'.format(
                **result['counts']))


if __name__ == '__main__':
    sys.exit(run())
