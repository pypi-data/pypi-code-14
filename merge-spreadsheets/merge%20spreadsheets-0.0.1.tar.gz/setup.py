from setuptools import setup, find_packages

setup(
    name='merge spreadsheets',
    version='0.0.1',
    packages=find_packages(),
    long_description='gui for merge spreadsheets',
    include_package_data=True,
    test_suite='tests',
    entry_points={
        'console_scripts':
            ['merge_spreadsheets = src.gui_merge_spreadsheets:main']
    },
    author='msBooM',
    author_email='work-msboom@yandex.ru',
)
