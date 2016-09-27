import argparse
import boto3
import sys
import json

def main():
    parser = argparse.ArgumentParser(description='Creates a federated aws user with limited privileges.')
    parser.add_argument('name', help='federation token name')
    parser.add_argument('--duration', default=3600, help='session length')
    parser.add_argument('--iam-role', help='iam role')
    args = parser.parse_args()

    # fetch policies by role name
    iam = boto3.client('iam')
    response = iam.list_role_policies(RoleName=args.iam_role)

    statements = []
    for policy_name in response['PolicyNames']:
        response = iam.get_role_policy(RoleName=args.iam_role, PolicyName=policy_name)
        statements += response['PolicyDocument']['Statement']

    policy = {'Version': '2012-10-17', 'Statement': statements}

    # create federation token
    sts = boto3.client('sts')

    response = sts.get_federation_token(Name=args.name, Policy=json.dumps(policy), DurationSeconds=args.duration)
    credentials = response['Credentials']
    print("set -e AWS_ACCESS_KEY")
    print("set -e AWS_SECRET_KEY")
    print("set -x AWS_CREDS_NAME '%s*'" % args.name)
    print("set -x AWS_ACCESS_KEY_ID %s" % credentials['AccessKeyId'])
    print("set -x AWS_SECRET_ACCESS_KEY %s" % credentials['SecretAccessKey'])
    print("set -x AWS_SESSION_TOKEN '%s'" % credentials['SessionToken'])
