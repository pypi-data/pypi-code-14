from setuptools import setup

setup(
    name='taskall',
    version='0.1.0',
    install_requires=['dill'],
    packages=['taskall'],
    license='MIT',
    url='https://github.com/srafehi/taskall',
    keywords=['parallel', 'pool', 'multiprocessing'],
    description='Taskall is a Python module which simplifies the chore '
                'of creating and executing tasks in parallel')
