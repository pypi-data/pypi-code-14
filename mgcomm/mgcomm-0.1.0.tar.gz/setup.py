import sys

from setuptools import setup, find_packages


with open('README.md') as f_:
    long_description = f_.read()


def main():
    setup(name='mgcomm',
          description='small utility library with handy fixtures',
          long_description=long_description,
          use_scm_version={'write_to': 'src/mgcomm/_version.py'},
          license='MIT',
          author='Michał Góral',
          author_email='dev@mgoral.org',
          url='https://gitlab.com/mgoral/mgcomm',
          platforms=['linux'],
          setup_requires=['setuptools_scm'],

          # https://pypi.python.org/pypi?%3Aaction=list_classifiers
          classifiers=['Development Status :: 2 - Pre-Alpha',
                       'Environment :: Console',
                       'Intended Audience :: Developers',
                       'License :: OSI Approved :: MIT License',
                       'Natural Language :: English',
                       'Operating System :: POSIX',
                       'Programming Language :: Python :: 3 :: Only',
                       'Topic :: Software Development :: Libraries',
                       'Topic :: Utilities',
                       ],

          packages=find_packages('src'),
          package_dir={'': 'src'},
          )

if __name__ == '__main__':
    assert sys.version_info >= (3, 3)
    main()
