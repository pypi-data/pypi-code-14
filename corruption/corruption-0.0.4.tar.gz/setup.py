from distutils.core import setup

import corruption

version = corruption.__version__

setup(
  name="corruption",
  description="A Zalgo Text Generator",
  long_description=open("README.txt").read(),
  version=version,
  author="James Lee",
  author_email="0x0uLL@gmail.com",
  url="https://github.com/amesee/corruption",
  py_modules=["corruption"],
  license="MIT",
  classifiers=[
    "Development Status :: 2 - Pre-Alpha",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: POSIX",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Topic :: Text Processing",
  ],
)
