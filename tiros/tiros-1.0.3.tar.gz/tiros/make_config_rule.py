import json
import tiros.make_lambda

RULE_NAME = 'TirosRule'


def make_config_rule(session, params_file):
    client = session.client('config')
    names = client.describe_config_rules()
    params = json.dumps({
        'ParamsFile': params_file
    })
    if [r for r in names['ConfigRules'] if r['ConfigRuleName'] == RULE_NAME]:
        return
    client.put_config_rule(
        ConfigRule={
            'ConfigRuleName': RULE_NAME,
            'Source': {
                'Owner': 'CUSTOM_LAMBDA',
                'SourceIdentifier': tiros.make_lambda.FUN_NAME,
                'SourceDetails': [
                    {
                        'EventSource': 'aws.config',
                        'MessageType': 'ConfigurationSnapshotDeliveryCompleted'
                    },
                ]
            },
            'MaximumExecutionFrequency': 'One_Hour',
            'InputParameters': params
        }
    )
