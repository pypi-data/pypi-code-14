import sys
import yaml
from os.path import expanduser

def main():
    """Entry point for the application script"""
    #filex=open( expanduser('~/etc/helloworld.conf') )
    filex=open( expanduser('~/.local/etc/helloworld.conf') )
    conf= filex.read()
    filex.close()
    yamlConf = yaml.load(conf)

    if len(sys.argv) > 1:
        print("%s %s"%( yamlConf['banner'] ,  sys.argv[1]) )
    else:
        print("%s"%( yamlConf['banner'] ) )

def add(arg1,arg2):
    """ Add two values arg1 and arg2 """
    return arg1+arg2

