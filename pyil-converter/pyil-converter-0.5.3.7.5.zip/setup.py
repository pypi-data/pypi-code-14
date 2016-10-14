try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import re, sys, pip, platform, time, shutil, os

v = '0.5.3.7.5'
avi = {'x32_34':   r'resources\lxml-3.6.4-cp34-cp34m-win32.whl',
       'AMD64_34': r'resources\lxml-3.6.4-cp34-cp34m-win_amd64.whl',
       'x32_35':   r'resources\lxml-3.6.4-cp35-cp35m-win32.whl',
       'AMD64_35': r'resources\lxml-3.6.4-cp35-cp35m-win_amd64.whl',
       'none':     """I can't find the version of lxml wheel that fit this platform
        or this version of python, that means you may not be able to use the
        convert_to_docx() function. However, if you figure out a way to install
        lxml and did it, reinstall pyil-converter or call reinstall function."""}
ire = ['Python-Docx', 'binaryornot', 'openpyxl', 'dill']


def install(file):
    if file.endswith('.whl'):
        try:
            temp5 = pip.main(['install', file])
            if temp5 != 0:
                raise Exception()
            print('Successfully installed lxml!')
            print('Will now continued the installation of pyil-converter.')
            return
        except Exception:
            pass
    print(file)
    del ire[0]
    time.sleep(3)


def what():
    with open('CHANGELOG.log')as file:
        temp6 = file.read()
        tempre = re.compile('v' + v + '.+', flags=re.DOTALL)
        tempm = tempre.search(temp6)
        print('\n\n', tempm.group(0), '\n\n')


def read(name):
    with open(name) as file:
        return file.read()


what()

final = ''
temp1 = platform.machine()
temp2 = re.compile('x86')
temp2.sub('AMD64', temp1)
final += temp1
temp1 = sys.version
temp2 = re.compile(r'\d+(\.\d\.)\d+')
temp3 = temp2.search(temp1)
temp4 = temp3.group()
temp1 = temp4[0] + temp4[2]
final += '_' + temp1
install(avi.get(final, avi['none']))

try:
    setup(
        name='pyil-converter',
        version=v,
        packages=['pyil'],
        license='MIT',
        author='G.M',
        author_email='G.Mpydev@gmail.com',
        description='Convert files to the format you want!',
        long_description=read('README.md'),
        install_requires=ire.copy(),
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
                  'converting', 'data'],
        url=r'https://wasted123.github.io/pyil/'
    )
    print('Installation succeeded.')

except Exception as msg:
    print('\n')
    print('An unexpected exception happened.')
    print()
    print(str(msg))
    print('\n')
    print('Please read the exception and google it.')
finally:
    if not os.path.exists(r'C:\ind'):
        print('Finding python path.')
        from pyil.util import search_file

        result = [search_file('python.exe', caseI=True), search_file('pythonw.exe', caseI=True)]
        content = open(r'.\pyil\enum\variable.py').readlines()
        content = content[:-3]
        print('Done!\nModifying source code.')
        with open(r'.\pyil\enum\variable.py', 'w')as f:
            for i in content:
                f.write(i)
            print("pythonPath=r'" + result[0] + "'", file=f)
            print("pythonPath2=r'" + result[1] + "'", file=f)
            print(file=f)

    print('Removing source package of lxml.')
    if not os.path.exists(r'C:\ind'):
        shutil.rmtree(r'.\resources', ignore_errors=True)
    print('Process completed, you can now close this window.')
