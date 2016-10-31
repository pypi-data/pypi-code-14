#!/usr/bin/env python
#coding:utf-8
"""
  Author:  dog - <yafeile@sohu.com>
  Purpose: 
  Created: 2016年10月31日
"""

from mercurial import commands
from os.path import exists, join,abspath
from os import mkdir
from utils import output, ui, get_repo

__all__ = [
    'create_repository','log','get_summary',
    'remove_repository','commit','get_repository_status',
    'clone_repository','get_track_file','get_repository_tags',
    'pull_repository','get_heads','add_file'
    'update_repository','get_file_annotate'
]

@output
def log(path,*args,**kw):
    """
    >>> log('/path/to',graph=True,limit=2)
    """
    repo = get_repo(ui, path)
    commands.log(ui, repo,*args,**kw)


def create_repository(path):
    path = abspath(join(path,'.hg'))
    commands.init(ui, path)

def remove_repository(path):
    path = abspath(join(path,'.hg'))
    if exists(path):
        from shutil import rmtree
        rmtree(path)

@output
def clone_repository(src,*args,**kw):
    """
    clone a repository
    >>> clone_repository('/home/dog/demo','/path/to')
    """
    commands.clone(ui, src, *args,**kw)

@output
def pull_repository(path,**kw):
    repo = get_repo(ui, '.')
    commands.pull(ui, repo,path,**kw)
    
@output
def update_repository(path='.'):
    repo = get_repo(ui, path)
    commands.update(ui, repo)

@output
def commit(path='.',*args,**kw):
    """
    >>> commit(message='提交')
    """
    repo = get_repo(ui, path)
    commands.commit(ui, repo)

@output
def get_track_file(path='.'):
    repo = get_repo(ui, path)
    commands.files(ui, repo)


@output
def get_heads(path='.'):
    repo = get_repo(ui, path)
    commands.heads(ui, repo)

@output
def get_file_annotate(filename,path='.'):
    """
    >>> get_file_annotate('utils.py')
    """
    repo = get_repo(ui, path)
    commands.annotate(ui, repo, filename)

@output
def get_summary(path='.'):
    repo = get_repo(ui, path)
    commands.summary(ui, repo)

@output
def get_repository_status(path='.'):
    repo = get_repo(ui, path)
    commands.status(ui, repo)

@output
def get_repository_tags(path='.',*args,**kw):
    repo = get_repo(ui, path)
    commands.tags(ui, repo,*args,**kw)

@output
def add_file(path='.',*args,**kw):
    """
    >>> add_file(subrepos=True)
    """
    repo = get_repo(ui, path)
    commands.add(ui, repo, *args,**kw)