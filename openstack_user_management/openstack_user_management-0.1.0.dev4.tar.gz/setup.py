#!/usr/bin/env python
import setuptools

# In python < 2.7.4, a lazy loading of package `pbr` will break
# setuptools if some other modules registered functions in `atexit`.
# solution from: http://bugs.python.org/issue15881#msg170215
try:
    import multiprocessing  # noqa
except ImportError:
    from ez_setup import use_setuptools

    use_setuptools()
    from setuptools import setup
    # pass

setuptools.setup(
    setup_requires=['pbr>=1.8'],
    pbr=True)
