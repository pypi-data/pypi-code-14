#!/usr/bin/env python
# coding: utf8

import os
import sqlite3
import psutil

USAGE_DIR = os.path.join(os.path.expanduser("~"), '.usage')

if not os.path.exists(USAGE_DIR):
    os.mkdir(USAGE_DIR)
elif not os.path.isdir(USAGE_DIR):
    os.remove(USAGE_DIR)
    os.mkdir(USAGE_DIR)


DB = sqlite3.connect(os.path.join(USAGE_DIR, 'usage.db'))


def init_db():
    tables = DB.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    if 'usage' not in str(tables):
        DB.execute('''
        create table usage(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name text not null,
            identifier text not null,
            app_path text not null,
            created int not null,
            focused int not null
        )
        ''')
        DB.commit()


def singleton(cls):
    INSTANCES = {}

    def _singleton(*args, **kwargs):
        if cls not in INSTANCES:
            INSTANCES[cls] = cls(*args, **kwargs)
        return INSTANCES[cls]

    return _singleton


@singleton
class Usage(object):
    init_db()

    @property
    def pid(self):
        if hasattr(self, '_pid'):
            return self._pid

        path = os.path.join(USAGE_DIR, 'pid')
        if not os.path.exists(path):
            return None

        with open(path) as fp:
            try:
                pid = int(fp.read())
            except:
                return None

        if not psutil.pid_exists(pid):
            return None

        print '[log] model :', psutil.Process(pid).name()
        print '[log] model :', psutil.Process(pid).cmdline()

        self._pid = pid
        return self._pid

    def log_pid(self):
        path = os.path.join(USAGE_DIR, 'pid')
        pid = os.getpid()
        self._pid = pid

        with open(path, 'w') as fp:
            fp.write(str(pid))

        return pid


class ActiveApp(object):

    def __init__(self, name, identifier, app_path):
        self.name = name
        self.identifier = identifier
        self.app_path = app_path

    def __str__(self):
        return "ActiveApp(name='{name}', identifier='{identifier}', " \
               "app_path='{app_path}')".format(**self.__dict__)

    @classmethod
    def get_current(cls):
        from AppKit import NSWorkspace

        active_app = NSWorkspace.sharedWorkspace().activeApplication()
        return cls(active_app['NSApplicationName'],
                   active_app['NSApplicationBundleIdentifier'],
                   active_app['NSApplicationPath'])
