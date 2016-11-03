import codecs
import os
import re

from setuptools import setup, find_packages, Command

here = os.path.abspath(os.path.dirname(__file__))

package = 'tapioca_circleci'
requirements = [
    'tapioca-wrapper<2',
]

test_requirements = [
    'pytest',
    'flake8',
    'pytest-cov',
]

version = "0.0.0"
changes = os.path.join(here, "CHANGES.rst")
match = r'^#*\s*(?P<version>[0-9]+\.[0-9]+(\.[0-9]+)?)$'
with codecs.open(changes, encoding='utf-8') as changes:
    for line in changes:
        res = re.match(match, line)
        if res:
            version = res.group("version")
            break

# Get the long description
with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n{}'.format(f.read())

with codecs.open(os.path.join(here, 'CHANGES.rst'), encoding='utf-8') as f:
    changes = f.read()
    long_description += '\n\nChangelog:\n----------\n\n{}'.format(changes)

# Get version
with codecs.open(os.path.join(here, 'CHANGES.rst'), encoding='utf-8') as f:
    changelog = f.read()


class VersionCommand(Command):
    description = "print library version"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(version)


setup(
    name='tapioca-circleci',
    version=version,
    description='CircleCI API wrapper using tapioca',
    long_description=long_description,
    author='George Y. Kussumoto',
    author_email='contato@georgeyk.com.br',
    url='https://github.com/georgeyk/tapioca-circleci/',
    download_url='https://github.com/georgeyk/tapioca-circleci/releases/',
    packages=find_packages(exclude=['docs', 'tests*', 'requirements*']),
    package_dir={'tapioca_circleci': 'tapioca_circleci'},
    include_package_data=True,
    install_requires=requirements,
    license='MIT',
    zip_safe=False,
    keywords='circleci,api,wrapper',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
    ],
    setup_requires=['pytest-runner'],
    test_suite='tests',
    tests_require=test_requirements,
    cmdclass={
        'version': VersionCommand,
    }
)
