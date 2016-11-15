from setuptools import setup, find_packages
import os

version = '2.1.1'

setup(name='rer.al.mcorevideoportlet',
      version=version,
      description="This package is used to show mediacore video into a portlet",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.rst")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        'Framework :: Plone :: 4.1',
        'Framework :: Plone :: 4.2',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='plone video mediacore',
      author='RedTurtle Technology',
      author_email='sviluppoplone@redturtle.it',
      url='https://github.com/PloneGov-IT/rer.al.mcorevideoportlet',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['rer', 'rer.al'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.rtvideo.mediacore',
          'Paste==1.7.5.1'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
