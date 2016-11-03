import os
import re
import glob
import distutils.log

try:
    import setuptools
except ImportError:
    import distutils.core

    setup = distutils.core.setup
else:
    setup = setuptools.setup

PACKAGE = next((str(s) for s in setuptools.find_packages('.', exclude=("tests", "tests.*"))), None)
PWD = os.path.abspath(os.path.dirname(__file__))
VERSION = (
    re
        .compile(r".*__version__ = '(.*?)'", re.S)
        .match(open(os.path.join(PWD, PACKAGE, "__init__.py")).read())
        .group(1)
)

with open(os.path.join(PWD, "README.rst")) as f:
    README = f.read()


# requires = [
    # "coreapi===1.20.0",
    # "wac===0.28",
    # "wheel==0.29",
    # "twine==1.8.1"
# ]


# def parse_requirements(file_name):
#     requirements = []
#     for line in open(file_name, 'r').read().split('\n'):
#         if re.match(r'(\s*#)|(\s*$)', line):
#             continue
#         if re.match(r'\s*-e\s+', line):
#             requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
#         elif re.match(r'\s*-f\s+', line):
#             pass
#         else:
#             requirements.append(line)
#
#     return requirements

def get_reqs_from_files(requirements_files):
    for requirements_file in requirements_files:
        if os.path.exists(requirements_file):
            return open(requirements_file, 'r').read().split('\n')
    return []


def parse_requirements(requirements_files=['requirements.txt']):
    requirements = []
    for line in get_reqs_from_files(requirements_files):
        if re.match(r'\s*-e\s+', line):
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1',line))
        elif re.match(r'\s*-f\s+', line):
            pass
        else:
            requirements.append(line)

    return requirements


def parse_dependency_links(requirements_files=['requirements.txt']):
    dependency_links = []
    for line in get_reqs_from_files(requirements_files):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-[ef]\s+', line):
            dependency_links.append(re.sub(r'\s*-[ef]\s+', '', line))
    return dependency_links

extras_require = {
    "tests": [
        "nose",
        "coverage"
    ]
}

scripts = [
    # 'bin/citadel'
]


# class UploadCommand(distutils.cmd.Command):
#     description = "upload to PyPI"
#     user_options = [
#         ('repository=', "r", 'repository defined in section [distutils] in setup.cfg'),
#     ]
#
#     def run(self):
#         from twine.commands import upload as twine_upload
#         from twine.commands import register as twine_register
#
#         self.announce('running upload `{}` to `{}`'.format(PACKAGE, self.repository), level=distutils.log.INFO)
#         for package in glob.glob("dist/*"):
#             twine_register.register(
#                 package=package,
#                 repository=self.repository,
#                 username=PYPI_USERNAME,
#                 password=PYPI_PASSWORD,
#                 comment=None,
#                 config_file="setup.cfg",
#                 cert=None,
#                 client_cert=None,
#                 repository_url=None
#             )
#
#         twine_upload.upload(
#             dists=["dist/*"],
#             repository=self.repository,
#             sign=False,
#             identity=None,
#             username=PYPI_USERNAME,
#             password=PYPI_PASSWORD,
#             comment=None,
#             sign_with="gpg",
#             config_file="setup.cfg",
#             skip_existing=True,
#             cert=None,
#             client_cert=None,
#             repository_url=None
#         )
#
#     def initialize_options(self):
#         self.repository = 'pypi'
#
#     def finalize_options(self):
#         self.announce('using repository `%s`' % self.repository, level=distutils.log.INFO)


setup(
    name=PACKAGE,
    version=VERSION,
    description='test app',
    long_description=README,
    classifiers=[
        "Programming Language :: Python",
    ],
    author='Very Good',
    author_email='dev@vgs.io',
    license='MIT License',
    packages=[PACKAGE],
    include_package_data=True,
    zip_safe=False,
    scripts=scripts,
    dependency_links=parse_dependency_links(),
    install_requires=parse_requirements(),
    extras_require=extras_require,
    tests_require=extras_require['tests'],
    test_suite='nose.collector'
)
