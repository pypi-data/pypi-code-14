import os
from setuptools import setup

setup(
    name="dj-jsonfield",
    version=open(os.path.join(os.path.dirname(__file__),
                 'dj_jsonfield', 'VERSION')).read().strip(),
    description="JSONField for django models",
    long_description=open("README.rst").read(),
    url="https://github.com/ratson/dj-jsonfield/",
    author="Ratson",
    author_email="contact@ratson.name",
    packages=[
        "dj_jsonfield",
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Framework :: Django',
    ],
    test_suite='tests.main',
    include_package_data=True,
)
