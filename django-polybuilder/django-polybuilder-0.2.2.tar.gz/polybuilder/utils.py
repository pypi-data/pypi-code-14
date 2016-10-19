# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

import os
import sys
from django.conf import settings


def get_all_files(path, extensions=[]):
    """Get all files from 'path' if extension is in 'extensions'"""
    files_list = []

    for path, subdir, files in os.walk(path):
        for f in files:
            file_path = os.path.join(path, f)
            filename, file_ext = os.path.splitext(file_path)

            if file_ext in extensions:
                files_list.append(file_path)

    return files_list


def get_bower_choices(extensions=['.html']):
    """Get a list of all the file in 'bower_components'
    ending with the extensions
    """
    bower_dir = 'bower_components'
    files_list = get_all_files(
        os.path.join(settings.BASE_DIR, bower_dir), extensions
    )

    paths_list = []
    for path in files_list:
        path_name = path.split(bower_dir)[-1][1:]
        paths_list.append((path_name, path_name))

    return paths_list
