#!/usr/bin/python

from __future__ import print_function
import argparse
from bs4 import BeautifulSoup
import json
import markdown
import re
import sys
import yaml


INTERSTITIAL_PUNCTUATION = [
    re.compile(r'\.\.+'),
    re.compile(r'--+'),
]
"""list: Interstitial punctuation that separates two words represented as
    compiled regular expressions.

Punctuation that may be used between word characters that will separate
words rather than just being wiped out.
E.g: ellipses should separate words ('a...b' should parse as two words) but
apostrophes
"""


def _mockable_print(arg):
    """A print function that can be mocked in tests.

    Args:
        arg: the thing to print
    """
    print(arg)


def run():
    """Entry point for the command, running wordcount with CLI args."""
    prose_wc(setup(sys.argv[1:]))


def setup(argv):
    """Sets up the ArgumentParser.

    Args:
        argv: an array of arguments
    """
    parser = argparse.ArgumentParser(
        description='Compute Jekyl- and prose-aware wordcounts',
        epilog='Accepted filetypes: plaintext, markdown, markdown (Jekyll)')
    parser.add_argument('-S', '--split-hyphens', action='store_true',
                        dest='split_hyphens',
                        help='split hyphenated words rather than counting '
                        'them as one word ("non-trivial" counts as two words '
                        'rather than one)')
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
    """Processes data provided to print a count object, or update a file.

    Args:
        args: an ArgumentParser object returned by setup()
    """
    if args.file is None:
        return 1
    if args.split_hyphens:
        INTERSTITIAL_PUNCTUATION.append(re.compile(r'-'))
    content = args.file.read()
    filename = args.file.name
    body = strip_frontmatter(content)
    parsed = markdown_to_text(body)
    result = wc(filename, body, parsed=parsed,
                is_jekyll=(body != content))
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


def markdown_to_text(body):
    """Converts markdown to text.

    Args:
        body: markdown (or plaintext, or maybe HTML) input

    Returns:
        Plaintext with all tags and frills removed
    """
    # Turn our input into HTML
    md = markdown.markdown(body, extensions=[
        'markdown.extensions.extra'
    ])

    # Safely parse HTML so that we don't have to parse it ourselves
    soup = BeautifulSoup(md, 'html.parser')

    # Return just the text of the parsed HTML
    return soup.get_text()


def strip_frontmatter(contents):
    """Strips Jekyll frontmatter

    Args:
        contents: the contents of a Jekyll post with frontmatter

    Returns:
        The contents of the file without frontmatter
    """
    if contents[:3] == '---':
        contents = re.split('---+', contents, 2)[2].strip()
    return contents


def wc(filename, contents, parsed=None, is_jekyll=False):
    """Count the words, characters, and paragraphs in a string.

    Args:
        contents: the original string to count
        filename (optional): the filename as provided to the CLI
        parsed (optional): a parsed string, expected to be plaintext only
        is_jekyll: whether the original contents were from a Jekyll file

    Returns:
        An object containing the various counts
    """
    if is_jekyll:
        fmt = 'jekyll'
    else:
        fmt = 'md/txt'
    body = parsed.strip() if parsed else contents.strip()

    # Strip the body down to just words
    words = re.sub(r'\n', ' ', body)
    words = re.sub(r'\s+', ' ', words)
    for punctuation in INTERSTITIAL_PUNCTUATION:
        words = re.sub(punctuation, ' ', words)
    words = re.sub(r'[^\w\s]', '', words)

    # Retrieve only non-space characters
    real_characters = re.sub(r'\s', '', words)

    return {
        'counts': {
            'file': filename,
            'type': fmt,
            'paragraphs': len(contents.strip().split('\n\n')),
            'words': len(re.split('\s+', words)),
            'characters_real': len(real_characters),
            'characters_total': len(words),
        }
    }


def update_file(filename, result, content, indent):
    """Updates a Jekyll file to contain the counts form an object

    This just converts the results to YAML and adds to the Jekyll frontmatter.

    Args:
        filename: the Jekyll file to update
        result: the results object from `wc`
        content: the contents of the original file
        indent: the indentation level for dumping YAML
    """
    # Split the file into frontmatter and content
    parts = re.split('---+', content, 2)

    # Load the frontmatter into an object
    frontmatter = yaml.safe_load(parts[1])

    # Add the counts entry in the results object to the frontmatter
    frontmatter['counts'] = result['counts']

    # Set the frontmatter part backed to the stringified version of the
    # frontmatter object
    parts[1] = '\n{}'.format(
        yaml.dump(frontmatter, default_flow_style=False, indent=indent))
    result = '---'.join(parts)

    # Write everything back to the file
    with open(filename, 'w') as f:
        f.write(result)
    print('{} updated.'.format(filename))


def default_dump(result):
    """Prints a tab-separated, human-readable report of the results.

    Args:
        result: the results object from `wc`

    Returns:
        A string with the formatted result
    """
    result['counts']['_paragraphs'] = (
        'paragraph' if result['counts']['paragraphs'] == 1 else 'paragraphs')

    return ('{file} ({type})\t{paragraphs} {_paragraphs}\t{words} '
            'words\t{characters_real} characters (real)\t'
            '{characters_total} characters (total)'.format(
                **result['counts']))


if __name__ == '__main__':
    sys.exit(run())
