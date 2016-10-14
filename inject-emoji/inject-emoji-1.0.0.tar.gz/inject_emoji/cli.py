#!/usr/bin/env python

import argparse
import sys
from .core import __version__
from .inject_emoji import InjectEmoji

parser = argparse.ArgumentParser(
    description='Convert emoji-cheat-sheet notation to HTML image tags.')
parser.add_argument('-o', '--output',
    type=argparse.FileType('w'),
    default=sys.stdout,
    metavar='FILE',
    help="Write to FILE instead of stdout")
parser.add_argument('-d', '--dir',
    default=None,
    metavar='EMOJI_DIR',
    help="Read emoji directory listing from EMOJI_DIR instead of bundled emoji")
parser.add_argument('input_file',
    nargs='?',
    metavar='FILE',
    type=argparse.FileType('r'),
    default=sys.stdin,
    help='Read from FILE instead of stdin')
parser.add_argument('-v', '--version', action='version', version=__version__)
args = parser.parse_args()

def main():
    return InjectEmoji(args.input_file, args.output, args.dir).main()

if __name__ == '__main__':
    sys.exit(main())
