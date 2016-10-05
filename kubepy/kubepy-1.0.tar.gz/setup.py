from pip.req import parse_requirements
from setuptools import find_packages
from setuptools import setup


setup(
    name='kubepy',
    version='1.0',
    description='Python wrapper on kubectl that makes deploying easy.',
    author='Jakub Skiepko',
    author_email='jakub.skiepko@socialwifi.com',
    url='https://github.com/socialwifi/kubepy',
    packages=find_packages(),
    install_requires=[str(ir.req) for ir in parse_requirements('base_requirements.txt', session=False)],
    entry_points={
        'console_scripts': [
            'kubepy-apply-all = kubepy.commands.apply_all:run',
            'kubepy-apply-one = kubepy.commands.apply_one:run',
        ],
    },
)
