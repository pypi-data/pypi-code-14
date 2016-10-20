from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import boto3
import json
import sys

import tiros
import tiros.make_config_rule as make_config_rule
import tiros.make_lambda as make_lambda
import tiros.server as server
import tiros.util as util

from tiros.util import eprint, pretty, vprint

# Fix input in python2
try:
    # noinspection PyShadowingBuiltins
    input = raw_input
except NameError:
    pass


def format_response(response, json_errors):
    try:
        j = json.loads(response.text)
    # The exception thrown on json parse failure in python3 is
    # json.decoder.JSONDecodeError, which does not exist in python2.
    # Fortunately, what python2 throws in that case is ValueError,
    # which is a superclass of json.decoder.JSONDecodeError.
    except ValueError:
        j = {'error': response.text}
    if 'error' in j and not json_errors:
        return j['error']['message']
    else:
        return pretty(j)


def snapshot_session(name):
    if '/' not in name:
        session = boto3.Session(profile_name=name)
    else:
        [profile, region] = name.split('/')
        session = boto3.Session(profile_name=profile, region_name=region)
    return session


def autodetect_raw_snapshot(s):
    # For Palisade snapshots, the raw snapshot holds the actual snapshot
    # in the db field
    if 'db' in s:
        return s.get('db')
    else:
        return s


parser = argparse.ArgumentParser(
    description='Tiros, version ' + util.TIROS_VERSION)

general_group = argparse.ArgumentParser(add_help=False)

general_group.add_argument(
    '--verbose',
    '-v',
    action='store_true',
    help='Be chatty'
)

general_group.add_argument(
    '--json',
    action='store_true',
    help='Force json output, even for errors'
)

server_group = argparse.ArgumentParser(add_help=False)

server_group.add_argument(
    '--dev',
    action='store_true',
    help='Use the dev server'
)

server_group.add_argument(
    '--host',
    help='''
    Tiros host.  If the port is nonstandard, include it here,
    e.g. http://localhost:9000
    '''
)

server_group.add_argument(
    '--no-ssl',
    action='store_true',
    help="Don't use SSL"
)

snapshot_group = argparse.ArgumentParser(add_help=False)

snapshot_group.add_argument(
    '--signing-profile',
    '-p',
    default=None,
    help='An AWS profile name used to sign the request.'
)

snapshot_group.add_argument(
    '--snapshot-profile',
    '-n',
    action='append',
    help="""
    An AWS profile name or profile/region pair.
    (e.g. dev, dev/us-east-1, prod/us-west-2).
    Multiple profiles are supported.  If no profile is
    provided the default is used. If no region
    is specified for a profile, the default region for the
    profile is used.
    """
)

snapshot_group.add_argument(
    '--raw-snapshot-file',
    '-r',
    default=[],
    action='append',
    help='File containing the raw JSON snapshot'
)

snapshot_group.add_argument(
    '--snapshot-file',
    '-s',
    default=[],
    action='append',
    help='File containing the raw JSON snapshot'
)


subparsers = parser.add_subparsers(title='subcommands', dest='cmd')


'''Allow'''


def allow(args):
    if args.profile:
        session = boto3.Session(profile_name=args.profile)
    else:
        session = boto3.Session()
    if args.role_arn:
        session = util.assume_role_session(session, args.role_arn)
    account = session.client('sts').get_caller_identity().get('Account')
    print('This will allow the Tiros service to run Describe* calls in account: ' + account)
    if input('Proceed? [y/n] ') != 'y':
        sys.exit(1)
    tiros.allow(session)

allow_parser = subparsers.add_parser(
    'allow',
    parents=[general_group]
)

allow_parser.set_defaults(func=allow)

allow_parser.add_argument(
    '--profile',
    '-p',
    default=None,
    help='The profile with permission to add an IAM role to the account'
)

allow_parser.add_argument(
    '--role-arn',
    '-r',
    help='An IAM role arn to assume before modifying the role'
)


'''Config'''


def config(args):
    session = boto3.Session(profile_name=args.profile)
    make_config_rule.make_config_rule(session, args.params_file)


config_parser = subparsers.add_parser(
    'make-config-rule',
    parents=[general_group]
)

config_parser.set_defaults(func=config)

config_parser.add_argument(
    '--profile',
    '-p',
    default=None,
    help='The profile with permission to add an IAM role to the account'
)

config_parser.add_argument(
    '--params-file',
    required=True,
    help='The s3 path to the parameters for the config rule.'
)


'''Fetch'''


def fetch(args):
    profile = args.profile
    region = args.region
    role = args.role
    session = boto3.Session(profile_name=profile, region_name=region)
    if role:
        session = util.assume_role_session(session, role)
    print(util.pretty(tiros.fetch(session)))
    sys.exit(0)


fetch_parser = subparsers.add_parser(
    'fetch',
    parents=[general_group]
)

fetch_parser.set_defaults(func=fetch)

fetch_parser.add_argument(
    '--profile',
    '-p',
    help='An AWS profile name'
)

fetch_parser.add_argument(
    '--region',
    '-r',
    help="""
    Snapshot region. If no region is specified for a profile,
    the default region for the profile is used.
    """
)

fetch_parser.add_argument(
    '--role',
    help='An IAM role arn to assume before fetching'
)


'''Lambda'''


def mk_lambda(args):
    session = boto3.Session(profile_name=args.profile)
    make_lambda.make_lambda(session, args.role_arn)

lambda_parser = subparsers.add_parser(
    'make-lambda',
    parents=[general_group]
)

lambda_parser.set_defaults(func=mk_lambda)

lambda_parser.add_argument(
    '--profile',
    '-p',
    help='An AWS profile name'
)

lambda_parser.add_argument(
    '--role-arn',
    '-r',
    required=True,
    help='The IAM role to associate with the Lambda function'
)


'''Query'''


query_parser = subparsers.add_parser(
    'query',
    parents=[general_group, server_group, snapshot_group]
)


def query(args):
    signing_session = boto3.Session(profile_name=args.signing_profile)
    ssl = not args.no_ssl
    host = args.host or (server.DEV_HOST if args.dev else server.PROD_HOST)
    snapshot_sessions = [snapshot_session(p) for p in (args.snapshot_profile or [])]
    snapshots = [json.loads(util.file_contents(f))
                 for f in (args.snapshot_file or [])]
    raw_snapshots = [autodetect_raw_snapshot(json.loads(util.file_contents(f)))
                     for f in (args.raw_snapshot_file or [])]
    if not snapshot_sessions and not snapshots and not raw_snapshots:
        snapshot_sessions = [signing_session]
    if args.inline and args.queries_file:
        eprint("Can't specify both --inline and --queries_file")
    queries = None
    if args.inline:
        queries = args.inline
    elif args.queries_file:
        queries = util.file_contents(args.queries_file)
    else:
        eprint('You must specify --inline or --queries_file')
    if args.relations_file:
        user_relations = util.file_contents(args.relations_file)
    else:
        user_relations = None
    response = tiros.query(
        signing_session=signing_session,
        queries=queries,
        snapshot_sessions=snapshot_sessions,
        snapshots=snapshots,
        raw_snapshots=raw_snapshots,
        backend=args.backend,
        transforms=args.transform,
        user_relations=user_relations,
        ssl=ssl,
        host=host)
    vprint('Status code: ' + str(response.status_code))
    print(format_response(response, args.json))
    if response.status_code != 200:
        sys.exit(1)
    sys.exit(0)

query_parser.set_defaults(func=query)

query_parser.add_argument(
    '--backend',
    '-b',
    default='z3',
    help='Datalog backend'
)

query_parser.add_argument(
    '--transform',
    '-x',
    action='append',
    default=[],
    help='Apply source transforms. Available: magic-sets'
)

query_parser.add_argument(
    '--relations-file',
    '-l',
    default=None,
    help='User relations file'
)

query_parser.add_argument(
    '--queries-file',
    '-f',
    default=None,
    help='File containing the JSON Tiros queries'
)

query_parser.add_argument(
    '--inline',
    '-i',
    help='Inline query'
)


'''Snapshot'''


def snapshot(args):
    signing_session = boto3.Session(profile_name=args.signing_profile)
    ssl = not args.no_ssl
    host = args.host or (server.DEV_HOST if args.dev else server.PROD_HOST)
    snapshot_sessions = [snapshot_session(p) for p in (args.snapshot_profile or [])]
    snapshots = [json.loads(util.file_contents(f))
                 for f in (args.snapshot_file or [])]
    raw_snapshots = [autodetect_raw_snapshot(json.loads(util.file_contents(f)))
                     for f in (args.raw_snapshot_file or [])]
    if not snapshot_sessions and not snapshots and not raw_snapshots:
        snapshot_sessions = [signing_session]
    response = tiros.snapshot(
        signing_session=signing_session,
        snapshot_sessions=snapshot_sessions,
        snapshots=snapshots,
        raw_snapshots=raw_snapshots,
        ssl=ssl,
        host=host)
    vprint('Status code: ' + str(response.status_code))
    print(format_response(response, args.json))
    if response.status_code != 200:
        sys.exit(1)
    sys.exit(0)

snapshot_parser = subparsers.add_parser(
    'snapshot',
    parents=[general_group, server_group, snapshot_group]
)


snapshot_parser.set_defaults(func=snapshot)


'''Main'''


def main():
    args = parser.parse_args()
    if args.verbose:
        util.VERBOSE = True
    if not args.cmd:
        print("No subcommand specified")
        parser.print_help()
        sys.exit(1)
    args.func(args)


if __name__ == '__main__':
    main()
