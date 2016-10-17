#!/usr/bin/env python3
import sys

from docker_ascii_map.docker_config import ConfigParser

from docker_ascii_map.ascii_render import Renderer

if __name__ == '__main__':
    parser = ConfigParser()
    renderer = Renderer()

    config = parser.get_configuration()
    # print(config)
    text = renderer.render(config, sys.stdout.encoding)
    print(text)
