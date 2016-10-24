from __future__ import absolute_import, division, print_function, unicode_literals

import boto3
import json
import os
import sys

TIROS_VERSION = '1.0'

CONTENT_TYPE = 'application/json'
METHOD = 'POST'

VERBOSE = False


def vprint(x):
    if VERBOSE:
        print(str(x))


def eprint(s):
    print(s)
    sys.exit(1)


def file_contents(path):
    if os.path.exists(path):
        with open(path) as fd:
            return fd.read()
    else:
        # Don't use FileNotFoundError, which doesn't exist in Python2
        raise IOError('File not found: ' + path)


def quote(s):
    return '"' + s + '"'


def json_encoder(obj):
    """JSON serializer for objects not serializable by default json code"""
    if type(obj) == bytes:
        return obj.decode('utf-8')
    raise TypeError("Type not serializable")


def pretty(x):
    return json.dumps(x, indent=2, sort_keys=True, default=json_encoder)


def canonical(x):
    return json.dumps(x, sort_keys=True, default=json_encoder)


def assume_role_session(session, role_arn, region=None):
    """
    :param session: An existing boto Session
    :param role_arn: An IAM role to assume
    :param region: The region for the new Session, defaults to region of
    existing session.
    :return: A Session with the assumed role.
    """
    sts = session.client('sts')
    creds = sts.assume_role(
        RoleArn=role_arn,
        RoleSessionName='tiros',  # arbitrary
    )
    if 'Credentials' not in creds:
        eprint("Couldn't assume role: " + role_arn)
    cs = creds['Credentials']
    token = cs['SessionToken'] if 'SessionToken' in cs else None
    if not region:
        region = session.region_name
    return boto3.Session(
        aws_access_key_id=cs['AccessKeyId'],
        aws_secret_access_key=cs['SecretAccessKey'],
        aws_session_token=token,
        region_name=region)


def change_session_region(session, region):
    if region == session.region_name:
        return session
    creds = session.get_credentials()
    return boto3.Session(aws_access_key_id=creds.access_key,
                         aws_secret_access_key=creds.secret_key,
                         aws_session_token=creds.token,
                         region_name=region)


def account(session):
    return session.client('sts').get_caller_identity().get('Account')


# Fix input in python2
try:
    # noinspection PyShadowingBuiltins
    safe_input = raw_input
except NameError:
    safe_input = input
