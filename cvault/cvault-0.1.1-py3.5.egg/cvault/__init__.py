#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Credential Vault (cvault)

Usage:
  cvault init <vault_name>
  cvault save <account> <password> <description>
  cvault remove <entry_id>
  cvault list [-v]
  cvault show <entry_id>

Options:
  -h --help             show this help message and exit
  --version             show version and exit
"""
from docopt import docopt
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase

import datetime
import os

db = SqliteExtDatabase('vault.db')
SIMPLE_TMPL = "{e.acct}|{e.passwd}|{e.desc}"
DETAIL_TMPL = "{e.id}: {e.timestamp}|{e.acct}|{e.passwd}|{e.desc}"

class Entry(Model):
    acct = CharField()
    passwd = CharField()
    desc = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


def init_vault(vault_name):
    db.connect()
    try:
        db.create_tables([Entry])
    except OperationalError:
        print("Vault \"{}\" is already initialized.".format(vault_name))

def save_entry(acct, passwd, desc):
    entry = Entry(acct=acct, passwd=passwd, desc=desc)
    try:
        entry.save()
    except OperationalError:
        print("No vault can be used.")

def remove_entry(entry_id):
    try:
        entry = Entry.get(Entry.id == entry_id)
    except Entry.DoesNotExist:
        print('The given entry ID does not exist.')
    else:
        entry.delete_instance()

def list_entries(verbose=False):
    if verbose:
        template = SIMPLE_TMPL
    else:
        template = DETAIL_TMPL
    for entry in Entry.select():
        print(template.format(e=entry))

def show_entry(entry_id):
    try:
        entry = Entry.get(Entry.id == entry_id)
    except Entry.DoesNotExist:
        print('The given entry ID does not exist.')
    else:
        print(DETAIL_TMPL.format(e=entry))

def cvault(vault_name, acct, passwd, desc, entry_id, init=False, save=False,
        remove=False, dump=True, show=False, verbose=False):
    if init:
        init_vault(vault_name)
    elif save:
        save_entry(acct, passwd, desc)
    elif remove:
        remove_entry(entry_id)
    elif dump:
        list_entries(verbose)
    elif show:
        show_entry(entry_id)
    else:
        list_entries()

def main():
    args = docopt(__doc__, version='cvault 0.1.1')

    kwargs = {
        'init': args['init'],
        'vault_name': args['<vault_name>'],
        'save': args['save'],
        'acct': args['<account>'],
        'passwd': args['<password>'],
        'desc': args['<description>'],
        'remove': args['remove'],
        'entry_id': args['<entry_id>'],
        'dump': args['list'],
        'show': args['show'],
        'verbose': args['-v'],
    }

    cvault(**kwargs)
