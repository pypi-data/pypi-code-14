from setuptools import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='ndtree',
      version='0.1',
      description='bin-, quad-, oct- tree for mesh refinements',
      long_description=read('README'),
      url='http://github.com/leonshting/ndtree',
      author='Leonid Shtanko',
      author_email='leonshting@gmail.com',
      license='MIT',
      packages=['ndtree'],
      install_requires=[
          'numpy'
      ],
      zip_safe=False)
