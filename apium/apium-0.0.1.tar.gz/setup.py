from setuptools import setup, find_packages


setup(
    name='apium',
    version='0.0.1',
    author='Christian Boelsen',
    author_email='christianboelsen+github@gmail.com',
    packages=find_packages(exclude=["tests"]),
    entry_points={
        'console_scripts': [
            'apium-worker = apium.command:start_workers',
            'apium-inspect = apium.command:inspect',
        ],
    },
    license='LICENSE',
    description=open('README').read(),
    install_requires=[],
    keywords=['celery', 'task', 'queue'],
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
