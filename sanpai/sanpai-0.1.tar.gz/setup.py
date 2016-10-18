from setuptools import setup


def readme():
    with open('README.rst', 'r') as f:
        return f.read()


setup(name='sanpai',
      version='0.1',
      description='sanpai is a tool for inspecting and diffing SANs on x509 certificates',
      long_description=readme(),
      classifiers=['Intended Audience :: Developers',
                   'Intended Audience :: Information Technology',
                   'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
                   'Natural Language :: English',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 2.7',
                   'Topic :: Software Development :: Testing',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Topic :: System :: Filesystems',
                   'Topic :: Utilities'],
      keywords='x509 cert inspect diff subject alternative name san domain openssl crypto cryptography ssl https',
      url='http://github.com/blaketmiller/sanpai',
      author='Blake Miller',
      author_email='blakethomasmiller@gmail.com',
      license='GNU GPL v2.0',
      packages=['sanpai'],
      install_requires=['cryptography'],
      scripts=['bin/sanpai'],
      zip_safe=False)
