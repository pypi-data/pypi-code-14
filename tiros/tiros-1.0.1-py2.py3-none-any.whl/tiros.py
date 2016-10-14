#!/usr/bin/env python

"""
Tiros, a VPC network analyzer
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import boto3
import botocore
import datetime
import hashlib
import hmac
import json
import os
import requests
import sys
from botocore.parsers import EC2QueryParser, ResponseParserFactory


# Use new-style classes in Python 2
__metaclass__ = type

TIROS_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# noinspection PyUnresolvedReferences
NOW = datetime.datetime.utcnow()
AMZ_DATE = NOW.strftime('%Y%m%dT%H%M%SZ')
DATE_STAMP = NOW.strftime('%Y%m%d')

# NB: The host HTTP field must be lower case for ARPS.
PROD_HOST = 'prod.tiros.amazonaws.com'
DEV_HOST = 'dev.tiros.amazonaws.com'

CONTENT_TYPE = 'application/json'
API_VERSION = 1
VERBOSE = False
JSON = False
METHOD = 'POST'
COMMANDS = ['snapshot', 'query']
DEFAULT_PROFILE_NAME = 'default'
DEFAULT_SSL = True
DEFAULT_HOST = PROD_HOST
DOCKER_DEFAULT_SNAPSHOT_VOLUME = '/snapshots'
IAM_POLICY_NAME = 'Tiros'
IAM_ROLE_NAME = 'Tiros'
IAM_POLICY = json.loads("""
{
    "Statement": [
        {
            "Action": [
                "ec2:Describe*",
                "elasticache:Describe*",
                "elasticloadbalancing:Describe*",
                "rds:Describe*"
            ],
            "Resource": "*",
            "Effect": "Allow"
        }
    ],
    "Version": "2012-10-17"
}
""")
ASSUME_ROLE_POLICY = json.loads("""
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "sts:AssumeRole",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::748907555215:root"
            }
        }
    ]
}
""")


def vprint(x):
    if VERBOSE:
        print(str(x))


def eprint(s):
    print(s)
    sys.exit(1)


def file_contents(path):
    """
    To support easier use of Docker, if we can't find a file, we look
    for it in the /snapshots directory, which is where we suggest users
    mount their files
    """
    docker_path = os.path.join(DOCKER_DEFAULT_SNAPSHOT_VOLUME, path)
    if os.path.exists(path):
        with open(path) as fd:
            return fd.read()
    elif os.path.exists(docker_path):
        with open(docker_path) as fd:
            return fd.read()
    else:
        # Don't use FileNotFoundError, which doesn't exist in Python2
        raise IOError('File not found: ' + path)


def quote(s):
    return '"' + s + '"'


def _json_encoder(obj):
    """JSON serializer for objects not serializable by default json code"""
    if type(obj) == bytes:
        return obj.decode('utf-8')
    raise TypeError("Type not serializable")


def pretty(x):
    return json.dumps(x, indent=2, sort_keys=True, default=_json_encoder)


def canonical(x):
    return json.dumps(x, sort_keys=True, default=_json_encoder)


class Signer:
    """
    See: http://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html
    """
    @staticmethod
    def sign(key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    @staticmethod
    def get_signature_key(key, date, region, service):
        k_date = Signer.sign(('AWS4' + key).encode('utf-8'), date)
        k_region = Signer.sign(k_date, region)
        k_service = Signer.sign(k_region, service)
        return Signer.sign(k_service, 'aws4_request')

    def __init__(self, access_key, body, host, method, region, route,
                 secret_key):
        assert host.islower(), 'Host must be lower case (for authentication)'
        algorithm = 'AWS4-HMAC-SHA256'
        canonical_querystring = ''
        service = 'tiros'
        signed_headers = 'content-type;host;x-amz-date'
        canonical_headers = (
            'content-type:{}\nhost:{}\nx-amz-date:{}\n'.format(
                CONTENT_TYPE, host, AMZ_DATE))
        payload_hash = hashlib.sha256(body.encode()).hexdigest()
        canonical_request = '\n'.join(
            [method, route, canonical_querystring, canonical_headers,
             signed_headers, payload_hash])
        credential_scope = '/'.join(
            [DATE_STAMP, region, service, 'aws4_request'])
        string_to_sign = '\n'.join(
            [algorithm, AMZ_DATE, credential_scope,
             hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()])
        signing_key = Signer.get_signature_key(
            secret_key, DATE_STAMP, region, service)
        signature = hmac.new(
            signing_key, string_to_sign.encode('utf-8'),
            hashlib.sha256).hexdigest()
        credential = ''.join([access_key, '/', credential_scope])
        # NB: It's important to quote the auth header, since it has characters
        # not generally legal for HTTP headers like '/'
        authorization_header = ''.join([
            algorithm,
            ' Credential=', quote(credential),
            ', SignedHeaders=', quote(signed_headers),
            ', Signature=', signature
        ])
        self.signature = signature
        self.authorization_header = authorization_header


class Profile:
    def __init__(self, name, region, key, secret, session_token):
        self.name = name
        self.region = region
        self.key = key
        self.secret = secret
        self.session_token = session_token

    def _signer(self, body, host, method, route):
        return Signer(self.key, body, host, method, self.region, route,
                      self.secret)

    def auth_header(self, body, host, method, route):
        return self._signer(body, host, method, route).authorization_header

    def request_key(self, body, host, method, route):
        obj = {
            'accessKeyId': self.key,
            'amzDate': AMZ_DATE,
            'body': body,
            'host': host,
            'method': method,
            'region': self.region,
            'route': route,
            'signature': self._signer(body, host, method, route).signature
        }
        # Python encodes None in JSON as "None", not null
        if self.session_token:
            obj['sessionToken'] = self.session_token
        return obj

    def snapshot_key(self, host):
        return self.request_key('', host, METHOD, 'snapshot')

    @staticmethod
    def from_env(region):
        name = 'env'
        session = boto3.Session(region_name=region)
        creds = session.get_credentials()
        key = creds.access_key
        secret = creds.secret_key
        token = creds.token
        return Profile(name, region, key, secret, token)

    @staticmethod
    def from_name(name):
        if '/' not in name:
            session = boto3.Session(profile_name=name)
        else:
            [profile, region] = name.split('/')
            session = boto3.Session(profile_name=profile, region_name=region)
        creds = session.get_credentials()
        key = creds.access_key
        secret = creds.secret_key
        token = creds.token
        return Profile(name, session.region_name, key, secret, token)


def get_route(command):
    assert command in COMMANDS
    return ''.join(['/v', str(API_VERSION), '/', command])


def get_endpoint(ssl, host, route):
    if host in [DEV_HOST, PROD_HOST] and not ssl:
        eprint("You must use SSL with the dev and prod hosts")
    proto = 'https' if ssl else 'http'
    return ''.join([proto, '://', host, route])


def get_headers(auth_header, signing_profile):
    headers = {
        'Authorization': auth_header,
        'Content-Type': CONTENT_TYPE,
        'X-Amz-Date': AMZ_DATE
    }
    token = signing_profile.session_token
    if token:
        headers['X-Amz-Security-Token'] = token
    return headers


def format_json_response(response):
    # noinspection PyUnresolvedReferences
    try:
        return json.loads(response.text)
    # The exception thrown on json parse failure in python3 is
    # json.decoder.JSONDecodeError, which does not exist in python2.
    # Fortunately, what python2 throws in that case is ValueError,
    # which is a superclass of json.decoder.JSONDecodeError.
    except ValueError:
        return {'error': response.text}


def format_response(response):
    j = format_json_response(response)
    if 'error' in j and not VERBOSE:
        return j['error']['message']
    else:
        return pretty(j)


def autodetect_raw_snapshot(s):
    # For Palisade snapshots, the raw snapshot holds the actual snapshot
    # in the db field
    if 'db' in s:
        return s.get('db')
    else:
        return s


def boto_session(profile, role_arn=None):
    session = boto3.Session(
        aws_access_key_id=profile.key,
        aws_secret_access_key=profile.secret,
        aws_session_token=profile.session_token,
        region_name=profile.region)
    if role_arn:
        sts = session.client('sts')
        creds = sts.assume_role(
            RoleArn=role_arn,
            RoleSessionName='tiros',  # arbitrary
        )
        if 'Credentials' not in creds:
            eprint("Couldn't assume role: " + role_arn)
        cs = creds['Credentials']
        akid = cs['AccessKeyId']
        secret = cs['SecretAccessKey']
        token = cs['SessionToken'] if 'SessionToken' in cs else None
        session = boto3.Session(
            aws_access_key_id=akid,
            aws_secret_access_key=secret,
            aws_session_token=token,
            region_name=profile.region)
    return session


'''Fetch'''


# noinspection PyProtectedMember
class PassthroughParser(EC2QueryParser):
    """
    What follows is a patch to also include the raw xml on the wire
    before it hits all of botocore's xml -> json parsing. The reason we
    want the raw xml out is the fact that we can pass it directly to the
    pre-existing nice type-safe java xml unmarshalers on the scala side
    of the world. We also return the parsed json data so that we can do
    pagination and extract certain other bits of it when we need to.
    """
    # noinspection PyMissingConstructor
    def __init__(self, _parser):
        self.old_parser = _parser

    def _do_parse(self, response, shape):
        parsed = self.old_parser._do_parse(response, shape)
        return {'xml': response['body'], 'parsed': parsed}


class PassthroughParserFactory(ResponseParserFactory):
    # noinspection PyMissingConstructor
    def __init__(self, factory):
        self.old_factory = factory

    def create_parser(self, protocol_name):
        _parser = self.old_factory.create_parser(protocol_name)
        return PassthroughParser(_parser)


def fetch(snapshot_profile, role_arn=None):
    assert snapshot_profile
    vprint('Snapshot profile: {}'.format(snapshot_profile.name))
    session = boto_session(snapshot_profile, role_arn)

    # This will intentionally fail for api calls that *can* be
    # paginated, because you should be calling get_pages. Returns one
    # xml string of all the results.
    def get_results(client, method, **kwargs):
        result = getattr(client, method)(**kwargs)
        assert not (client.can_paginate(method))
        return result['xml']

    # This will intentionally fail (because the get_paginator call
    # will fail) for api calls that *can't* be paginated, because you
    # should be calling get_results. Returns a list of xml strings of
    # all the results.
    # noinspection PyProtectedMember
    def get_pages(client, method, **kwargs):
        # XXX: CLI dies with an inscrutable error message on this line if the
        # caller doesn't have permission.  The error message should be better.
        result = getattr(client, method)(**kwargs)
        pagination = client.get_paginator(method)._pagination_cfg
        input_token = pagination['input_token']
        output_token = pagination['output_token']
        result_key = pagination['result_key']

        parsed = result['parsed']
        rv = {'xml': [result['xml']], 'parsed': result['parsed'][result_key]}
        if output_token in parsed:
            kwargs.update({input_token: parsed[output_token]})
            rest = get_pages(client, method, **kwargs)
            rv['xml'] += rest['xml']
            rv['parsed'] += rest['parsed']
        return rv

    def get_pages_xml(client, method, **kwargs):
        return get_pages(client, method, **kwargs)['xml']

    # noinspection PyProtectedMember
    def xml_client(client):
        old_factory = client._endpoint._response_parser_factory
        client._endpoint._response_parser_factory = PassthroughParserFactory(
            old_factory)
        return client

    ec2 = xml_client(session.client('ec2'))
    elb = xml_client(session.client('elb'))

    elb_results = get_pages(elb, 'describe_load_balancers', PageSize=1)
    elb_names = [e['LoadBalancerName'] for e in elb_results['parsed']]

    # XXX in the aws documentation (e.g.
    # http://docs.aws.amazon.com/cli/latest/reference/ec2/describe-nat-gateways.html)
    # it appears that the output of describe_nat_gateways,
    # describe_vpc_endpoints, and describe_vpc_peering_connections may
    # sometimes be paginated, but boto3 does not appear to support
    # pagination for them. Which is very strange, since the official
    # aws cli uses boto.
    return {
        "describe_availability_zones":
            get_results(ec2, 'describe_availability_zones'),
        "describe_instances":
            get_pages_xml(ec2, 'describe_instances'),
        "describe_internet_gateways":
            get_results(ec2, 'describe_internet_gateways'),
        "describe_nat_gateways":
            get_results(ec2, 'describe_nat_gateways'),
        "describe_network_acls":
            get_results(ec2, 'describe_network_acls'),
        "describe_network_interfaces":
            get_results(ec2, 'describe_network_interfaces'),
        "describe_prefix_lists":
            get_results(ec2, 'describe_prefix_lists'),
        "describe_regions":
            get_results(ec2, 'describe_regions'),
        "describe_route_tables":
            get_results(ec2, 'describe_route_tables'),
        "describe_security_groups":
            get_results(ec2, 'describe_security_groups'),
        "describe_subnets":
            get_results(ec2, 'describe_subnets'),
        "describe_vpc_endpoints":
            get_results(ec2, 'describe_vpc_endpoints'),
        "describe_vpc_peering_connections":
            get_results(ec2, 'describe_vpc_peering_connections'),
        "describe_vpcs":
            get_results(ec2, 'describe_vpcs'),

        "describe_load_balancers": {
            "describe_load_balancers":
                elb_results['xml'],
            "describe_load_balancer_tags":
                [get_results(elb, 'describe_tags', LoadBalancerNames=[elb_name])
                 for elb_name in elb_names],
            "describe_load_balancer_attributes":
                [{'name': elb_name,
                  'body': get_results(elb, 'describe_load_balancer_attributes',
                                      LoadBalancerName=elb_name)}
                 for elb_name in elb_names]}
        }


def top_fetch(args):
    snapshot_profile_name = args.snapshot_profile
    snapshot_profile = Profile.from_name(snapshot_profile_name)
    print(pretty(fetch(snapshot_profile, role_arn=args.role_arn)))
    sys.exit(0)


'''Snapshot'''


def snapshot(signing_profile,
             snapshots=None,
             raw_snapshots=None,
             profiles=None,
             ssl=DEFAULT_SSL,
             host=DEFAULT_HOST):
    route = get_route('snapshot')
    endpoint = get_endpoint(ssl, host, route)
    vprint('Endpoint: ' + endpoint)
    obj_body = (
        [{'credentials': p.snapshot_key(host)} for p in (profiles or [])] +
        [{'snapshot': s} for s in (snapshots or [])] +
        [{'raw_snapshot': s} for s in (raw_snapshots or [])]
    )
    body = canonical(obj_body)
    auth_header = signing_profile.auth_header(body, host, METHOD, route)
    headers = get_headers(auth_header, signing_profile)
    vprint('Headers: ' + pretty(headers))
    return requests.request(METHOD, endpoint, headers=headers, data=body)


def top_snapshot(args):
    signing_profile = Profile.from_name(args.signing_profile)
    ssl = not args.no_ssl
    host = args.host or (DEV_HOST if args.dev else PROD_HOST)
    profiles = [Profile.from_name(p) for p in (args.snapshot_profile or [])]
    snapshots = [json.loads(file_contents(f))
                 for f in (args.snapshot_file or [])]
    raw_snapshots = [autodetect_raw_snapshot(json.loads(file_contents(f)))
                     for f in (args.raw_snapshot_file or [])]
    if not profiles and not snapshots and not raw_snapshots:
        profiles = [signing_profile]
    response = snapshot(
        signing_profile=signing_profile,
        snapshots=snapshots,
        raw_snapshots=raw_snapshots,
        profiles=profiles,
        ssl=ssl,
        host=host)
    vprint('Status code: ' + str(response.status_code))
    print(format_response(response))
    if response.status_code != 200:
        sys.exit(1)
    sys.exit(0)


'''Query'''


def query(signing_profile,
          queries,
          snapshots=None,
          raw_snapshots=None,
          profiles=None,
          backend=None,
          transforms=None,
          user_relations=None,
          ssl=DEFAULT_SSL,
          host=DEFAULT_HOST):
    route = get_route('query')
    endpoint = get_endpoint(ssl, host, route)
    dbs = (
        [{'credentials': p.snapshot_key(host)} for p in (profiles or [])] +
        [{'snapshot': s} for s in (snapshots or [])] +
        [{'raw_snapshot': s} for s in (raw_snapshots or [])]
    )
    obj_body = {'queries':  queries, 'dbs': dbs}
    if backend:
        obj_body['backend'] = backend
    if transforms:
        obj_body['transforms'] = transforms
    if user_relations:
        obj_body['userRelations'] = user_relations
    vprint('Body: ' + pretty(obj_body))
    body = canonical(obj_body)
    auth_header = signing_profile.auth_header(body, host, METHOD, route)
    headers = get_headers(auth_header, signing_profile)
    vprint('Headers: ' + pretty(headers))
    return requests.request(METHOD, endpoint, headers=headers, data=body)


def top_query(args):
    signing_profile = Profile.from_name(args.signing_profile)
    profiles = [Profile.from_name(p) for p in (args.snapshot_profile or [])]
    snapshots = [json.loads(file_contents(f))
                 for f in (args.snapshot_file or [])]
    raw_snapshots = [autodetect_raw_snapshot(json.loads(file_contents(f)))
                     for f in (args.raw_snapshot_file or [])]
    ssl = not args.no_ssl
    host = args.host or (DEV_HOST if args.dev else PROD_HOST)
    if args.inline and args.queries_file:
        eprint("Can't specify both --inline and --queries_file")
    if args.inline:
        queries = args.inline
    elif args.queries_file:
        queries = file_contents(args.queries_file)
    else:
        queries = None
        eprint('You must specify --inline or --queries_file')
    if args.relations_file:
        user_relations = file_contents(args.relations_file)
    else:
        user_relations = None
    if not profiles and not snapshots and not raw_snapshots:
        profiles = [signing_profile]
    response = query(
        signing_profile=signing_profile,
        queries=queries,
        snapshots=snapshots,
        raw_snapshots=raw_snapshots,
        profiles=profiles,
        backend=args.backend,
        transforms=args.transform,
        user_relations=user_relations,
        ssl=ssl,
        host=host)
    vprint('Status code: ' + str(response.status_code))
    print(format_response(response))
    if response.status_code != 200:
        sys.exit(1)
    sys.exit(0)


'''Allow'''


def iam_policy_arn(account):
    return 'arn:aws:iam::' + account + ':policy/Tiros'


def get_default_policy(client, account):
    try:
        arn = iam_policy_arn(account)
        policy = client.get_policy(PolicyArn=arn)
        version = policy['Policy']['DefaultVersionId']
        doc = client.get_policy_version(PolicyArn=arn, VersionId=version)
        return doc['PolicyVersion']['Document']
    except botocore.exceptions.ClientError:
        return None


def create_or_update_policy(client, account):
    policy = get_default_policy(client, account)
    if not policy:
        vprint('Creating Tiros policy')
        client.create_policy(
            PolicyName=IAM_POLICY_NAME,
            PolicyDocument=pretty(IAM_POLICY),
            Description='For Tiros, a VPC network analyzer')
    else:
        if policy != IAM_POLICY:
            vprint('Updating Tiros policy')
            client.create_policy_version(
                PolicyArn=iam_policy_arn(account),
                PolicyDocument=pretty(IAM_POLICY),
                SetAsDefault=True)
        else:
            vprint('Policy is up to date')


def create_or_update_role(client, account):
    try:
        role = client.get_role(RoleName=IAM_ROLE_NAME)
        policy = role['Role']['AssumeRolePolicyDocument']
        if policy != ASSUME_ROLE_POLICY:
            vprint('Updating Tiros role')
            client.update_assume_role_policy(
                RoleName=IAM_ROLE_NAME,
                PolicyDocument=pretty(ASSUME_ROLE_POLICY))
        else:
            vprint('Role is up to date')
    except botocore.exceptions.ClientError:
        vprint('Creating Tiros role')
        client.create_role(
            RoleName=IAM_ROLE_NAME,
            AssumeRolePolicyDocument=pretty(ASSUME_ROLE_POLICY))
    policies = client.list_attached_role_policies(RoleName=IAM_ROLE_NAME)
    if any([p['PolicyName'] == IAM_POLICY_NAME
            for p in policies['AttachedPolicies']]):
        vprint('Tiros role policies are OK')
    else:
        vprint('Adding Tiros policy to Tiros role')
        arn = iam_policy_arn(account)
        client.attach_role_policy(RoleName=IAM_ROLE_NAME, PolicyArn=arn)


def top_allow(args):
    profile = Profile.from_name(args.profile)
    session = boto_session(profile, args.role_arn)
    account = args.account
    if not account:
        account = session.client('sts').get_caller_identity().get('Account')
    iam = session.client('iam')
    create_or_update_policy(iam, account)
    create_or_update_role(iam, account)


'''Commandline Arguments'''


parser = argparse.ArgumentParser(description='Tiros, version 1.0')

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
    e.g. localhost:9000
    '''
)

server_group.add_argument(
    '--no-ssl',
    action='store_true',
    help='Use HTTP, not HTTPS'
)

snapshot_group = argparse.ArgumentParser(add_help=False)

snapshot_group.add_argument(
    '--signing-profile',
    '-p',
    default=DEFAULT_PROFILE_NAME,
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

fetch_parser = subparsers.add_parser(
    'fetch',
    parents=[general_group]
)

fetch_parser.set_defaults(func=top_fetch)

# We only allow one snapshot profile for fetch, so don't copy
# argument from snapshot_group
fetch_parser.add_argument(
    '--snapshot-profile',
    '-n',
    default=DEFAULT_PROFILE_NAME,
    help="""
    An AWS profile name or profile/region pair.
    (e.g. dev, dev/us-east-1, prod/us-west-2).
    Multiple profiles are supported.  If no profile is
    provided the default is used. If no region
    is specified for a profile, the default region for the
    profile is used.
    """
)

fetch_parser.add_argument(
    '--role-arn',
    '-r',
    help='An IAM role arn to assume before fetching'
)

snapshot_parser = subparsers.add_parser(
    'snapshot',
    parents=[general_group, server_group, snapshot_group]
)

snapshot_parser.set_defaults(func=top_snapshot)

query_parser = subparsers.add_parser(
    'query',
    parents=[general_group, server_group, snapshot_group]
)

query_parser.set_defaults(func=top_query)

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


allow_parser = subparsers.add_parser(
    'allow',
    parents=[general_group]
)

allow_parser.set_defaults(func=top_allow)

allow_parser.add_argument(
    '--account',
    '-a',
    help='The account where we will add a Tiros IAM role'
)

allow_parser.add_argument(
    '--profile',
    '-p',
    default=DEFAULT_PROFILE_NAME,
    help='The profile with permission to add an IAM role to the account'
)

allow_parser.add_argument(
    '--role-arn',
    '-r',
    help='An IAM role arn to assume before modifying the role'
)

'''Main'''


def main():
    global VERBOSE
    global JSON
    args = parser.parse_args()
    if args.verbose:
        VERBOSE = True
    if args.json:
        JSON = True
    if not args.cmd:
        print("No subcommand specified")
        parser.print_help()
        sys.exit(1)
    args.func(args)


if __name__ == '__main__':
    main()
