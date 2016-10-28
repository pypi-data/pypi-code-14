from setuptools import setup

long_description = ''
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = open('README.md').read()

setup(name='MimirNotes',
      version='0.4.7',
      description='A simple, command line, note taking utility.',
      long_description=long_description,
      keywords='note terminal command-line journal',
      url='https://github.com/jcerise/mimir',
      author='Jeremy Cerise',
      author_email='jcerise06@gmail.com',
      packages=['MimirNotes'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['click', 'enum34', 'dateparser'],
      entry_points='''
            [console_scripts]
            mimir=MimirNotes.mimir:cli
      ''',
      )
