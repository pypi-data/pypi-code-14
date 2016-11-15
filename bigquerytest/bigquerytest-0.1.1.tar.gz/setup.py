from setuptools import setup

setup(
    name='bigquerytest',
    version='0.1.1',
    author='Andreas Jansson',
    author_email='andreas@jansson.me.uk',
    description='unittest TestCase with BigQuery table mocks in human-readable format',
    license='MIT',
    packages=['bigquerytest'],
    install_requires=[
        'google-cloud-bigquery>=0.20.0',
    ],
)
