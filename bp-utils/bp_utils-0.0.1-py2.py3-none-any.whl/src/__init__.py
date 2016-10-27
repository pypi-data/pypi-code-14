import os
import logging
import argparse
import requests

UPLOAD_URL = 'https://api.bitbucket.org/2.0/repositories/%s/%s/downloads'
DOWNLOAD_URL = 'https://api.bitbucket.org/2.0/repositories/%s/%s/downloads/%s'


def main():
    """Entry point for the application script"""
    logging.basicConfig(**{
        'level': logging.INFO,
        'format': '[%(levelname)-5s] %(message)s',
    })

    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest='command')

    upload_cmd = commands.add_parser('upload', **{
        'help': 'upload a file to bitbucket repo downloads',
    })
    upload_cmd.add_argument('filename', **{
        'help': 'file to upload',
        'type': str,
    })
    upload_cmd.add_argument('-n', '---name', **{
        'type': str,
        'help': 'upload the file with the given name'
    })
    upload_cmd.add_argument('-u', '--username', **{
        'type': str,
        'help': 'username to use in basic auth',
        'default': os.getenv('BITBUCKET_USERNAME'),
    })
    upload_cmd.add_argument('-p', '--password', **{
        'type': str,
        'help': 'password to use in basic auth',
        'default': os.getenv('BITBUCKET_PASSWORD'),
    })
    upload_cmd.add_argument('-s', '--slug', **{
        'type': str,
        'help': 'the git repository slug. eg bitbucket.org/{owner}/{slug}',
        'default': os.getenv('BITBUCKET_REPO_SLUG'),
    })
    upload_cmd.add_argument('-o', '--owner', **{
        'type': str,
        'help': 'the git repository owner. eg bitbucket.org/{owner}/{slug}',
        'default': os.getenv('BITBUCKET_REPO_OWNER'),
    })

    download_cmd = commands.add_parser('download', **{
        'help': 'download a file from bitbucket repo downloads',
    })
    download_cmd.add_argument('filename', **{
        'help': 'file to download',
        'type': str,
    })
    download_cmd.add_argument('-u', '--username', **{
        'type': str,
        'help': 'username to use in basic auth',
        'default': os.getenv('BITBUCKET_USERNAME'),
    })
    download_cmd.add_argument('-p', '--password', **{
        'type': str,
        'help': 'password to use in basic auth',
        'default': os.getenv('BITBUCKET_PASSWORD'),
    })
    download_cmd.add_argument('-s', '--slug', **{
        'type': str,
        'help': 'the git repository slug. eg bitbucket.org/{owner}/{slug}',
        'default': os.getenv('BITBUCKET_REPO_SLUG'),
    })
    download_cmd.add_argument('-o', '--owner', **{
        'type': str,
        'help': 'the git repository owner. eg bitbucket.org/{owner}/{slug}',
        'default': os.getenv('BITBUCKET_REPO_OWNER'),
    })

    args = parser.parse_args()
    if args.command == 'upload':
        upload(args.filename, args.username, args.password, args.owner, args.slug, args.name)
    elif args.command == 'download':
        download(args.filename, args.username, args.password, args.owner, args.slug)
    else:
        logging.error("unknown command: '%s'", args.command)


def upload(filename, username, password, owner, slug, rename):
    if owner is None:
        logging.error("no repository owner was set")
        exit(1)
    elif slug is None:
        logging.error("no repository slug was set")
        exit(1)
    elif not os.path.exists(filename):
        logging.error("failed to find file: %s", filename)
        exit(1)

    auth = None
    if username is None:
        logging.warning("no username set")
    elif password is None:
        logging.warning("no password set")
    else:
        auth = (username, password)

    url = UPLOAD_URL % (owner, slug)
    path = os.path.abspath(filename)
    name = rename or os.path.basename(filename)
    logging.info("uploading '%s' to %s as %s", path, url, name)

    resp = requests.post(url, auth=auth, files=[
        ('files',  (name, open(path, 'rb'))),
    ])

    if resp.status_code != 201:
        logging.error("failed to upload: status code %d", resp.status_code)
        print(resp.headers)
        print(resp.text)
        exit(1)

    logging.info("upload successful")


def download(filename, username, password, owner, slug):
    if owner is None:
        logging.error("no repository owner was set")
        exit(1)
    elif slug is None:
        logging.error("no repository slug was set")
        exit(1)
    elif os.path.exists(filename):
        logging.error("file already exists: %s", filename)
        exit(1)

    auth = None
    if username is None:
        logging.warning("no username set")
    elif password is None:
        logging.warning("no password set")
    else:
        auth = (username, password)

    url = DOWNLOAD_URL % (owner, slug, filename)
    logging.info("downloading %s", url)

    resp = requests.get(url, auth=auth)

    if resp.status_code != 200:
        logging.error("failed to upload: status code %d", resp.status_code)
        exit(1)

    with open(filename, 'wb') as f:
        f.write(resp.content)

    logging.info("download successful")
