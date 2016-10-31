#!/usr/bin/env python3
import argparse
import sys
from docker_ascii_map import __version__

from docker_ascii_map.docker_config import ConfigParser

from docker_ascii_map.ascii_render import Renderer

parser = argparse.ArgumentParser(description='Display the docker host contents on a visual map.')
parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
parser.add_argument('-c', '--color', action='store_const', const='color', help='Use color in map display')
parser.add_argument('-m', '--mono', action='store_const', const='mono', help='Render the map in monochrome')

if __name__ == '__main__':
    args = parser.parse_args()
    color_mode = args.color and not args.mono

    config_parser = ConfigParser()
    renderer = Renderer()

    config = config_parser.get_configuration()
    # print(config)
    text = renderer.render(config, encoding=sys.stdout.encoding, color=color_mode)
    print(text)
