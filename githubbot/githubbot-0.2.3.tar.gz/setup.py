from setuptools import setup, find_packages

with open('README') as f:
    long_description = ''.join(f.readlines())

setup(
    name='githubbot',
    version='0.2.3',
    description='Automatically labels repositories\' issues or pull requests on GitHub.',
    long_description=long_description,
    author='Jakub Tomanek',
    author_email='tomanj23@fit.cvut.cz',
    license='Public Domain',
    url='http://tmp.url.com',
    install_requires=['requests','click>=6','Flask'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'githubbot = githubbot.githubbot:main',
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Version Control'
        ],
)