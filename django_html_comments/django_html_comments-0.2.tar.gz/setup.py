import os
import sys

from setuptools import setup, find_packages

version = '0.2'

setup(name='django_html_comments',
    description='Django app that provides views to process limited sanitized html comments and a sample tinymce configuration. Compatible with django.contrib.comments and Mezzanines ThreadedComments',
    long_description='Django app that provides views to process limited sanitized html comments and a sample tinymce configuration. Compatible with django.contrib.comments and Mezzanines ThreadedComments',
    author = "Sean O\'Donnell",
    author_email = "sean@odonnell.nu",
    url = "https://github.com/seanodonnell/django_html_comments",
    download_url = "https://github.com/seanodonnell/django_html_comments/archive/master.zip",
    keywords = ["django", "tinymce", "html", "comments", "mezzanine"],
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Environment :: Plugins",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
    ],
    version=version,
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False,
)
