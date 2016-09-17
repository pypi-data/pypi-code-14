from setuptools import setup

setup(name='pyblog',
      version='0.5',
      description='Dirt-simple static blog general',
      url='http://github.com/cesarparent/pyblog',
      author='Cesar Parent',
      author_email='cesar@cesarparent.com',
      license='MIT',
      packages=['pyblog'],
      install_requires=[
          'markdown',
          'jinja2',
		  'pygments',
          'watchdog'
      ],
      entry_points = {
          'console_scripts': [
              'pyblog = pyblog.entry:main'
          ],
      },
      zip_safe=False)