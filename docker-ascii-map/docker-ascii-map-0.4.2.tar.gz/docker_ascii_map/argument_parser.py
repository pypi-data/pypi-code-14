import argparse
import os
from typing import Tuple
from docker_ascii_map import __version__


def get_input_parameters() -> Tuple[bool]:
    parser = argparse.ArgumentParser(description='Display the docker host contents on a visual map.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('-c', '--color', action='store_const', const='color', help='Use color in map display')
    parser.add_argument('-m', '--mono', action='store_const', const='mono', help='Render the map in monochrome')

    terminal = os.getenv('TERM')

    args = parser.parse_args()
    color_mode = False

    if terminal:
        color_mode = 'color' in terminal

    if args.color:
        color_mode = True

    if args.mono:
        color_mode = False

    return color_mode, None
