from base64 import b64encode, b64decode
import os
from StringIO import StringIO

from PIL import Image
from six import string_types


def pdf_preprocess(pdf, batch=False):
    """
    Load pdfs from local filepath if not already b64 encoded
    """
    if batch:
        return [pdf_preprocess(doc, batch=False) for doc in pdf]

    if os.path.isfile(pdf):
        # a filepath is provided, read and encode
        return b64encode(open(pdf).read())
    else:
        # assume pdf is already b64 encoded
        return pdf


def postprocess_image(image):
    raw_data = image.get('data')
    data = b64decode(raw_data)
    try:
        return Image.open(StringIO(data))
    except IOError:
        return None


def postprocess_images(images):
    images = [postprocess_image(image) for image in images]
    images = [image for image in images if image] # remove Nones
    return images
