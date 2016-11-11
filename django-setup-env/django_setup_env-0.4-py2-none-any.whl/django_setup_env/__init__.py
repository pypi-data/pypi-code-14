import os
import sys

import django


def setup_django(filename, django_package_name='mysite'):
    """
    Utility function that adds the Django package

     * adds the Django project to the path
     * sets the DJANGO_SETTINGS_MODULE environment variable
     * calls django.setup()
    """
    # Get module path
    path = os.path.realpath(filename)
    # Strip script name
    if os.path.isfile(path):
        path = os.path.dirname(path)
    # Add the absolute path containing the Django package
    path_list = path.split(os.sep)
    if django_package_name in path_list:
        path_list = path_list[:path_list.index(django_package_name)]
        path = os.sep.join(path_list)
        sys.path.append(path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%s.settings" % django_package_name)

    try:
        django.setup()
    except AttributeError:
        # django.setup does not exist in Django 1.6
        pass
