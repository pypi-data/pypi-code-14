from setuptools import setup

setup(name='pyblog',
      version='0.3',
      description='Dirt-simple static blog general',
      url='http://github.com/cesarparent/pyblog',
      author='Cesar Parent',
      author_email='cesar@cesarparent.com',
      license='MIT',
      packages=['pyblog'],
      install_requires=[
          'markdown',
          'jinja2',
		  'pygments'
      ],
      entry_points = {
          'console_scripts': [
              'pyblog-init = pyblog.cli:pyblog_init',
              'pyblog-build = pyblog.cli:pyblog_build'
          ],
      },
      zip_safe=False)