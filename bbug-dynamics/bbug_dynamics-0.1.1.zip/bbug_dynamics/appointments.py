import json
from .dynamics import Dynamics
from .bbug import Bbug
from boto3.dynamodb.conditions import Key, Attr
from decimal import *

class Appointments(Dynamics):

    def __init__(self,settings):
        Dynamics.__init__(self,settings)
        self.table=self.dynamodb.Table('dynamics_bookingbug_events')

    def base_uri(self):
        return '/appointments'

    def save(self,bbug_event):
        self.table.put_item(Item=bbug_event)
        self.messages.append("Bookingbug Event " + bbug_event['id'] +
                             " was saved in dynamodb.")

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
                                 FilterExpression='attribute_not_exists(dynamics_updated_at)')
        return response['Items']
