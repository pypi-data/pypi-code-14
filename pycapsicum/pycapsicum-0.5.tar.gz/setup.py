from setuptools import setup, Extension, find_packages

setup(name='pycapsicum',
      version='0.5',
      description="Python interface to FreeBSD capsicum security system",
      long_description=
      """Pycapsicum provides an easy python interface to the capsicum
         (capabilites) system and the cap_rights_t for FreeBSD.
      """,
      author="Chris Stillson",
      author_email="stillson@gmail.com",
      license="New BSD license",
      url='https://github.com/stillson/pycapsicum2',
      ext_modules=[Extension('_pycapsicum', ['_pycapsicum.c'])],
      py_modules = ['pycapsicum',],
      keywords = ["capsicum","freebsd","sandbox","capabilities"],
      classifiers = [ "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Topic :: Security",],
)
