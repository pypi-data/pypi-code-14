from setuptools import find_packages
from setuptools import setup

setup(
    name='netapp-lib',
    packages=find_packages(exclude=['*.tests', '*.tests.*',
                                    'tests.*', '*.tools', '*.tools.*',
                                    'tools.*', 'tests', 'tools']),
    version='2016.10.14',
    license='Proprietary::NetApp',
    description='netapp-lib is required for OpenStack deployments to '
                'interact with NetApp storage systems.',
    author='NetApp, Inc.',
    author_email='ng-openstack-pypi@netapp.com',
    install_requires=[
        'xmltodict',
    ],
    package_data={
        '': ['*.txt', '*.rst'],
    },
    include_package_data=True,
    keywords=['openstack', 'netapp', 'cinder', 'manila', 'netapp_lib'],
    classifiers=['Environment :: OpenStack'],
)
