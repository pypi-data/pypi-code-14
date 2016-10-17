# Copyright (c) 2016, Formation Data Systems, Inc. All Rights Reserved.
#
import json
from services.abstract_service import AbstractService
from model.fds_error import FdsError
from model.volume.subscription import Subscription
from utils.converters.volume.subscription_converter import SubscriptionConverter

class SubscriptionClient(AbstractService):
    '''
    Formation Subscription
    Formation Subscription is a web service that enables a volume to subscribe to one or
    more SafeGuard policies. SafeGuard policies enable management of data migration tasks.
    Each SafeGuard policy can reference a durable storage endpoint and specify a recurrence
    rule for data migration.

    To provide end-user credentials, first use the CredentialsClient and make a call to
    create. That call will provide a unique identifier for the persisted credentials. Each
    named credential supplies a URL for the data migration destination.

    Client
    This low-level API provides one-to-one mappings to the underlying HTTP API operations.
    '''

    def __init__(self, session):
        '''
        :type session: ``services.FdsAuth``
        :param session: Data about the active session
        '''
        AbstractService.__init__(self, session)

    def create_subscription(self, subscription):
        '''Create a subscription

        Parameters
        ----------
        :type subscription: ``model.volume.Subscription``
        :param subscription: Subscription object

        Returns
        -------
        :type ``model.FdsError`` or ``model.volume.Subscription``
        '''
        j_str = SubscriptionConverter.to_json(subscription)

        # Adds additional members
        d = json.loads(j_str)
        d["primaryDomainId"] = 0

        url="{}{}".format(self.get_url_preamble(), "/subscriptions")
        data = json.dumps(d)

        response = self.rest_helper.post(self.session, url, data)

        if isinstance(response, FdsError):
            return response

        deserialized = SubscriptionConverter.build_from_json(response)
        return deserialized

    def list_subscriptions(self, volume_id):
        '''Request list of subscriptions for a given volume.

        Parameters
        ----------
        :type volume_id: int
        :param volume_id: Unique identifier for a volume

        Returns
        -------
        :type ``model.FdsError`` or list(``Subscription``)
        '''
        url = "{}{}{}".format(self.get_url_preamble(), "/subscriptions/", volume_id)
        response = self.rest_helper.get(self.session, url)

        if isinstance(response, FdsError):
            return response

        subscriptions = []

        for j_subscription in response:
           subscription = SubscriptionConverter.build_from_json(j_subscription)
           subscriptions.append(subscription)

        return subscriptions

    def delete_subscription(self, subscription):
        '''Delete a subscription

        Parameters
        ----------
        :type subscription: ``model.volume.Subscription``
        :param subscription: Subscription object

        Returns
        -------
        :type ``model.FdsError`` or delete response
        '''
        url="{}{}{}".format(self.get_url_preamble(), "/subscriptions/",
            subscription.name)

        response = self.rest_helper.delete(self.session, url)

        if isinstance(response, FdsError):
            return response

        return response 

