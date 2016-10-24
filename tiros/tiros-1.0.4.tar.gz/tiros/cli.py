from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import boto3
import json
import sys

import tiros.iam as iam
import tiros.fetch_ as fetch_
import tiros.lam as lam
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


general_args = argparse.ArgumentParser(add_help=False)

general_args.add_argument(
    '--profile',
    '-p',
    default=None,
    help='The AWS profile to use for signing requests'
)

general_args.add_argument(
    '--verbose',
    '-v',
    action='store_true',
    help='Be chatty'
)

server_args = argparse.ArgumentParser(add_help=False)

server_args.add_argument(
    '--dev',
    action='store_true',
    help='Use the dev server'
)

server_args.add_argument(
    '--host',
    help='''
    Tiros host.  If the port is nonstandard, include it here,
    e.g. http://localhost:9000
    '''
)

server_args.add_argument(
    '--json',
    action='store_true',
    help='Force json output, even for errors'
)

server_args.add_argument(
    '--no-ssl',
    action='store_true',
    help="Don't use SSL"
)

server_args.add_argument(
    '--raw-snapshot-file',
    '-r',
    default=[],
    action='append',
    help='File containing the raw JSON snapshot'
)

server_args.add_argument(
    '--snapshot-file',
    '-s',
    default=[],
    action='append',
    help='File containing the raw JSON snapshot'
)

server_args.add_argument(
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

parser = argparse.ArgumentParser(
    description='Tiros, version ' + util.TIROS_VERSION)

subparsers = parser.add_subparsers(title='subcommands', dest='cmd')
iam_parser = subparsers.add_parser('iam', help='IAM utilities')
iam_subparsers = iam_parser.add_subparsers(title='subcommands', dest='cmd')
lambda_parser = subparsers.add_parser('lambda', help='Lambda utilities')
lambda_subparsers = lambda_parser.add_subparsers(title='subcommands', dest='cmd')


def main():
    args = parser.parse_args()
    if args.verbose:
        util.VERBOSE = True
    if not args.cmd:
        print("No subcommand specified")
        parser.print_help()
        sys.exit(1)
    args.func(args)


# ---------- iam create-policy ----------


def iam_create_policy(args):
    session = boto3.Session(profile_name=args.profile)
    iam.create_tiros_policy(session)

iam_create_policy_parser = iam_subparsers.add_parser(
    'create-policy',
    parents=[general_args],
    help='Create a policy with enough permissions to run Tiros'
)

iam_create_policy_parser.set_defaults(func=iam_create_policy)


# ---------- iam create-role ----------


def iam_create_role(args):
    session = boto3.Session(profile_name=args.profile)
    iam.create_tiros_role(session)

iam_create_role_parser = iam_subparsers.add_parser(
    'create-role',
    parents=[general_args],
    help='Create a cross-account role to the Tiros service'
)

iam_create_role_parser.set_defaults(func=iam_create_role)


# ---------- iam delete-policy ----------


def iam_delete_policy(args):
    session = boto3.Session(profile_name=args.profile)
    iam.delete_tiros_policy(session)

iam_delete_policy_parser = iam_subparsers.add_parser(
    'delete-policy',
    parents=[general_args],
    help='Remove the Tiros policy'
)

iam_delete_policy_parser.set_defaults(func=iam_delete_policy)


# ---------- iam delete-role ----------


def iam_delete_role(args):
    session = boto3.Session(profile_name=args.profile)
    iam.delete_tiros_role(session)

iam_delete_role_parser = iam_subparsers.add_parser(
    'delete-role',
    parents=[general_args],
    help='Remove the Tiros role'
)

iam_delete_role_parser.set_defaults(func=iam_delete_role)


# ---------- iam show-policy ----------


def iam_show_policy(args):
    print(util.pretty(iam.TIROS_POLICY))

iam_show_policy_parser = iam_subparsers.add_parser(
    'show-tiros-policy',
    parents=[general_args],
    help='Show the IAM policy Tiros requires to make a network snapshot'
)

iam_show_policy_parser.set_defaults(func=iam_show_policy)


# ---------- fetch -----------


def top_fetch(args):
    session = boto3.Session(profile_name=args.profile)
    if args.region:
        session = util.change_session_region(session, args.region)
    print(util.pretty(fetch_.fetch(session)))

fetch_parser = subparsers.add_parser(
    'fetch',
    parents=[general_args],
    help='Fetch a tiros snapshot using local credentials'
)

fetch_parser.set_defaults(func=top_fetch)

fetch_parser.add_argument(
    '--region',
    '-r',
    help="""
    Snapshot region. If no region is specified for a profile,
    the default region for the profile is used.
    """
)


# ---------- lambda create-function ----------


def lambda_create_function(args):
    session = boto3.Session(profile_name=args.profile)
    lam.create_or_update_lambda_function(session)

lambda_create_function_parser = lambda_subparsers.add_parser(
    'create-function',
    parents=[general_args],
    help='Create a Lambda function that calls Tiros and processes the results'
)

lambda_create_function_parser.set_defaults(func=lambda_create_function)


# ---------- lambda create-lambda-role ----------


def lambda_create_role(args):
    session = boto3.Session(profile_name=args.profile)
    iam.create_lambda_role(session,
                           s3_prefix=args.s3_prefix,
                           sns_topic_arn=args.sns_topic_arn)

lambda_create_role_parser = lambda_subparsers.add_parser(
    'create-role',
    parents=[general_args],
    help='Create an IAM role to run Tiros in Lambda'
)

lambda_create_role_parser.set_defaults(func=lambda_create_role)

lambda_create_role_parser.add_argument(
    '--s3-prefix',
    required=True,
    help="""
    Allow the Tiros Lambda role read-write access to the given prefix
    """
)

lambda_create_role_parser.add_argument(
    '--sns-topic-arn',
    help="""
    Allow the Tiros Lambda write to the given SNS topic
    """
)


# ---------- lambda create-rule ----------


def lambda_create_rule(args):
    session = boto3.Session(profile_name=args.profile)
    lam.create_rule(session, args.params_file)

lambda_rule_parser = lambda_subparsers.add_parser(
    'create-rule',
    parents=[general_args],
    help='Create a custom Config rule from the sample Lambda function'
)

lambda_rule_parser.set_defaults(func=lambda_create_rule)

lambda_rule_parser.add_argument(
    '--params-file',
    required=True,
    help='The s3 path to the parameters for the config rule.'
)


# ---------- lambda delete-function ----------


def lambda_delete_function(args):
    session = boto3.Session(profile_name=args.profile)
    lam.delete_lambda(session)

lambda_delete_function_parser = lambda_subparsers.add_parser(
    'delete-function',
    parents=[general_args],
    help='Delete the Lambda function'
)

lambda_delete_function_parser.set_defaults(func=lambda_delete_function)


# ---------- lambda delete-role ----------


def lambda_delete_role(args):
    session = boto3.Session(profile_name=args.profile)
    iam.delete_lambda_role(session)

lambda_delete_role_parser = lambda_subparsers.add_parser(
    'delete-role',
    parents=[general_args],
    help='Remove the Tiros Lambda role'
)

lambda_delete_role_parser.set_defaults(func=lambda_delete_role)


# ---------- lambda delete-rule ----------


def lambda_delete_rule(args):
    session = boto3.Session(profile_name=args.profile)
    lam.delete_rule(session)

lambda_delete_rule_parser = lambda_subparsers.add_parser(
    'delete-rule',
    parents=[general_args],
    help='Delete the Config Rule'
)

lambda_delete_rule_parser.set_defaults(func=lambda_delete_rule)


# ---------- query ----------


query_parser = subparsers.add_parser(
    'query',
    parents=[general_args, server_args],
    help='Query a network using TQL'
)


def query(args):
    session = boto3.Session(profile_name=args.profile)
    ssl = not args.no_ssl
    host = args.host or (server.DEV_HOST if args.dev else server.PROD_HOST)
    snapshot_sessions = [snapshot_session(p) for p in (args.snapshot_profile or [])]
    snapshots = [json.loads(util.file_contents(f))
                 for f in (args.snapshot_file or [])]
    raw_snapshots = [autodetect_raw_snapshot(json.loads(util.file_contents(f)))
                     for f in (args.raw_snapshot_file or [])]
    if not snapshot_sessions and not snapshots and not raw_snapshots:
        snapshot_sessions = [session]
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
    response = server.query(
        signing_session=session,
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
    '--inline',
    '-i',
    help='Inline query'
)

query_parser.add_argument(
    '--queries-file',
    '-f',
    default=None,
    help='File containing the JSON Tiros queries'
)

query_parser.add_argument(
    '--relations-file',
    '-l',
    default=None,
    help='User relations file'
)

query_parser.add_argument(
    '--transform',
    '-x',
    action='append',
    default=[],
    help='Apply source transforms. Available: magic-sets'
)


# ---------- snapshot ----------


def snapshot(args):
    session = boto3.Session(profile_name=args.profile)
    ssl = not args.no_ssl
    host = args.host or (server.DEV_HOST if args.dev else server.PROD_HOST)
    snapshot_sessions = [snapshot_session(p) for p in (args.snapshot_profile or [])]
    snapshots = [json.loads(util.file_contents(f))
                 for f in (args.snapshot_file or [])]
    raw_snapshots = [autodetect_raw_snapshot(json.loads(util.file_contents(f)))
                     for f in (args.raw_snapshot_file or [])]
    if not snapshot_sessions and not snapshots and not raw_snapshots:
        snapshot_sessions = [session]
    response = server.snapshot(
        signing_session=session,
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
    parents=[general_args, server_args],
    help="Get a network snapshot using the Tiros service's credentials"
)

snapshot_parser.set_defaults(func=snapshot)


if __name__ == '__main__':
    main()
