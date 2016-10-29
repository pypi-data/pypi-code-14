from setuptools import setup
from timelineio import __version__

BASE_CVS_URL = 'http://github.com/filwaitman/timelineio'

setup(
    name='timelineio',
    packages=['timelineio', ],
    version=__version__,
    author='Filipe Waitman',
    author_email='filwaitman@gmail.com',
    install_requires=[x.strip() for x in open('requirements.txt').readlines()],
    url=BASE_CVS_URL,
    download_url='{}/tarball/{}'.format(BASE_CVS_URL, __version__),
    test_suite='tests',
    tests_require=[x.strip() for x in open('requirements_test.txt').readlines()],
    keywords=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
)
