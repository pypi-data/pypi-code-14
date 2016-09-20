# 项目：标准函数库
# 模块：Python相关实用命令
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2015-08-09 07:50
# 修订：2016-03-19
# 修订：2016-5-12
import sys
import os
from orange import Path,exec_shell

def pytest():
    import unittest
    sys.path.insert(0,'.')
    unittest.main('testing')

def pysdist():
    if Path('setup.py').is_file():
        cmd='setup.py sdist --dist-dir "%s"'%(Path('~/OneDrive/pylib'))
        if os.name!='nt':
            cmd='python3 %s'%(cmd)
        exec_shell(cmd)
        for path in Path('.').glob('*.egg-info'):
            print('Path %s has beed deleted!'%(path))
            if path.is_dir():
                path.rmtree()
    else:
        print('没有找到setup.py文件！')
    
"""
import os
import re
import sys
from distutils.version import StrictVersion as Version
from .stdlib import exec_shell
from .path import Path
from glob import glob
from shutil import rmtree,move

version_re = re.compile(r'(\d+) \. (\d+) (\. (\d+))? ([ab](\d+))?',
        re.VERBOSE | re.ASCII)
lib_path='~/OneDrive/pylib'
package_exts=('.tar.gz','.whl','.zip')


def pytest():
    import unittest
    sys.path.append('.')
    unittest.main('testing')

def parse_package(path):
    def split(pkg_name):
        k=version_re.search(pkg_name)
        if k:
            v=Version()
            (major, minor, patch, prerelease, prerelease_num) = \
                k.group(1, 2, 4, 5, 6)

            if patch:
                v.version = tuple(map(int, [major, minor, patch]))
            else:
                v.version = tuple(map(int, [major, minor])) + (0,)

            if prerelease:
                v.prerelease = (prerelease[0], int(prerelease_num))
            else:
                v.prerelease = None
            name=pkg_name[:k.start(0)-1]
            return name,v
    if os.path.exists(path):
        pkg_name=os.path.basename(path)
    else:
        return None,None
    if os.path.isfile(path):
        for ext in package_exts:
            if path.endswith(ext):
                break
        else:
            return None,None
    return split(pkg_name)

def get_package(pkg_name,path='.'):
    files=glob('%s/*%s*'%(path,pkg_name))
    v=Version('0.0')
    path=None
    for file in files:
        name,ver=parse_package(file)
        if name==pkg_name:
            if ver>v:
                v=ver
                path=file
    else:
        return path 

def pkgmgr(packages=None,download=False,path='.'):
    path=os.path.expanduser(path)
    if download and packages:
        cmd='install -d "%s" %s'%(
            path," ".join(packages))
        if os.name=='nt':
            cmd='pip %s'%(cmd)
        else:
            cmd='pip3 %s'%(cmd)
        exec_shell(cmd)
    else:
        pkgs=[]
        for pkg in packages:
            pkg_path=get_package(pkg,path)
            if pkg_path:
                pkgs.append('"%s"'%(pkg_path))
            else:
                pkgs.append(pkg)
        cmd="install %s"%(" ".join(pkgs))
        if os.name=='nt':
            cmd='pip %s'%(cmd)
        else:
            cmd='pip3 %s'%(cmd)
        exec_shell(cmd)
            
def pkg_mgr(argv=sys.argv[1:]):
    args=[{'arg':'-d,--download',
           'action':'store_true',
           'help':'下载指定的包',},
           {'arg':'packages',
            'nargs':'*',
            'metavar':'package',
            'help':'指定的软件包',},
        {'arg':'-p,--path',
         'nargs':'?',
         'default':'~/Onedrive/pylib',
         'help':'指定的路径',}]
    parse_args(args,argv=argv,func=pkgmgr)
    
def pysetup():
    if os.path.isfile('setup.py'):
        if os.name=='nt':
            exec_shell('setup.py install')
        elif sys.platform=='darwin':
            exec_shell('python3 setup.py install')
        else:
            exec_shell('sudo python3 setup.py install')
        pyclean()
    else:
        print('没有找到setup.py文件！')
        
def pysdist():
    if Path('setup.py').is_file():
        if os.name=='nt':
            exec_shell('setup.py sdist')
        else:
            exec_shell('python3 setup.py sdist')
        dst=Path(os.path.expanduser(lib_path))
        for source_file in Path("dist").glob("*.*"):
            dst_file=dst/source_file.name
            source_file.resolve()
            source_file.replace(dst_file)
        pyclean()
    else:
        print('没有找到setup.py文件！')
    
def pyclean():
    dirs=glob('build')
    dirs.extend(glob('dist'))
    dirs.extend(glob('*egg-info'))
    for _dir in dirs:
        rmtree(_dir)

def py_setup(packages=None,download=False,\
             path=None,install=False):
    if packages:
        for package in packages:
            print('pip install %s'%(package))
    else:
        if os.name=='nt':
            print('setup.py install')
        elif sys.platform=='darwin':
            print('python3 setup.py install')
        else:
            print('sudo python3 setup.py install')
            

def _pysetup(argv=None):
    '''
    安装Python程序的入口程序
    '''
    args=[{'arg':'packages',
           'nargs':'*',
           'metavar':'package',
           'help':'指定的包',},
        {'arg':'-d,--download',
            'action':'store_true',
            'help':'仅下载指定的包',},
        {'arg':'-p,--path',
            'nargs':'?',
            'help':'指定的目录',},
        {'arg':'-i,--install',
             'nargs':'?',
             'help':'从互联网下载并安装',}
           ]
    parse_args(args,argv=argv,func=py_setup,print_usage=False)

"""
