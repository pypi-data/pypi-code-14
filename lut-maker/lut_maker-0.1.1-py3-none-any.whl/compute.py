"""
Functions for use in computing LUTs from altered measurement assets.
"""

import os
import json
import itertools
import math
from PIL import Image
from statistics import mean

from .constants import MEASUREMENT_FILENAME, META_FILENAME, LUT_JSON_FILENAME, LUT_CUBE_FILENAME, LUT_PNG_FILENAME
from .lut import Lut

def compute_lut(path, name):
    """
    Load altered LUT assets, compute lut, and save to disk in a variety of formats.
    """
    meta_path = os.path.join(path, META_FILENAME.format(name))
    with open(meta_path,'r') as f:
        meta = json.loads(f.read())

    lut = Lut(meta['lut_size'], meta['image_size'])

    images = [Image.open(os.path.join(path,MEASUREMENT_FILENAME.format(name,i))) for i in range(meta['stack_size'])]
    colors = []
    for i in range(lut.swatch_count):
        pixels = list(itertools.chain.from_iterable(
            [extract_data(images[stack_i], meta['sidecars'][stack_i][i], lut) for stack_i in range(meta['stack_size'])]
            ))
        r = int(mean([color[0] for color in pixels]))
        g = int(mean([color[1] for color in pixels]))
        b = int(mean([color[2] for color in pixels]))
        color = (r,g,b)
        colors.append(color)

    save_lut_json(path, name, lut, colors)
    save_lut_cube(path, name, lut, colors)
    save_lut_png(path, name, lut, colors)

    return (lut, meta)


def cube_row(color):
    """
    Format color tuple as string for a CUBE file line
    """
    return ' '.join(map(lambda x: str(x/255), color))


def extract_data(image, i, lut):
    """
    Extract and return image data for given measurement point.
    """
    crop = image.crop(lut.cell_center(i, 6))
    data = list(crop.getdata())
    return data


def save_lut_json(path, name, lut, colors):
    """
    Save LUT data as JSON, for general programmatic use.
    """
    with open(os.path.join(path,LUT_JSON_FILENAME.format(name)),'w') as f:
        f.write(json.dumps({
                'name': name,
                'lut_size': lut.size,
                'samples': list(map(lambda x: list(map(lambda y: y/255, x)), colors))
                }))


def save_lut_cube(path, name, lut, colors):
    """
    Save LUT data as Adobe Cube, for use in Photoshop, Premiere, etc.
    Adobe Cube Spec: http://wwwimages.adobe.com/content/dam/Adobe/en/products/speedgrade/cc/pdfs/cube-lut-specification-1.0.pdf
    """
    cube = 'LUT_3D_SIZE {}\n'.format(lut.size) + '\n'.join(map(cube_row, colors))
    with open(os.path.join(path,LUT_CUBE_FILENAME.format(name)),'w') as f:
        f.write(cube)


def save_lut_png(path, name, lut, colors):
    """
    Save LUT data as pseudo-3D texture, for use in OpenGL shaders.
    """
    im = Image.new('RGB', (pow(lut.size,2), lut.size), (0, 0, 0))
    for i,color in enumerate(colors):
        column, row, z = lut.lattice_coords(i)
        im.putpixel((z*lut.size+column,row), color)
    im.save(os.path.join(path, LUT_PNG_FILENAME.format(name)),'PNG')
