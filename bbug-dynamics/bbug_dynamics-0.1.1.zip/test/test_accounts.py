from bbug_dynamics import Settings, Accounts, Dynamics
import httplib, urllib, json, boto3
from datetime import datetime
from dateutil.relativedelta import relativedelta

def init_accounts(bbug_company_id = 'uk__21'):
    settings= Settings(bbug_company_id).settings
    return Accounts(settings)

def test_all_accounts_status():
    accounts = init_accounts()
    accounts.query()
    assert accounts.response.status == 200

def test_accounts_data():
    accounts = init_accounts()
    accounts.query()
    assert len(accounts.process_response()) > 1

def test_accounts_query():
    accounts = init_accounts()
    date_after_month = datetime.today() + relativedelta(months=1)
    accounts.query({ '$filter': 'modifiedon gt ' +
                        date_after_month.strftime('%Y-%m-%d') })
    assert len(accounts.process_response()) == 0

def test_acounts_get_from_dynamics():
    # reset date in test account
    table_modifiedon=boto3.resource('dynamodb').Table('dynamics_accounts_greather_modifiedon')
    table_modifiedon.put_item(Item={ 'bbug_company_id': 'test', 'modifiedon':
                                    '2010-01-01'})

    accounts = init_accounts('test')
    messages = accounts.get_from_dynamics()
    total_test = len(accounts.data['value'])
    assert  total_test > 1
    assert len(messages) > 1
    accounts2 = init_accounts('localhost__37000')
    messages2 = accounts2.get_from_dynamics()

    total_local = len(accounts2.data['value'])
    assert total_test > total_local
    assert len(messages)>len(messages2)

def test_accounts_get_from_dynamo():
    accounts = init_accounts()
    first_dynamo_account = accounts.get_from_dynamo(limit=1)
    assert len(first_dynamo_account) == 1

def test_to_update():
    accounts = init_accounts('test')
    test_to_update = accounts.to_update()
    assert len(test_to_update)>1
    accounts = init_accounts('uk__21')
    assert len(accounts.to_update())< test_to_update
