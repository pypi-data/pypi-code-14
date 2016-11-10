from setuptools import setup

setup(name='lut_maker',
    version='0.1.1',
    description='Generate 3D color LUTs in Adobe Cube and Pseudo-3D texture format',
    url='https://github.com/faymontage/lut-maker',
    author='Fay Montage',
    author_email='accounts@faymontage.com',
    license='MIT',
    packages=['lut_maker'],
    zip_safe=False,
    entry_points = {
        'console_scripts': [
            'lut_maker=lut_maker.cli:main',
        ],
    },
    install_requires = {
        'click',
        'numpy',
        'Pillow'
    })
