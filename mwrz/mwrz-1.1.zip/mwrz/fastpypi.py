pypirc_config = """[distutils]
index-servers =
  pypi
  pypitest

[pypi]
repository=https://pypi.python.org/pypi
username=your_username
password=your_password

[pypitest]
repository=https://testpypi.python.org/pypi
username=your_username
password=your_password
"""


LICENSE_txt = """ Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION"""

setup_py = """from distutils.core import setup

setup(
  name = '{packageName}',
  packages=['{packageName}'],# this must be the same as the name above
  version = '1.0',
  scripts=['{packageName}/pyScript.py'],
  description = "there is a simple introduction",
  long_description="details",
  author = 'author',
  author_email = 'author_email@gmail.com',
  url = 'http://github_package', # use the URL to the github repo
  download_url = 'http://github_can_download_package',
  keywords = [], # arbitrary keywords
  classifiers = [],
  install_requires = ['', ''], # dependencies needed
  license="Apache-2.0"
)
"""

README_md = """explain your package
"""

setup_cfg = """[metadata]
description-file = README.md

"""

example_pyscript = """def main():
    pass

if __name__ == '__main__':
    main()
"""

final_upload = """
python setup.py register -r pypitest
python setup.py sdist upload -r pypitest
python setup.py register -r pypi
python setup.py sdist upload -r pypi
"""

import easyargs
import os

@easyargs
def main(packagename = 'wonderful_package'):
    try:
        os.mkdir('myNewPackage')
        os.chdir('myNewPackage')
        with open('.pypirc', 'w') as f :
            f.write(pypirc_config)
            print('You should put .pypirc at ~/.pypirc and change the name and password !!!')
            print('If in windows, use "echo %HOMEPATH%" to find HOME')
        with open('setup.py', 'w') as f :
            f.write(setup_py.format(packageName = packagename))
            print('You should change the setup.py for yourself !!!')
        with open('README.md', 'w') as f :
            f.write(README_md)
        with open('setup.cfg', 'w') as f :
            f.write(setup_cfg)
        with open('LICENSE.txt', 'w') as f :
            f.write(LICENSE_txt)
        os.mkdir(packagename)
        os.chdir(packagename)
        with open('__init__.py','w') as f :
            f.write('')
        with open('pyScript.py', 'w') as f :
            f.write(example_pyscript)
        print("Last, use below commands to upload:")
        print(final_upload)
    except Exception as e:
        print('Somethin error happened : \n', e)

if __name__ == '__main__':
    main()