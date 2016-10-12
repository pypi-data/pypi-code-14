from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='MimirNotes',
      version='0.2.7',
      description='A simple, command line, note taking utility.',
      keywords='note terminal command-line journal',
      url='https://github.com/jcerise/mimir',
      author='Jeremy Cerise',
      author_email='jcerise06@gmail.com',
      packages=['MimirNotes'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['click', 'enum34'],
      entry_points='''
            [console_scripts]
            mimir=MimirNotes.mimir:cli
      ''',
      )
