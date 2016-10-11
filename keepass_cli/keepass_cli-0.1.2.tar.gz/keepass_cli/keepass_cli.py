#!/bin/env python
# -*- coding: utf-8 -*-

import libkeepass
from os import environ
from optparse import OptionParser


def getEntry(obj_root,entryPath, fieldName):
    """Return a specific field from the entry given by entryPath
    @:param The path to the entry (sperated by /)
    @:param fieldName The name of the field of which  the value should be returned.
    @:return The value of the field.
    """
    entryPath = entryPath.split('/')
    title = entryPath[-1]
    entryPath = entryPath[:-1]
    query = ".//Root/"
    for group in entryPath:
        query = query + "Group[Name='%s']/" % group
    query = query + "Entry[String[Key='Title' and Value='%s']]/String[Key='%s']/Value" % (title,fieldName)
    result = obj_root.xpath(query);
    if len(result) > 0:
        return obj_root.xpath(query)[0];
    else:
        return None

def listEntriesInGroup(obj_root, entryPath):
    """Return all entries in the given Group.
    @:param The path to the group (sperated by /)
    @:return A list of entries in the group.
    """
    entryPath = entryPath.split('/')
    query = ".//Root/"
    for group in entryPath:
        query = query + "Group[Name='%s']/" % group
    query = query + "Entry/String[Key='Title']/Value"
    return obj_root.xpath(query)

def listGroupsInGroup(obj_root, entryPath):
    """Return all groups in the given Group.
    @:param The path to the group (sperated by /)
    @:return A list of groups in the group.
    """
    entryPath = entryPath.split('/')
    query = ".//Root/"
    for group in entryPath:
        query = query + "Group[Name='%s']/" % group
    query = query + "Group/Name"
    return obj_root.xpath(query)

def entryTreeToObject(obj_root, entryPath, fieldNames):
    """Return a specific field from the entry given by entryPath
    @:param The path of which the tree should be returned (sperated by /)
    @:param fieldNames List fo the names of the field of which  the value should be returned.
    @:return An object tree (string map) with the lements in the given path.
    """
    result = {}
    for group in listGroupsInGroup(obj_root,entryPath):
        result[group] = entryTreeToObject(obj_root, entryPath + "/" + group, fieldNames)
    for entry in listEntriesInGroup(obj_root, entryPath):
        result[entry] = {}
        fn = fieldNames
        if fn == "*":
            fn = listEntriesInGroup(obj_root, entryPath)
        for fieldName in fn:
            result[entry][fieldName] = getEntry(obj_root, entryPath + "/" + entry, fieldName)
    return result

def entryTreeToKeyValue(obj_root, entryPath, fieldName):
    """Return a specific field from the entry given by entryPath
    @:param The path of which the tree should be returned (sperated by /)
    @:param fieldNames List fo the names of the field of which  the value should be returned.
    @:return An object tree (string map) with the lements in the given path.
    """
    result = []
    for group in listGroupsInGroup(obj_root,entryPath):
        tmp = entryTreeToKeyValue(obj_root,entryPath + "/" + group, fieldName)
        for entry in tmp:
            result.append(group + "." + entry)
    for entry in listEntriesInGroup(obj_root, entryPath):
        result.append(entry + "=" + str(getEntry(obj_root, entryPath + "/" + entry, fieldName)))
    return result

def main():
    env_password = environ.get('KEEPASS_PASSWORD')

    usage = "Usage: %prog command options\n\ncommand my be one of show-entry, list-entries, to-json and to-keyvalue"

    parser = OptionParser(usage=usage)
    parser.add_option("-f", "--file", dest="filename",
                      help="keepass file", metavar="FILE")
    parser.add_option("-p", "--pass",
                      dest="password", default=env_password,
                      help="password to open keepass file. The password can also be given through the KEEPASS_PASSWORD environment variable")

    parser.add_option("-e", "--entry",
                      dest="entryPath",
                      help="field to retrieve (for example Passwordlist/MyGroup/MyEntry")
    parser.add_option("-n", "--names",
                      dest="fieldNames", default="Password",
                      help="Comma seperated list of fields to retrieve (default: Password, for show-entry only the first one is used). Can also be '*' for all entries")

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("You must give exactly one command (show-entry, list-entries, to-json or to-keyvalue)");
    
    if args[0] == "show-entry":
        with libkeepass.open(options.filename, password=options.password) as kdb:
            print(getEntry(kdb.obj_root,options.entryPath,options.fieldNames.split(",")[0]));
    if args[0] == "list-entries":
        with libkeepass.open(options.filename, password=options.password) as kdb:
            print(listEntriesInGroup(kdb.obj_root, options.entryPath));
    if args[0] == "to-json":
        if options.entryPath == None:
            parser.error("You must give the entryPath parameter with to-json");
        with libkeepass.open(options.filename, password=options.password) as kdb:
            print(entryTreeToObject(kdb.obj_root, options.entryPath, options.fieldNames.split(",")))

    if args[0] == "to-keyvalue":
        if options.entryPath == None:
            parser.error("You must give the entryPath parameter with to-keyvalue");
        with libkeepass.open(options.filename, password=options.password) as kdb:
            print("\n".join(entryTreeToKeyValue(kdb.obj_root, options.entryPath, options.fieldNames.split(",")[0])))

if __name__ == "__main__":
  main()
   
