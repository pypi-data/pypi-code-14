try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
setup(name='streamplot', 
      version='1.0',
      description='Real Time Plots with pyqtgraph',
      url="https://github.com/GuillaumeGenthial/streamplot/tarball/1.0", 
      py_modules=["streamplot"], 
      author='Guillaume Genthial',
      author_email='genthial@stanford.edu',
      license='MIT',
      install_requires=[
          'numpy',
          'pyqtgraph',
      ],
      zip_safe=False)


# Tag
# git tag 0.1 -m "Adds a tag so that we can put this on PyPI."
# git push --tags origin master

# Test
# python setup.py register -r pypitest
# python setup.py sdist upload -r pypitest

# pip install -i https://testpypi.python.org/pypi streamplot

# Real
# python setup.py register -r pypi
# python setup.py sdist upload -r pypi
