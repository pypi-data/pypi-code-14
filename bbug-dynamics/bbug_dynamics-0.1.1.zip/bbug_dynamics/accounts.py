import json
from .dynamics import Dynamics
from .bbug import Bbug
from boto3.dynamodb.conditions import Key, Attr
from decimal import *

class Accounts(Dynamics):

    def __init__(self,settings):
        Dynamics.__init__(self,settings)
        self.table=self.dynamodb.Table('dynamics_accounts')

    def base_uri(self):
        return '/accounts'

    def save(self,account):
        self.table.put_item(Item=account)
        self.messages.append("Account " + account['name'] +
                             " was saved in dynamodb.")

    def get_from_dynamics(self, param_modifiedon=''):
        """Get all the accounts with modifiedon greather than the latest
        modifiedon updated account. To change the defuault filter can use the
        param_modfiedon.

        Args:
            self (Accounts): Instance of Accounts.
            param_modifiedon (str): By defualt is an empty str, only used to
            force a modifiedon date.
        """
        # get in dynamo the date of latest update
        table_modifiedon = self.dynamodb.Table('dynamics_accounts_greather_modifiedon')

        try:
            last_update=table_modifiedon.get_item( Key={ 'bbug_company_id':
                                                        self.bbug_company_id })
            modifiedon=last_update['Item']['modifiedon']
        except:
            modifiedon='2000-01-01'

        # update all accounts greather than a param_modifiedon
        if param_modifiedon!='':
            modifiedon=param_modifiedon

        # get all accounts modifiedon after the latest update
        self.query({'$filter': 'modifiedon gt ' + modifiedon })
        self.data=json.loads(self.response.read())


        for account in self.data['value']:
            account['bbug_company_id']=self.bbug_company_id
            for k in account.keys():
                if isinstance(account[k] , float):
                    account[k]=Decimal(str(account[k]))
            self.save(account)
        return self.get_messages()

    def get_messages(self):
        """Get messages and clean the messages instance variable
        """
        messages = self.messages
        self.messages=[]
        return messages

    def get_from_dynamo(self, limit = 100 ):
        response=self.table.query( KeyConditionExpression= Key('bbug_company_id').eq( self.bbug_company_id), Limit=limit)
        return response['Items']

    def to_update(self):
        response=self.table.query( KeyConditionExpression= Key('bbug_company_id').eq( self.bbug_company_id),
                                 FilterExpression='attribute_not_exists(bbug_updated_at)')
        return response['Items']
