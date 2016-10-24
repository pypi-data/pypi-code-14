# this file has been auto generated. Do not edit.

import os

def find_packages(name):
    packages = []
    for dir,subdirs,files in os.walk(name):
        package = dir.replace(os.path.sep, '.')
        if '__init__.py' not in files:
            # not a package
            continue
        packages.append(package)
    return packages


from setuptools import setup

setup(name='nose_warnings_filters',
      version='0.1.3',
      description='Allow to inject warning filters during ``nosetest``.\n\nPut the same arguments as ``warnings.filterwarnings`` in ``setup.cfg``\nat the root of your project. Separated each argument by pipes ``|``, one\nfilter per line. Whitespace are stripped.\n\nfor example:\n\n::\n\n    [nosetests]\n    warningfilters=default         |.*            |DeprecationWarning |notebook.*\n                   ignore          |.*metadata.*  |DeprecationWarning |notebook.*\n                   once            |.*schema.*    |UserWarning        |nbfor.*\n                   error           |.*warn.*      |DeprecationWarning |notebook.services.contents.manager*\n\nIf you prefer another name for the configuration file, you can tell nose\nto load the configuration using the ``-c`` flag: run the tests with\n``nosetests -c nose.cfg``.\n\ndetails configuration.\n======================\n\nEach line of warning filter is separated in maximum 4 sections, that\nmatch the first 4 sections of ``filterwarnings``:\n\n.. code:: python\n\n    filterwarnings(action, message="", category=Warning, module="", lineno=0, append=False)\n\nfields 2 to 4 can be omitted, ie to say 1 line can be of the following\nform:\n\n::\n\n    action\n    action| message\n    action| message | category\n    action| message | category | module\n\nthe value of each fields is treated the same as for ``filterwarnigns``\nexcept: - whitespace are trimmed. - if the ``category`` has dots, the\ncorresponding class try to be imported. If it does not have dots, the\nname is looked up in ``builtins`` or ``__builtins__``\n\ntest are failing\n================\n\nFor some reasons in some systems tests are failing; it seem that this\npackage have difficulty to self-test. That\'s likely due to the fact that\nthe tested package need to be in different namespaces, and by\nself-testing we break this assumption.\n',
      url='https://github.com/Carreau/nose_warnings_filters',
      author='Matthias Bussonnier',
      author_email='bussonniermatthias@gmail.com',
      license='MIT',
      packages=find_packages('nose_warnings_filters'),
      python_requires='>=2.7',
      install_requires=[
          ['nose']
      ],
      zip_safe=False,
      entry_points= {
          'nose.plugins.0.10':[
                'warningfiltersx = nose_warnings_filters:WarningFilter'
          ]
        }
      )
# this file has been auto generated. Do not edit.
