
import math, os, shutil, sys, subprocess
from bl.file import File

DEBUG=False

class Image(File):

    def gm(self, cmd, **params):
        args = ['gm', cmd]
        for key in params.keys():
            args += ['-'+key, str(params[key])]
        args += [self.fn]
        if DEBUG==True: print(args)
        o = subprocess.check_output(args).decode('utf8')
        return o.strip()

    def mogrify(self, **params):
        return self.gm('mogrify', **params)

    def identify(self, **params):
        return self.gm('identify', **params)

    def convert(self, outfn, **params):
        args = ['gm', 'convert', self.fn]
        for key in params.keys():
            args += ['-'+key, str(params[key])]
        args += [outfn]
        if DEBUG==True: print(args)
        o = subprocess.check_output(args).decode('utf8')
        return o.strip()
                