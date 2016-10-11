import argparse
import os
import re
import crirm.util
import crirm.criteria as criteria
import sys

options = None


def main():
    global options
    options = parse_options(sys.argv[1:])

    if options.recursive:
        for root, dirs, files in os.walk(options.path, topdown=True):
            clean_directory(root, dirs, files)
    else:
        root = os.path.abspath(options.path)
        clean_directory(root,
                        list(filter(lambda x: os.path.isdir(os.path.join(root, x)), os.listdir(root))),
                        list(filter(lambda x: os.path.isfile(os.path.join(root, x)), os.listdir(root))))


def clean_directory(root, dirs, files):
    global options
    if options.verbose >= 3:
        print("root: {0}\n  dirs: {1}\n  files: {2}\n".format(root, dirs, files))
    if len(files) > 0:
        for file in files:
            fname = os.path.join(root, file)

            if re.match(options.name, fname) is None:
                if options.verbose > 0:
                    print("no match: {0}".format(fname))
                continue

            if check_criteria(fname):
                if options.verbose > 0:
                    print("match: {}\n".format(fname))
                if options.dry_run:
                    print("{0}\n".format(fname))
                else:
                    delete(fname)
            elif options.verbose > 0:
                print("no match: {}\n".format(fname))
    else:
        if len(dirs) < 1 and len(files) < 1 and options.delete_empty:
            if options.dry_run:
                print("{0}\n".format(root))
            else:
                delete(root)


def parse_options(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="root path where the criteria will be applied")
    parser.add_argument("-r", "--recursive", help="apply criteria in subdirectories", action="store_true")
    parser.add_argument("-f", "--force", help="do not ask for confirmation on delete", action="store_true")
    parser.add_argument("-a", "--age", help="files older than the given number of days", default=-1, type=int)
    parser.add_argument("-n", "--name", help="regular expression for the filename to match", default=".*")
    parser.add_argument("-D", "--dry-run", help="print found files but do not delete", action="store_true")
    parser.add_argument("-e", "--delete-empty", help="delete empty directories", action="store_true")
    parser.add_argument("-v", "--verbose", help="verbose output", action="count", default=0)
    return parser.parse_args(args)


def check_criteria(fname):
    global options
    return criteria.match(fname, age=options.age)


def delete(fname):
    if not options.force:
        if not crirm.util.query_yes_no("{0} - Delete?".format(fname), default="no"):
            return

    if os.path.isfile(fname):
        os.remove(fname)
    elif os.path.isdir(fname):
        os.removedirs(fname)

    print("deleted: {}\n".format(fname))

if __name__ == '__main__':
    main()