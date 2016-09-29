# -*- coding: utf8 -*-
#
#  Copyright (c) 2014, 2016 unfoldingWord
#  http://creativecommons.org/licenses/MIT/
#  See LICENSE file for details.
#
#  Contributors:
#  Jesse Griffin <jesse@distantshores.org>
#  Phil Hopper <phillip_hopper@wycliffeassociates.org>
#
#  Requires PyGithub for Github commands.

from __future__ import print_function, unicode_literals
import shlex
from subprocess import *
# noinspection PyPackageRequirements
from github import Github, GithubException
import os

# noinspection PyPep8Naming
from general_tools.print_utils import print_warning


# noinspection PyPep8Naming
def getGithubOrg(org_name, user):
    return user.get_organization(org_name)


# noinspection PyPep8Naming
def githubLogin(user, pw):
    return Github(user, pw)


# noinspection PyPep8Naming
def githubCreate(d, r_name, r_desc, r_url, org):
    """
    Creates a Github repo, unless it already exists.
    Accepts a local path, repo name, description, org name.
    """
    try:
        org.get_repo(r_name)
        return
    except GithubException:
        try:
            repo = org.create_repo(r_name, r_desc, r_url,
                                   has_issues=False,
                                   has_wiki=False,
                                   auto_init=False,
                                   )
        except GithubException as ghe:
            print(ghe)
            return
    os.chdir(d)
    out, ret = runCommand('git remote add origin {0}'.format(repo.ssh_url))
    if ret > 0:
        print_warning('Failed to add Github remote to repo in: {0}'.format(d))


# noinspection PyPep8Naming
def gitCreate(d):
    """
    Creates local git repo, unless it already exists.
    Accepts a local path as the git repo.
    """
    if os.path.exists(os.path.join(d, '.git')):
        return
    os.chdir(d)
    out, ret = runCommand('git init .')
    if ret > 0:
        print_warning('Failed to create a git repo in: {0}'.format(d))
        sys.exit(1)


# noinspection PyPep8Naming
def gitCommit(d, msg, files='*'):
    """
    Adds all files in d and commits with message m.
    """
    os.chdir(d)
    out, ret = runCommand('git add {0}'.format(files))
    out1, ret1 = runCommand('''git commit -am "{0}" '''.format(msg))
    if ret > 0 or ret1 > 0:
        print('Nothing to commit, or failed commit to repo in: {0}'.format(d))
        print(out1)


# noinspection PyPep8Naming
def gitPush(d):
    """
    Pushes local repository to origin master.
    """
    os.chdir(d)
    out, ret = runCommand('git push origin master')
    if ret > 0:
        print(out)
        print('Failed to push repo to origin master in: {0}'.format(d))


# noinspection PyPep8Naming
def gitPull(d):
    """
    Pulls from origin master to local repository.
    """
    os.chdir(d)
    out, ret = runCommand('git pull --no-edit origin master')
    if ret > 0:
        print(out)
        print('Failed to pull from origin master in: {0}'.format(d))


# noinspection PyPep8Naming
def gitClone(d, remote):
    """
    Clones a repo from remote into d.  Directory d should not exist or be
    empty.
    """
    out, ret = runCommand('git clone {0} {1}'.format(remote, d))
    if ret > 0:
        print(out)
        print('Failed to clone from {0} to {1}'.format(remote, d))


# noinspection PyPep8Naming
def createHallHook(repo, room_id):
    """
    Creates a hall hook for the given repository to the given room.
    """
    config = {u'room_token': room_id}
    repo.create_hook(u'hall', config)


# noinspection PyPep8Naming
def runCommand(c):
    """
    Runs a command in a shell.  Returns output and return code of command.
    """
    command = shlex.split(c)
    com = Popen(command, shell=False, stdout=PIPE, stderr=PIPE)
    com_out = ''.join(com.communicate()).strip()
    return com_out, com.returncode


if __name__ == '__main__':
    pass
