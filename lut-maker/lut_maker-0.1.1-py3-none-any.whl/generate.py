"""
Functions for use in generating assets to be altered and then used for LUT calculations.
"""

import os
import json
import math
import random
from PIL import Image, ImageDraw

from .constants import MEASUREMENT_FILENAME, ALIGNMENT_FILENAME, META_FILENAME
from .lut import Lut

def new(lut_size, image_size, output_path, name, stack_size):
    """
    Generate and save measurement and alignment assets to disk for use in computing the LUT later.
    """
    lut = Lut(lut_size, image_size)
    shuffle = stack_size > 1
    sidecars = []
    for i in range(stack_size):
        sidecar = swatch_card(
                os.path.join(output_path,MEASUREMENT_FILENAME.format(name,i)),
                lut,
                shuffle)
        sidecars.append(sidecar)

    alignment_guide(
            os.path.join(output_path, ALIGNMENT_FILENAME.format(name)),
            lut)

    with open(os.path.join(output_path, META_FILENAME.format(name)), 'w') as f:
        f.write(json.dumps({
            'lut_size': lut_size,
            'stack_size': stack_size,
            'image_size': image_size,
            'sidecars': sidecars
        }))


def swatch_card(path, lut, shuffle):
    """
    Generate measurement image and save it to disk, returning the inverse lookup table for color positions.
    """
    colors = lut.generate_colors()
    image = Image.new('RGB', (lut.image_size, lut.image_size), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    lookup_table = list(range(lut.swatch_count))
    if shuffle:
        random.shuffle(lookup_table)

    for i, color in enumerate(colors):
        draw.rectangle(lut.cell_bounds(lookup_table[i]), fill=tuple(color))

    image.save(path, "PNG")
    return lookup_table


def alignment_guide(path, lut):
    """
    Generate image alignment guide and save to disk.
    """
    image = Image.new('RGBA',(lut.image_size, lut.image_size),(255,0,0,0))
    draw = ImageDraw.Draw(image)

    for i in range(lut.swatch_count):
        image.putpixel(lut.cell_center(i),(255,0,0))
        draw.rectangle(lut.cell_bounds(i), outline=(0,0,255,255))
        draw.rectangle(lut.cell_center(i, 6), outline=(0,255,0))

    image.save(path,'PNG')
