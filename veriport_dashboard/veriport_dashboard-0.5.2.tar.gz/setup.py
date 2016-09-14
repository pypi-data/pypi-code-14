import os
from os import listdir
from os.path import isfile, join
from setuptools import setup, find_packages


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
APP_DIR = os.path.join(BASE_DIR, "veriport_dashboard")


def get_all_files(parent_path):
    files = []
    def get_files(dir_path):
        """
        """
        for filename in listdir(dir_path):
            fullpath = join(dir_path, filename)
            if isfile(fullpath):
                if not fullpath.endswith(".pyc"):
                    files.append(fullpath)
            else:
                get_files(fullpath)
        return files
    return get_files(parent_path)


setup(
    name = 'veriport_dashboard',
    include_package_data=True,
    package_data={
        'migrations': get_all_files(os.path.join(APP_DIR, "migrations")),
        'static': get_all_files(os.path.join(APP_DIR, "static")),
        'templates': get_all_files(os.path.join(APP_DIR, "templates")),
        'templatetags': get_all_files(os.path.join(APP_DIR, "templatetags")),
    },
    packages=find_packages(exclude=["dist"]),
    version = '0.5.2',
    description = 'This is a dashboard utility made specifically for Veriport project',
    author = 'Ronil Rufo',
    author_email = 'ronil.rufo@gmail.com',
    url = 'https://github.com/verifydx/veriport-dashboard', # use the URL to the github repo
    download_url = 'https://github.com/verifydx/veriport-dashboard/tarball/0.1', # I'll explain this in a second
    keywords = ['veriport', 'dashboard', 'veriport_dashboard'], # arbitrary keywords
    classifiers = [],
    install_requires=["numpy", "reportlab", "django-haystack"],
)
