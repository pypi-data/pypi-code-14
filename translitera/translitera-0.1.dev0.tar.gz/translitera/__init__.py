# -*- coding: utf-8 -*-
# Copyright (C) Srikanth Anantharam 2016
"""
Created on Mon Aug  8 08:19:47 2016

@title:   translitera
@author:  Srikanth Anantharam <srikanth_anantharam@linux.com>
@purpose: Phonetic transliteration of text in Kannaḍa script into Latin/English characters
"""

import os, json, getopt, codecs

"load the phonetic transliteration data"
k2e_file = codecs.open(os.path.join(os.path.dirname(__file__), 'kannaḍa_to_latin.json'), encoding='utf-8')
k2e = json.load(k2e_file)
k2e_file.close()

def translitera(text):
    "the core logic to perform the transliteration"
    phonemes = u''
    for index in range(len(text)):
        phonemes += k2e.get(text[index:index+2], k2e.get(text[index], text[index]))
    return(phonemes)

def validate(path):
    if os.path.exists(path):
        if os.path.isfile(path) or os.path.isdir(path):
            return True;
        else:
            os.sys.stderr.write("PathError: '" + path + "' is not a file/directory\n")
    else:
        os.sys.stderr.write("PathError: the file/directory '" + path + "' doesn't exist\n")

def translitera_cat(paths):
    for path in paths:
        if validate(path):
            f = codecs.open(path)
            text = translitera(f.read())
            os.sys.stdout.write(text)

def file_directory_renamer(path):
    if validate(path):
        (pathwithoutext, ext) = os.path.splitext(path)
        dirname = os.path.dirname(pathwithoutext)
        name = os.path.basename(pathwithoutext)
        newname = translitera(name)
        newabsname = os.path.join(dirname, newname + ext)
        os.rename(path, newabsname)

def directory_contents_renamer(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            contents = os.listdir(path)
            for name in contents:
                file_directory_renamer(os.path.join(path, name))
        else:
            os.sys.stderr.write("PathError: '" + path + "' is not a directory\n")
    else:
        os.sys.stderr.write("PathError: the directory '" + path + "' doesn't exist\n")

def usage():
    "displays usage informtion"
    print("translitera: " + "phonetic transliteration of text in Kannaḍa script into Latin/English characters")
    print("Usage: " + "translitera [filename(s)]")
    print("Options:")
    print(" -h or --help, display this help message")
    print(" -t <Kannaḍa text>, transliterates the text in Kannaḍa script")
    print(" -r <file/directory name>, transliterates the file/directory")
    print(" -b <directory>, transliterates the name of files within a directory")
    return(2)

def main():
    "main function"
    try:
        opts, args = getopt.getopt(os.sys.argv[1:], "b:r:t:h", ("help",))
    except getopt.GetoptError:
        print("Error: invalid argument")
        os.sys.exit(usage())

    for opt in opts:
        if opt[0] == "-h" or opt[0] == "--help":
            usage()
            os.sys.exit(0)
        if opt[0] == "-t":
            print(translitera(opt[1]))
            os.sys.exit(0)
        if opt[0] == "-r":
            file_directory_renamer(opt[1])
            os.sys.exit(0)
        if opt[0] == "-b":
            directory_contents_renamer(opt[1])
            os.sys.exit(0)

    if args != []:
        translitera_cat(args)
        os.sys.exit(0)

    while True:
        text = os.sys.stdin.read()
        if len(text) == 0:
            break
        else:
            os.sys.stdout.write(translitera(text))
    
    os.sys.stdout.flush()
    return (0)

if __name__ == "__main__":
    "entry point"
    os.sys.exit(main())
