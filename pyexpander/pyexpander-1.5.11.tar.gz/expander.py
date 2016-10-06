#! /usr/bin/env python
# -*- coding: UTF-8 -*-

# pylint: disable=C0322,C0103,R0903

from optparse import OptionParser
#import string
import os.path
import sys

import pyexpander

# version of the program:
__version__= "1.5.11" #VERSION#

assert __version__==pyexpander.__version__

def process_files(options,args):
    """process all the command line options."""
    my_globals={}
    if options.eval is not None:
        for expr in options.eval:
            # pylint: disable=W0122
            exec expr in my_globals
            # pylint: enable=W0122
    filelist= []
    if (options.file is not None):
        filelist= options.file
    if len(args)>0: # extra arguments
        filelist.extend(args)
    if len(filelist)<=0:
        pyexpander.expandFile(sys.stdin,
                              my_globals,
                              options.simple_vars,
                              options.include)
    else:
        for f in filelist:
            # all files are expanded in a single scope:
            my_globals= \
                pyexpander.expandFile(f,
                                      my_globals,
                                      options.simple_vars,
                                      options.include)

def script_shortname():
    """return the name of this script without a path component."""
    return os.path.basename(sys.argv[0])

def print_summary():
    """print a short summary of the scripts function."""
    print ("%-20s: a powerful macro expension language "+\
           "based on python ...\n") % script_shortname()

def main():
    """The main function.

    parse the command-line options and perform the command
    """
    # command-line options and command-line help:
    usage = "usage: %prog [options] {files}"

    parser = OptionParser(usage=usage,
                          version="%%prog %s" % __version__,
                          description="expands macros in a file "+\
                                      "with pyexpander.")

    parser.add_option("--summary",  # implies dest="nodelete"
                      action="store_true", # default: None
                      help="print a summary of the function of the program",
                      )
    parser.add_option("-f", "--file", # implies dest="file"
                      action="append", # OptionParser's default
                      type="string",  # OptionParser's default
                      help="specify a FILE to process. This "+\
                           "option may be used more than once "+\
                           "to process more than one file but note "+\
                           "than this option is not really needed. "+\
                           "Files can also be specified directly after "+\
                           "the other command line options.",
                      metavar="FILE"  # for help-generation text
                      )
    parser.add_option("--eval", # implies dest="file"
                      action="append", # OptionParser's default
                      type="string",  # OptionParser's default
                      help="evaluate PYTHONEXPRESSION in global context.",
                      metavar="PYTHONEXPRESSION"  # for help-generation text
                      )
    parser.add_option("-I", "--include",
                      action="append", # OptionParser's default
                      type="string",  # OptionParser's default
                      help="add PATH to the list of include paths",
                      metavar="PATH"  # for help-generation text
                      )
    parser.add_option("-s", "--simple-vars",   # implies dest="switch"
                      action="store_true", # default: None
                      help="allow variables without brackets",
                      )

    # x= sys.argv
    (options, args) = parser.parse_args()
    # options: the options-object
    # args: list of left-over args

    if options.summary:
        print_summary()
        sys.exit(0)

    process_files(options,args)
    sys.exit(0)

if __name__ == "__main__":
    main()

