import os.path

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

long_description = ""
with open('README.rst') as f:
    long_description = f.read()

setup(
    name='ImageHash',
    version='3.1',
    author='Johannes Buchner',
    author_email='buchner.johannes@gmx.at',
    packages=['imagehash', 'imagehash.tests'],
    package_data={'imagehash': [os.path.join('tests', 'data', '*')]},
    scripts=['find_similar_images.py'],
    url='https://github.com/JohannesBuchner/imagehash',
    license='BSD 2-clause (see LICENSE file)',
    description='Image Hashing library',
    long_description=long_description,
    install_requires=[
        "numpy",
        "scipy",       # for phash
        "pillow",      # or PIL
        "PyWavelets",  # for whash
    ],
    test_suite='imagehash.tests'
)
