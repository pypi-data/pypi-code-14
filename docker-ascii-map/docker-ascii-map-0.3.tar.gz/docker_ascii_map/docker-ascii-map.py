#!/usr/bin/env python3
import argparse
import sys
from docker_ascii_map import __version__

from docker_ascii_map.docker_config import ConfigParser

from docker_ascii_map.ascii_render import Renderer

parser = argparse.ArgumentParser(description='Display the docker host contents on a visual map.')
parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)

if __name__ == '__main__':
    args = parser.parse_args()

    parser = ConfigParser()
    renderer = Renderer()

    config = parser.get_configuration()
    # print(config)
    text = renderer.render(config, sys.stdout.encoding)
    print(text)
