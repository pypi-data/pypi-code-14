from setuptools import setup

setup(
    name='KeyCat',
    version='0.0.2',
    packages=['keycat'],
    entry_points = {
        "console_scripts":  ['keycat = keycat.keycat:main']
        },
    url='https://github.com/KatreMetsvahi/KeyCat',
    description="Shortcut helper.",
    author='',
    author_email='',
    download_url='https://github.com/KatreMetsvahi/keycat/tarball/0.0.1app',
    install_requires=[
        'Pillow',
        'pyscreenshot',
        'PyUserInput',
        'screeninfo'
    ]
)
