import json

from botocore.exceptions import ClientError
import tiros.util as util
from tiros.util import vprint

# The name for the IAM policy with permissions for Tiros to describe
# networks
TIROS_POLICY_NAME = 'Tiros'

# The minimal permissions Tiros requires to download a network snapshot
TIROS_POLICY = json.loads("""
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

# The policy that allows the Tiros account to assume a role in a
# customer account.
TIROS_ASSUME_ROLE_POLICY = json.loads("""
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

# The name for cross-account IAM roles to allow Tiros to make calls
# on the user's behalf.  Note that this name is actually required by
# the Tiros service, while iam_policy_name
TIROS_ROLE_NAME = 'Tiros'

# Policies to attach to the Lambda role
LAMBDA_POLICY_NAMES = [TIROS_POLICY_NAME,
                       'AWSLambdaBasicExecutionRole',
                       'AWSConfigRulesExecutionRole']

LAMBDA_ASSUME_ROLE_POLICY = json.loads("""
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "sts:AssumeRole",
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            }
        }
    ]
}
""")

LAMBDA_ROLE_NAME = 'TirosLambda'


def s3_policy_statement(s3_prefix):
    s3_prefix = s3_prefix.replace('s3://', '')
    return {
        "Effect": "Allow",
        "Action": ["s3:PutObject", "s3:GetObject"],
        "Resource": ["arn:aws:s3:::" + s3_prefix + '*']
    }


def sns_policy_statement(sns_topic_arn):
    return {
        "Action": ["SNS:Publish"],
        "Effect": "Allow",
        "Resource": sns_topic_arn
    }


def lambda_inline_policy(s3_prefix, sns_topic_arn):
    statements = []
    if s3_prefix:
        statements += [s3_policy_statement(s3_prefix)]
    if sns_topic_arn:
        statements += [sns_policy_statement(sns_topic_arn)]
    return util.pretty({
        "Version": "2012-10-17",
        "Statement": statements
    })


def policy_arn(account, policy_name):
    return ''.join(['arn:aws:iam::', account, ':policy/', policy_name])


def role_arn(account, role_name):
    return ''.join(['arn:aws:iam::', account, ':role/', role_name])


def get_default_policy(client, account, policy_name):
    try:
        arn = policy_arn(account, policy_name)
        policy = client.get_policy(PolicyArn=arn)
        version = policy['Policy']['DefaultVersionId']
        doc = client.get_policy_version(PolicyArn=arn, VersionId=version)
        return doc['PolicyVersion']['Document']
    except ClientError:
        return None


def create_or_update_policy(client, account, policy_name, policy):
    existing_policy = get_default_policy(client, account, policy_name)
    if not existing_policy:
        vprint('Creating policy: ' + policy_name)
        client.create_policy(
            PolicyName=policy_name,
            PolicyDocument=util.pretty(policy))
    else:
        if existing_policy != policy:
            vprint('Updating policy: ' + policy_name)
            client.create_policy_version(
                PolicyArn=policy_arn(account, policy_name),
                PolicyDocument=util.pretty(policy),
                SetAsDefault=True)
        else:
            vprint('Policy is up to date: ' + policy_name)


def create_or_update_role(client, role_name, assume_role_policy):
    try:
        role = client.get_role(RoleName=role_name)
        policy = role['Role']['AssumeRolePolicyDocument']
        if policy != assume_role_policy:
            vprint('Updating role: ' + role_name)
            client.update_assume_role_policy(
                RoleName=role_name,
                PolicyDocument=util.pretty(assume_role_policy))
        else:
            vprint('Role is up to date: ' + role_name)
    except ClientError:
        vprint('Creating role: ' + role_name)
        client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=util.pretty(assume_role_policy))


def add_policy_to_role(client, account, role_name, policy_name):
    policies = client.list_attached_role_policies(RoleName=role_name)
    if any([p['PolicyName'] == policy_name
            for p in policies['AttachedPolicies']]):
        vprint(role_name + ' policies are OK')
    else:
        try:
            arn = ''.join(['arn:aws:iam::', account, ':policy/', policy_name])
            client.attach_role_policy(RoleName=role_name, PolicyArn=arn)
            vprint('Added local policy: ' + policy_name + ' to role: ' + role_name)
        except ClientError:
            arn = 'arn:aws:iam::aws:policy/service-role/' + policy_name
            client.attach_role_policy(RoleName=role_name, PolicyArn=arn)
            vprint('Added managed policy: ' + policy_name + ' to role: ' + role_name)


def add_inline_policy_to_role(client, role_name, policy_name, policy):
    vprint('Adding inline policy: ' + policy_name + ' to role: ' + role_name)
    client.put_role_policy(
        RoleName=role_name,
        PolicyName=policy_name,
        PolicyDocument=policy)


def role_names(client):
    roles = client.list_roles()['Roles']
    return [r['RoleName'] for r in roles]


def delete_role(client, role_name):
    if role_name not in role_names(client):
        vprint('No such role: ' + role_name)
        return
    policies = client.list_attached_role_policies(RoleName=role_name)
    for p in policies.get('AttachedPolicies'):
        vprint('Detaching policy: ' + p.get('PolicyName') + ' from role: ' + role_name)
        client.detach_role_policy(RoleName=role_name,
                                  PolicyArn=p.get('PolicyArn'))
    policies = client.list_role_policies(RoleName=role_name)
    for p in policies.get('PolicyNames'):
        vprint('Detaching policy: ' + p + ' from role: ' + role_name)
        client.delete_role_policy(RoleName=role_name, PolicyName=p)
    vprint('Deleting role: ' + role_name)
    client.delete_role(RoleName=role_name)


def policy_names(client):
    policies = client.list_policies(Scope='Local')['Policies']
    return [p['PolicyName'] for p in policies]


def delete_policy(client, account, policy_name):
    if policy_name not in policy_names(client):
        vprint('No such policy: ' + policy_name)
        return
    vprint('Deleting policy: ' + policy_name)
    arn = policy_arn(account, policy_name)
    for v in client.list_policy_versions(PolicyArn=arn)['Versions']:
        if not v.get('IsDefaultVersion'):
            vid = v['VersionId']
            vprint('Deleting policy version: ' + vid)
            client.delete_policy_version(PolicyArn=arn, VersionId=vid)
    client.delete_policy(PolicyArn=arn)


def create_tiros_policy(session):
    client = session.client('iam')
    account = util.account(session)
    create_or_update_policy(client, account, TIROS_POLICY_NAME, TIROS_POLICY)


def delete_tiros_policy(session):
    client = session.client('iam')
    account = util.account(session)
    delete_policy(client, account, TIROS_POLICY_NAME)


def create_tiros_role(session):
    client = session.client('iam')
    account = util.account(session)
    create_or_update_role(client, TIROS_ROLE_NAME, TIROS_ASSUME_ROLE_POLICY)
    add_policy_to_role(client, account, TIROS_ROLE_NAME, TIROS_POLICY_NAME)


def delete_tiros_role(session):
    client = session.client('iam')
    delete_role(client, TIROS_ROLE_NAME)


def create_lambda_role(session, s3_prefix, sns_topic_arn):
    client = session.client('iam')
    account = util.account(session)
    create_or_update_role(client, LAMBDA_ROLE_NAME, LAMBDA_ASSUME_ROLE_POLICY)
    for p in LAMBDA_POLICY_NAMES:
        add_policy_to_role(client, account, LAMBDA_ROLE_NAME, p)
    if s3_prefix or sns_topic_arn:
        add_inline_policy_to_role(
            client=client,
            role_name=LAMBDA_ROLE_NAME,
            policy_name='TirosLambdaS3SNS',
            policy=lambda_inline_policy(s3_prefix, sns_topic_arn))


def delete_lambda_role(session):
    client = session.client('iam')
    delete_role(client, LAMBDA_ROLE_NAME)
