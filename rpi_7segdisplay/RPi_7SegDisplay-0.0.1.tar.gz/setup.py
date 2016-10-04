from distutils.core import setup

setup(
    name='RPi_7SegDisplay',
    version='0.0.1',
    description='A Python package for displaying messages on an eight-digit seven-segment display connected to a Raspberry Pi',
    author='Tim Mendoza',
    author_email='timmydoza@gmail.com',
    url='https://github.com/timmydoza/RPi_7SegDisplay',
    py_modules=['RPi_7SegDisplay'],
    install_requires=['RPi.GPIO'],
    keywords=['raspberry', 'pi', 'gpio', 'led', 'display', 'seven-segment']
)
