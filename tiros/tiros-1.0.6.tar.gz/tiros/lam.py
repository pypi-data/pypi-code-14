import json
import tiros.iam as iam
import tiros.util as util
from botocore.exceptions import ClientError
from tiros.util import vprint

CODE_BUCKET = 'tiros-lambda'
CODE_KEY = 'tiros-lambda.zip'
CONFIG_ACTION = 'lambda:InvokeFunction'
CONFIG_S3_PREFIX_KEY = 's3-prefix'
CONFIG_PRINCIPAL = 'config.amazonaws.com'
CONFIG_RULE_NAME = 'TirosLambda'
FUN_DESCRIPTION = 'Tiros Lambda'
FUN_HANDLER = 'tiros_lambda.lambda_handler'
FUN_NAME = 'TirosLambda'
FUN_RUNTIME = 'python2.7'
FUN_TIMEOUT = 300
QUERIES_FILE_NAME = 'queries.tql'


def config_s3_prefix_key():
    return CONFIG_S3_PREFIX_KEY


def functions(client):
    res = client.list_functions()
    funs = [d['FunctionName'] for d in res['Functions']]
    m = res.get('NextMarker')
    while m:
        res = client.list_functions(Marker=m)
        funs += [d['FunctionName'] for d in res['Functions']]
        m = res.get('NextMarker')
    return funs


def rule_names(config_client):
    rules = config_client.describe_config_rules()
    return [r['ConfigRuleName'] for r in rules['ConfigRules']]


def lambda_function_exists(client):
    return FUN_NAME in functions(client)


def lambda_arn(account):
    return ''.join(
        ['arn:aws:lambda:us-west-2:', account, ':function:', FUN_NAME])


def create_or_update_lambda_function(session):
    client = session.client('lambda')
    account = util.account(session)
    role = iam.role_arn(account, iam.LAMBDA_ROLE_NAME)
    if lambda_function_exists(client):
        vprint('Updating existing lambda: ' + FUN_NAME)
        client.update_function_code(
            FunctionName=FUN_NAME,
            S3Bucket=CODE_BUCKET,
            S3Key=CODE_KEY)
    else:
        vprint('Creating new lambda: ' + FUN_NAME)
        client.create_function(
            FunctionName=FUN_NAME,
            Runtime=FUN_RUNTIME,
            Role=role,
            Handler=FUN_HANDLER,
            Code={
                'S3Bucket': CODE_BUCKET,
                'S3Key': CODE_KEY
            },
            Description=FUN_DESCRIPTION,
            Timeout=FUN_TIMEOUT)


def delete_lambda(session):
    client = session.client('lambda')
    if lambda_function_exists(client):
        vprint('Deleting lambda: ' + FUN_NAME)
        client.delete_function(FunctionName=FUN_NAME)
    else:
        vprint('There is no lambda named: ' + FUN_NAME)


def create_rule(session, region, s3_prefix, sns_topic_name):
    config_client = session.client('config')
    lambda_client = session.client('lambda')
    if not region:
        region = session.region_name
    params = {
        'region': region,
        's3-prefix': s3_prefix
    }
    if sns_topic_name:
        params['sns-topic-name'] = sns_topic_name
    account = util.account(session)
    rules = rule_names(config_client)
    if CONFIG_RULE_NAME in rules:
        vprint('Rule already created')
        return
    vprint('Giving Config permission to call the Lambda')
    try:
        lambda_client.add_permission(
            FunctionName=FUN_NAME,
            StatementId='ConfigPermission',
            Action=CONFIG_ACTION,
            Principal=CONFIG_PRINCIPAL,
            SourceAccount=account
        )
    except ClientError:
        # If we've already added permission this raises an exception
        # because the StatementId is a duplicate
        pass
    vprint('Creating Config Rule: ' + CONFIG_RULE_NAME)
    try:
        config_client.put_config_rule(
            ConfigRule={
                'ConfigRuleName': CONFIG_RULE_NAME,
                'Source': {
                    'Owner': 'CUSTOM_LAMBDA',
                    'SourceIdentifier': lambda_arn(account),
                    'SourceDetails': [
                        {
                            'EventSource': 'aws.config',
                            'MessageType': 'ScheduledNotification'
                        },
                    ]
                },
                # 'MaximumExecutionFrequency': 'One_Hour',
                'InputParameters': json.dumps(params)
            }
        )
    except ClientError as exn:
        # An error if Config is not set up refers to the deliveryFrequency
        s = str(exn)
        if 'deliveryFrequency' in s and 'MaximumExecutionFrequency' in s:
            print('Got an error suggesting Config has not been turned on.')
            print('Please enable Config before creating a Config Rule from the Tiros CLI.')
            exit(1)


def delete_rule(session):
    client = session.client('config')
    rules = rule_names(client)
    if CONFIG_RULE_NAME not in rules:
        vprint('No Config Rule named: ' + CONFIG_RULE_NAME)
        return
    vprint('Deleting Config Rule: ' + CONFIG_RULE_NAME)
    client.delete_config_rule(ConfigRuleName=CONFIG_RULE_NAME)
