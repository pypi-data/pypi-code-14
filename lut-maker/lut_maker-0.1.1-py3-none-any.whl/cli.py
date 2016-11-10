"""
Command line interface for lut_maker package.
"""

#!/usr/bin/env python
import glob
import os
import json
import sys
import click

from lut_maker import generate
from lut_maker import compute as c

@click.group()
def main():
    pass

@main.command()
@click.option('--name', default='lut', help='Name of LUT to generate')
@click.option('--lut-size', default=17, help='Size of each dimension in 3D LUT')
@click.option('--image-size', default=2048, help='Width & height of square output image in pixels')
@click.option('--stack', default=1, help='Number of unique measurement palettes to output')
@click.option('--data-dir', default='', help='Location for LUT files')
def new(lut_size, image_size, stack, name, data_dir):
    """
    Generate assets to be altered and later used for LUT computation.
    """
    generate.new(lut_size, image_size, data_dir, name, stack)

@main.command()
@click.option('--name', default='lut', help='Name of LUT to compute')
def compute(name):
    """
    Compute LUT from altered assets.
    """
    data_dir = ''
    c.compute_lut(data_dir, name)

if __name__ == '__main__':
    main()
