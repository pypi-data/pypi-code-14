##http://peterdowns.com/posts/first-time-with-pypi.html
##https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/

from setuptools import setup, find_packages

CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
INSTALL_REQUIRES = ["names >= 0.3.0"]

from distutils.core import setup

if __name__ == "__main__":
    setup(
      name = 'automation9',
      packages = ['automation9'], # this must be the same as the name above
      version = '0.0.2',
      description = 'An automation library',
      author = 'Nikola Dang',
      author_email = 'ducthinhdt@gmail.com',
      url = 'https://github.com/nikoladang/automation9', # use the URL to the github repo
      download_url = 'https://github.com/nikoladang/automation9/tarball/0.1', # I'll explain this in a second
      keywords = ['testing', 'logging', 'example', 'automation', 'signing'], # arbitrary keywords
      classifiers = CLASSIFIERS,
      install_requires=INSTALL_REQUIRES,
    )
