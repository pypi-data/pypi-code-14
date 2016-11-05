from setuptools import setup, find_packages

setup(
    name='hotplate',
    version='0.0.1',
    description='simple boilerplates',
    url='https://github.com/frnsys/hotplate',
    author='Francis Tseng (@frnsys)',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'click',
        'jinja2',
        'pyyaml'
    ],
    entry_points='''
        [console_scripts]
        hotplate=main:main
    ''',
)