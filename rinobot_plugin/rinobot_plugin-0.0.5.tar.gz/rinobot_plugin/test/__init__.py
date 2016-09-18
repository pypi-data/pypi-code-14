import os
import unittest

from .test import Test

def all():
    path = os.path.dirname(os.path.realpath(__file__))
    return unittest.defaultTestLoader.discover(path)
