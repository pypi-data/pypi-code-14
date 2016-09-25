#!/usr/bin/env python
# -*- coding: utf-8 -*-
# manage optionparser
# you can decorator
# sample
# @verb('verb1', 'alias1', usage='my usage', description='my description')
# @alias('alias2')
# @arg('-H', dest='arg1', type=str, help="help for arg1")
# def my_function(arg1):
#     print(arg1)
#
# if __name__ == '__main__':
#      parser = VerbParser()
#      parser.version = "%s %s" % (PROG, VERSION)
#      parser.description= "DESCRIPTION"
#      parser.epilog = "AUTHOR"
#      parser.parse_args()
#
# can use main.py verb1 -H tutu

import sys
from optparse import OptionParser, IndentedHelpFormatter

if 'stdinfo' not in dir(sys):
    sys.stdinfo = sys.stdout


ADD_DESC_FOR_VERB = True

def verb(*args,  **kwargs):
    if args and callable(args[0]):
        func = args[0]
        verbs = args[1:]
    else:
        func = None
    if func is None:
        def cmd_inner(func):
            return verb(func,*args, **kwargs)
        return cmd_inner
    else:
        kwargs['verb'] = verbs[0]
        VerbParser().add_verb(func, **kwargs)
        for alias in verbs[1:]:
            VerbParser().add_alias(func, alias)
        return func

def alias(*args,  **kwargs):
    if args and callable(args[0]):
        func = args[0]
        for k in args[1:]:
            VerbParser().add_alias(func, k)
        return func
    else:
        def alias_inner(func):
            return alias(func,*args, **kwargs)
        return alias_inner
 
def arg(*args, **kwargs):
    if args and callable(args[0]):
        func = args[0]
        args = args[1:]
    else:
        func = None
    if func is None:
        def arg_inner(func):
            return arg(func, *args, **kwargs)
        return arg_inner
    else:
        VerbParser().add_arg(func, args, **kwargs)
        return func

class PlainHelpFormatter(IndentedHelpFormatter):
    def format_description(self, description):
        if description:
            return description + "\n"
        else:
            return ""
    def format_epilog(self, epilog):
        if epilog:
            return epilog + "\n"
        else:
            return ""

class SingletonParser(object):
    """ renvoie tjrs la même instance """
    _ref = None
    def __new__(cls, *args, **kw):
        if cls._ref is None:
            cls._ref = super(SingletonParser, cls).__new__(cls, *args, **kw)
            cls._ref.funcs = {}
        return cls._ref

class VerbParser(SingletonParser, OptionParser):
    """
        create VerbParser
    """
    def __init__(self, **kw):
        OptionParser.__init__(self, formatter = PlainHelpFormatter(), **kw)
        self._add_version_option()


    def __add_func(self, func):
        if func.__name__ not in self.funcs:
             self.funcs[func.__name__] = {
                 'func' : func,
                 'alias' : [],
                 'args' : {}
            }

    def add_verb(self, func, **kw):
        self.__add_func(func)
        for k in kw:
            self.funcs[func.__name__][k] = kw[k]
    
    def add_arg(self, func, arg, **kw):
        self.__add_func(func)
        self.funcs[func.__name__]['args'][arg[0]] = {
            'arg' : arg,
            'kw' : kw
        }

    def add_alias(self, func, alias):
        self.__add_func(func)
        self.funcs[func.__name__]['alias'] = self.funcs[func.__name__]['alias'] + [alias,]

    def get_func(self, verb):
        for f in self.funcs:
            if self.funcs[f].get('verb','') == verb or verb in self.funcs[f]['alias']:
                return self.funcs[f]
        self.error("verb %s doesn't exist" % verb)

    def parse_args(self):
        self._basic()
        func = self.get_func(sys.argv[1])
        checking = {}
        #add arg in parser
        for args in func['args']:
            arg = func['args'][args]['arg']
            kw = func['args'][args]['kw']
            if 'check' in kw:
                checking[kw['dest']] = kw['check']
                del kw['check']
            self.add_option(*arg, **kw)
        self.set_usage(func.get('usage','%s %s [options]' % (self.prog, sys.argv[1])))
        self.description = func.get('description', '\n'.join([l.strip() for l in func['func'].__doc__.split('\n')]))
        # del verb in sys.argv
        sys.argv.pop(1)
        (options, args) = OptionParser.parse_args(self)
        # load check args
        for arg in checking:
            setattr(options,arg,checking[arg](func['verb'], arg,getattr(options,arg)))
        func['func'](*args, **options.__dict__)
    
    def _get_usage(self):
        verbs = [self.funcs[f].get('verb','') for f in self.funcs]
        for func in self.funcs:
            verbs= verbs + self.funcs[func].get('alias',[])
        return """%s [-h] [-v] {%s} ... """ % (self.prog, ','.join(sorted(verbs)))
    
    def _basic(self):
        self.usage = self._get_usage()
        if ADD_DESC_FOR_VERB:
            try:
                self.description = self.description + '\n\n'
                for f in sorted(self.funcs):
                    desc = self.funcs[f].get('description',self.funcs[f]['func'].__doc__.split('\n')[0])
                    if self.funcs[f].get('verb',''):
                        self.description =  self.description + '- %s : %s\n' % (self.funcs[f]['verb'], desc)
                    for alias in self.funcs[f]['alias']:
                        self.description =  self.description + '- %s : %s\n' % (alias, desc)
            except:
                pass
        if not len(sys.argv) > 1:
            self.print_help()
            sys.exit(1)
        if sys.argv[1] in ("--help", "-h"):
            self.print_help()
            self.print_version()
            sys.exit(0)
        if sys.argv[1] in ("--version","-v"):
            self.print_version()
            sys.exit(0)
    
    def print_version(self, stream=None):
        OptionParser.print_version(self, sys.stdinfo)
    
    def print_help(self, stream=None):
        OptionParser.print_help(self, sys.stdinfo)
