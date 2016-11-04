from bbug_dynamics import Settings,Tasks, Accounts, Bbug

def test_sync():
    settings = Settings('localhost__37000').settings
    tasks = Tasks(settings)
    messages = tasks.sync()
    assert 'Synchronization started for: localhost__37000' == messages[0]
    assert 'Synchronization ended for: localhost__37000' == messages[-1]
    accounts=Accounts(settings)
    dynamo_accounts=accounts.get_from_dynamo()
    print "Accounts in Dynamo:" + str(len(dynamo_accounts))
    for m in messages:
        print m
    bbug = Bbug(settings)
    for account in dynamo_accounts:
        bbug.get_client(account['accountid'])
        assert bbug.response.status_code == 200

def test_after_sync():
    settings = Settings('localhost__37000').settings
    tasks = Tasks(settings)
    messages = tasks.sync()

    # sync without accounts to update
    for m in messages:
        print m
    assert 'There are no accounts to update' in messages

    accounts=Accounts(settings)
    dynamo_accounts=accounts.get_from_dynamo(limit=1)
    account=dynamo_accounts[0]
    del account['bbug_updated_at']
    accounts.save(account)

    # sync with accounts to update
    messages = tasks.sync()
    for m in messages:
        print m
    assert 'There are no accounts to update' not in messages
