from bbug_dynamics import Bbug, Settings
from test_accounts import init_accounts

def init_bbug(bbug_company_id = 'uk__21'):
    settings = Settings(bbug_company_id).settings
    return Bbug(settings)

def test_init():
    bbug =init_bbug()
    assert(bbug.response.status_code == 201)

def test_save_client():
    accounts = init_accounts('localhost__37000')
    accounts_from_dynamo = accounts.get_from_dynamo(limit=30)
    bbug =init_bbug()
    for x in accounts_from_dynamo:
        messages=bbug.save_client(x)
        assert len(messages)>0
        print "status " + `bbug.response.status_code` + " for accountid: " + x['accountid']
        assert(bbug.response.status_code in [200,404])
        assert(bbug.bbug_response.status_code in [200,404])

def test_client_fields():
    accounts = init_accounts('localhost__37000')
    accounts_from_dynamo = accounts.get_from_dynamo(limit=30)
    bbug =init_bbug()
    for account in accounts_from_dynamo:
        client = bbug.get_client(account['accountid'])
        print "checking " + account['accountid']
        assert client['reference'] == account['accountid']
        assert client['last_name'] == account["name"]

        if account["emailaddress1"] != None:
            print "email: " + client['email']
            assert client['email'] == account["emailaddress1"]
        else:
            print "acount emailaddress1 None"
            assert client['email'] == ''

        if 'mobile' in client.keys():
            print "mobile:" + client['mobile'] + " telephone1: " + account["telephone1"]
            if '-' in account["telephone1"]:
                tel=account["telephone1"].split('-')
                if '+' in tel[0]:
                  del tel[0]
                tel= ''.join(tel)
            else:
                tel= account["telephone1"]

            tel=tel.replace('(','')
            tel=tel.replace(')','')

            assert tel in ('0' + client['mobile'])
        else:
            assert account['telephone1'] == None

        if 'postcode' in client.keys():
            assert client['postcode'] == account["address1_postalcode"]
        else:
            assert  account["address1_postalcode"] == None
#
# In bookinbug is not saved I don't know why this field in the api
#        if 'join_date' in client.keys():
#             print "join_date:" + client['join_date']
#            assert client['join_date'] == account["opendeals_date"][0:30]
#        else:
#            assert account["opendeals_date"] == None

        print "client country: "+  client['country'] + " accuont_country: " +  str(account["address1_country"])



