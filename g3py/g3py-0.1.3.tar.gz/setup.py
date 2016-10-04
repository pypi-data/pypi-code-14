from setuptools import setup

setup(name='g3py',
      version='0.1.3',
      description='Generalized Graphical Gaussian Processes',
      #url='http://github.com/storborg/funniest',
      author='Gonzalo Rios',
      author_email='grios@dim.uchile.cl',
      license='MIT',
      packages=['g3py'],
      install_requires=[
          'numpy','scipy','matplotlib','seaborn'
      ],
      zip_safe=False)
