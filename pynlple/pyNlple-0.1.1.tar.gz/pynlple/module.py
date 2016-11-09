# -*- coding: utf-8 -*-

import os.path


def get_abs_path(relative_to_project_path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), relative_to_project_path))


def abs_path(file_, relative_to_file_path):
    return os.path.abspath(os.path.join(os.path.dirname(file_), relative_to_file_path))


def append_paths(*parts):
    return os.path.join(*parts)


def file_name(file_path):
    components = os.path.split(file_path)
    return components[-1]
