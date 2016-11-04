#!/usr/bin/env python
import os


def create_dirs(path):
    directory = os.path.dirname(path)
    if not os.path.exists(path):
        os.mkdir(path)


