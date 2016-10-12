"""RobotFramework library for Secure Copy file transfers (SCP) that
works with the RobotFramework SSH library.
"""
from setuptools import setup, find_packages
import codecs
import os

readme_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'README.rst'))
with codecs.open(readme_path, encoding='utf-8') as f:
    readme = f.read()

setup(
    name='robotframework-scpcompat',
    version='0.1.0',
    description=__doc__,
    long_description=readme,
    author='Toby Fleming',
    author_email='tobywf@users.noreply.github.com',
    url='https://github.com/tobywf/robotframework-scpcompat',
    packages=find_packages(),
    install_requires=[
        'robotframework-sshlibrary',
        'scp'
    ],
    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Robot Framework',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Natural Language :: English',
        'Operating System :: OS Independent'
    ],
    keywords='RobotFramework SCP'
)
