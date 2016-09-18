from setuptools import setup, find_packages

setup(
    name='rinobot_plugin',
    description='Rinobot plugin helpers',
    version='0.0.1',

    author='Eoin Murray',
    author_email='eoin@rinocloud.com',
    url='https://github.com/rinocloud/rinobot-plugin',
    keywords=['rinocloud', 'rinobot', 'plugin'],

    packages=find_packages(),
    include_package_data=True,

    install_requires=[
        'click',
        'numpy'
    ],

    entry_points='''
        [console_scripts]
        rinobot-plugin=rinobot_plugin.scripts.cli:cli
    ''',

    test_suite='rinobot_plugin.test.all',
    tests_require=['mock'],
)
