import botocore
import json

import tiros.util as util
from tiros.util import vprint

IAM_POLICY_NAME = 'Tiros'

# The name for cross-account IAM roles to allow Tiros to make calls
# on the user's behalf.  Note that this name is actually required by
# the Tiros service, while iam_policy_name
IAM_ROLE_NAME = 'Tiros'

# The minimal permissions Tiros requires to download a network snapshot
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

# The policy that allows the Tiros account to assume a role in a
# customer account.
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
            PolicyDocument=util.pretty(IAM_POLICY),
            Description='For Tiros, a VPC network analyzer')
    else:
        if policy != IAM_POLICY:
            vprint('Updating Tiros policy')
            client.create_policy_version(
                PolicyArn=iam_policy_arn(account),
                PolicyDocument=util.pretty(IAM_POLICY),
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
                PolicyDocument=util.pretty(ASSUME_ROLE_POLICY))
        else:
            vprint('Role is up to date')
    except botocore.exceptions.ClientError:
        vprint('Creating Tiros role')
        client.create_role(
            RoleName=IAM_ROLE_NAME,
            AssumeRolePolicyDocument=util.pretty(ASSUME_ROLE_POLICY))
    policies = client.list_attached_role_policies(RoleName=IAM_ROLE_NAME)
    if any([p['PolicyName'] == IAM_POLICY_NAME
            for p in policies['AttachedPolicies']]):
        vprint('Tiros role policies are OK')
    else:
        vprint('Adding Tiros policy to Tiros role')
        arn = iam_policy_arn(account)
        client.attach_role_policy(RoleName=IAM_ROLE_NAME, PolicyArn=arn)


def allow(session):
    account = session.client('sts').get_caller_identity().get('Account')
    client = session.client('iam')
    create_or_update_policy(client, account)
    create_or_update_role(client, account)
