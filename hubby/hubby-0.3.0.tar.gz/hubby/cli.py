from . import Hub, get_auth_token, read_token
from . import git_wrapper as git
from ._version import __version__

import argcomplete

import argparse
import os
import subprocess
import sys
import tempfile
import textwrap


def list_assignees():
    token, session = get_auth_token()
    hub = Hub(token, session=session)
    for assignee in hub.get_assignees():
        print(assignee)


def create_or_update_pull_request():
    args = get_pull_request_args()
    token, session = get_auth_token()
    hub = Hub(token, session=session)
    pr_url = hub.create_or_update_pull_request(title=args.title, assignees=args.assignees,
        body=args.body)
    print(pr_url)


def get_pull_request_args():
    parser = argparse.ArgumentParser(prog='hubby')
    parser.add_argument('-t', '--title', help='Title of the pull request. If not given an editor '
        'will be opened where the title and body can be entered')
    parser.add_argument('-a', '--assignees', help='A comma-separated list of people who should be '
        'assigned to this pull request').completer = autocomplete_assignees
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    argcomplete.autocomplete(parser)

    args = parser.parse_args()

    args.body = ''

    if not args.title:
        args.title, args.body = get_title_and_body()
        if not args.title:
            sys.stderr.write('Needs at least a title, aborting\n')
            sys.exit(1)

    if args.assignees:
        args.assignees = args.assignees.split(',')

    return args


def autocomplete_assignees(prefix, **kwargs):
    token = read_token()
    if not token:
        argcomplete.warn('Not logged in with hubby yet, thus not completing')
        return []

    hub = Hub(token)
    return (a for a in hub.get_assignees() if a.startswith(prefix))


def get_title_and_body():
    commits_ahead = git.get_commits_ahead_of_master()
    if len(commits_ahead) == 1:
        commit_msg = git.get_commit_message(commits_ahead[0])
    else:
        commit_msg = get_text_from_editor()

    commit_lines = commit_msg.split('\n')

    title = commit_lines[0]
    body = '\n'.join(commit_lines[1:]).strip()
    return title, body


def get_text_from_editor():
    commit_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w')
    commit_file.write(textwrap.dedent('''\


    ### INFO
    # Describe the pull request. The first line of this file will be the
    # title, while the rest will be the body. Anything after the ### INFO
    # marker will be ignored.
    '''))
    commit_file.close()

    editor = os.environ.get('EDITOR', 'nano')
    cmd = [editor, commit_file.name]
    subprocess.check_call(cmd)

    with open(commit_file.name) as fh:
        text = fh.read()

    actual_lines = []
    for line in text.split('\n'):
        if line.startswith('### INFO'):
            break
        actual_lines.append(line)

    actual_text = '\n'.join(actual_lines)

    os.remove(commit_file.name)

    return actual_text
