from setuptools import setup

setup(
    name='bluejay2',
    version='0.1.5',
    py_modules=['bluejay', 'bluejay.bluejay', 'bluejay.openstack'],
    include_package_data=True,
    install_requires=[
        'click',
        'requests==2.3.0'
    ],
    description='Client for Nibiru',
    author='Dinesh Weerapurage',
    author_email='dinesh.weerapurage@pearson.com',
    entry_points='''
        [console_scripts]
        bluejay=bluejay:cli
    ''',
)
