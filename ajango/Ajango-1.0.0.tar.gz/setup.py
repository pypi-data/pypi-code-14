###########################################################################
#                                                                         #
#  Copyright (C) 2016  Rafal Kobel <rafyco1@gmail.com>                    #
#                                                                         #
#  This program is free software: you can redistribute it and/or modify   #
#  it under the terms of the GNU General Public License as published by   #
#  the Free Software Foundation, either version 3 of the License, or      #
#  (at your option) any later version.                                    #
#                                                                         #
#  This program is distributed in the hope that it will be useful,        #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the           #
#  GNU General Public License for more details.                           #
#                                                                         #
#  You should have received a copy of the GNU General Public License      #
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                         #
###########################################################################

import os
import sys
from distutils.sysconfig import get_python_lib

from setuptools import find_packages, setup

overlay_warning = False
if "install" in sys.argv:
    lib_paths = [get_python_lib()]
    if lib_paths[0].startswith("/usr/lib/"):
        # We have to try also with an explicit prefix of /usr/local in order to
        # catch Debian's custom user site-packages directory.
        lib_paths.append(get_python_lib(prefix="/usr/local"))
    for lib_path in lib_paths:
        existing_path = os.path.abspath(os.path.join(lib_path, "ajango"))
        if os.path.exists(existing_path):
            # We note the need for the warning here, but present it after the
            # command is run, so it's more likely to be seen.
            overlay_warning = True
            break
# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

version = __import__('ajango').get_version()

EXCLUDE_FROM_PACKAGES = ['ajango.conf.skeleton_template',
                         'ajango.contrib.automatic.templates',
                         'ajango.contrib.automatic.static']

setup(
    name = "Ajango",
    version=version,
    author = "Rafal Kobel",
    author_email = "rafyco1@gmail.com",
    description = ("Plugin to Django framework with automatic generate code"),
    license = "GNU",
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    package_dir={'ajango' : 'ajango'},
    package_data={'ajango' : ['contrib/automatic/static/favicon.ico',
                              'contrib/automatic/static/css/*.css',
                              'contrib/automatic/static/img/*.png',
                              'contrib/automatic/templates/default/*.html',
                              'contrib/automatic/templates/default/'
                                  'ajango_columns/*.html',
                              'contrib/automatic/templates/default/'
                                  'ajango_inputs/*.html',
                              'gui/resources/*.png']},
    include_package_data=True,
    keywords = "Django generate application",
    url = "http://bitbucket.org/rafyco/ajango",
    long_description= ("Ajango is a web application generator. It helps with build all type view in traditional programs."),
    install_requires=[
        'Django'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

if overlay_warning:
    sys.stderr.write("""

========
WARNING!
========

You have just installed Ajango over top of an existing
installation, without removing it first. Because of this,
your install may now include extraneous files from a
previous version that have since been removed from
Ajango. This is known to cause a variety of problems. You
should manually remove the

%(existing_path)s

directory and re-install Ajango.

""" % {"existing_path": existing_path})
