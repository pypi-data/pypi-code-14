from . import Hub, get_auth_token

import argparse

def list_assignees():
    token, session = get_auth_token()
    hub = Hub(token, session=session)
    for assignee in hub.get_assignees():
        print(assignee)


def create_or_update_pull_request():
    token, session = get_auth_token()
    args = get_pull_request_args()
    hub = Hub(token, session=session)
    pr_url = hub.create_or_update_pull_request(title=args.title, assignees=args.assignees)
    print(pr_url)


def get_pull_request_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--title', help='Title of the pull request. If not given an editor '
        'will be opened where the title and body can be entered')
    parser.add_argument('-a', '--assignees', help='A comma-separated list of people who should be '
        'assigned to this pull request')

    args = parser.parse_args()

    if args.assignees:
        args.assignees = args.assignees.split(',')

    return args
