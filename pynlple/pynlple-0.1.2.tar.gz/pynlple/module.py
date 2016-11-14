# -*- coding: utf-8 -*-

import os.path


def abs_path(source_path=None, relative_path=''):
    """Get the absolute path to the relative_path according to the source_path.
    Pass the __file__ variable to form absolute paths senseless to execution environment.
    If no source_path is set, then build absolute to the project folder."""
    return os.path.abspath(os.path.join(os.path.dirname(source_path if source_path else __file__), relative_path))


def append_paths(*parts):
    """Append parts of the paths to form correct path. Wraps os.path.join method."""
    return os.path.join(*parts)


def file_name(file_path):
    """Get the name of the file from the file path (assumed as the last component of the path). Preserve extension."""
    components = os.path.split(file_path)
    return components[-1]


def stripped_file_name(file_path):
    """Get the stripped name of the file from the file path (assumed as the last component of the path).
    Stripping includes cutting of the assumed extension of the file (the last suffix separated by .)"""
    file_name_ = file_name(file_path)
    return strip_extension(file_name_)


def strip_extension(file_name_):
    """Strips the file_name_ by cutting of the assumed extension of the file (the last suffix separated by .)"""
    return file_name_[:file_name_.rfind('.')]


def get_path_difference_postfix(path_, children_path):
    """Get the postfix of children path_ that is the leftover of path_ - children_path.
    If paths are identical, then None is returned."""
    components = os.path.split(path_)
    children_components = os.path.split(children_path)
    postfix = list(children_components)
    i = 0
    while len(postfix) > 0 and i < len(path_) and components[i] == children_components[i]:
        postfix = postfix[i:]
        i += 1
    if len(postfix) == 0:
        return None
    return postfix


def list_dir(path_):
    return os.listdir(path_)


def is_file(path_):
    return os.path.isfile(path_)


def is_folder(path_):
    return os.path.isdir(path_)


def exists(path_):
    return os.path.exists(path_)