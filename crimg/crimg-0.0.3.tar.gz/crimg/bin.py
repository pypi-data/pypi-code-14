# -*- coding: utf-8 -*-
import sys
from io import BytesIO
import argparse
from PIL import Image

from .api import crop_resize

parser = argparse.ArgumentParser(
    description='crop and resize an image without aspect ratio distortion.')
parser.add_argument('image')
parser.add_argument('-w', '-W', '--width', metavar='<width>', type=int,
                    help='desired width of image in pixels')
parser.add_argument('-H', '--height', metavar='<height>', type=int,
                    help='desired height of image in pixels')
parser.add_argument('-f', '--force', action='store_true',
                    help='whether to scale up for smaller images')
parser.add_argument('-d', '--display', action='store_true', default=False,
                    help='display the new image (don\'t write to file)')
parser.add_argument('-o', '--output', metavar='<file>',
                    help='Write output to <file> instead of stdout.')


def main():
    parsed_args = parser.parse_args()
    image = Image.open(parsed_args.image)
    size = (parsed_args.width, parsed_args.height)
    new_image = crop_resize(image, size, parsed_args.force)
    if parsed_args.display:
        new_image.show()
    elif parsed_args.output:
        new_image.save(parsed_args.output)
    else:
        f = BytesIO()
        new_image.save(f, image.format)
        try:
            stdout = sys.stdout.buffer
        except AttributeError:
            stdout = sys.stdout
        stdout.write(f.getvalue())
