import boto3
import re

import json

def detect_security_group(region, sg_regex):
    ec2 = boto3.client('ec2', region)

    sgs = [sg for sg in ec2.describe_security_groups()['SecurityGroups'] if re.match(sg_regex, sg['GroupName'])]

    if len(sgs) == 0:
        fatal_error('Could not find security group which matches regex {}'.format(sg_regex))

    if len(sgs) > 1:
        fatal_error('More than one security group found for regex {}'.format(sg_regex))

    return sgs[0]

print(json.dumps(detect_security_group('eu-central-1', 'app-zmon-db')))
