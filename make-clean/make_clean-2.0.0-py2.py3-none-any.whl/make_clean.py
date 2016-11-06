# -*- coding: utf-8 -*-
import os
import argparse
import shutil


VERSION = (2, 0, 0)
__version__ = '{0:d}.{1:d}.{2:d}'.format(*VERSION)


def make_clean(target_dirs, ignore_fname=None, ignores=None):
    '''clean target_dir except ignores relatively

    cleanup target directory except:

    - file: is in ignores
    - directory: is in ignores

    Files and directories are referenced relatively.

    :param str target_dir: target directory to cleanup
    :param list ignores: not rm files or directories
    '''
    target_dirs = [os.path.abspath(x) for x in target_dirs]
    ignore_dirs, ignore_files = parse_ignores(ignore_fname, ignores)
    rm_files(target_dirs, ignore_dirs, ignore_files)
    rm_dirs(target_dirs, ignore_dirs)


def parse_ignores(ignore_fname, ignore_patterns):
    ignores = []
    if ignore_fname:
        if os.path.isfile(ignore_fname):
            with open(ignore_fname) as fp:
                for line in fp:
                    line = line.strip()
                    if not line.startswith('#'):
                        # lstrip / and replace / to os.sep
                        line = line.lstrip('/').replace('/', os.sep)
                        ignores.append(line)

    if ignore_patterns:
        # lstrip /
        ignores.extend([x.lstrip('/') for x in ignore_patterns if x])

    ignore_dirs = tuple(os.path.abspath(x) for x in ignores
                        if x and x.endswith(os.sep) and os.path.isdir(x))
    ignore_files = {os.path.abspath(x) for x in ignores
                    if x and os.path.isfile(x)}
    return ignore_dirs, ignore_files


def rm_files(target_dirs, ignore_dirs, ignore_files):
    '''Remove files.'''
    for dir_path in target_dirs:
        for root, _, files in os.walk(dir_path):
            for f in files:
                fullpath = os.path.join(root, f)
                if (fullpath.startswith(ignore_dirs) or
                        fullpath in ignore_files):
                    continue
                os.remove(fullpath)


def rm_dirs(target_dirs, ignore_dirs):
    '''Remove empty directories.'''
    ignore_dir_set = set(ignore_dirs)

    for dir_path in target_dirs:
        for root, _, _ in os.walk(dir_path):
            if (not is_empty_dir(root) or
                    root in ignore_dir_set or
                    root in target_dirs):
                continue
            shutil.rmtree(root)


def is_empty_dir(target_dir):
    '''return is empty directory or not

    :param str target_dir: target dir
    '''
    for root, _, files in os.walk(target_dir):
        for f in files:
            if os.path.isfile(os.path.join(root, f)):
                return False
    return True


def main():
    parser = argparse.ArgumentParser(
        description=u'clean target dir without ignores')
    parser.add_argument(
        'target_dir',
        metavar='TARGET_DIR',
        nargs='+',
        help=u'dir to remove recursively ')
    parser.add_argument(
        '--clean-ignore',
        metavar='CLEAN_IGNORE',
        help=u'dir/file file to ignore from remove',
        default='.cleanignore',
        )
    parser.add_argument(
        '-i', '--ignores',
        metavar='IGNORE',
        help=u'dir/file to ignore from remove',
        nargs='*',
        default=[],
        )
    parser.set_defaults(
        func=lambda args:
            make_clean(
                args.target_dir,
                args.clean_ignore,
                args.ignores))

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
