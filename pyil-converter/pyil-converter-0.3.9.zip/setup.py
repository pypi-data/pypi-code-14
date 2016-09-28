from setuptools import setup
import re
from re import DOTALL

v = '0.3.9'


def what():
    with open('''update.log''')as file:
        temp = file.read()
        tempre = re.compile('v' + v + '.+', flags=DOTALL)
        tempm = tempre.search(temp)
        print('\n\n', tempm.group(0), '\n\n')


def read(name):
    with open(name) as file:
        return file.read()


what()
try:
    setup(
        name='pyil-converter',
        version=v,
        packages=['pyil'],
        license='MIT',
        author='G.M',
        author_email='G.Mpydev@gmail.com',
        description='Convert files to the format you want!',
        long_description=read('README.rst'),
        install_requires=[
            'openpyxl', 'binaryornot'],
        include_package_data=True,
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python :: 3 :: Only',
            'Operating System :: Microsoft :: Windows',
            'Intended Audience :: Developers',
            'Intended Audience :: Information Technology',
            'Natural Language :: English',
            'Topic :: System :: Filesystems',
            'Topic :: System :: Archiving :: Packaging',
            'Topic :: Utilities',
            'License :: OSI Approved :: MIT License'
        ],
        platforms='win32',
        keywords=['file', 'format', 'extension', 'reformatting',
                                            'converting','data'],
        url=r'https://wasted123.github.io/pyil/'
    )
    print('Installation succeeded.')

except Exception as msg:
    print('\n')
    print('An unexpected exception happened.')
    print('\n')
    print(str(msg))
    print('\n')
    print('If it is because installation error, fro example '
          ' when compiling c extensions, an error occurred, I '
          'personally recommend try install the python wheel '
          'for the nodule you want to install.''')


