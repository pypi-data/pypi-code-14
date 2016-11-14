# Copyright 2016 Formation Data Systems, Inc. All Rights Reserved.
#

from base_cli_test import BaseCliTest
from mock import patch
import mock_functions
from model.fds_error import FdsError
from model.volume.subscription import Subscription
from services.fds_auth import FdsAuth
from services.subscription.subscription_client import SubscriptionClient

def mock_list_subscriptions(volume_id):
    '''Request list of subscriptions for a given volume.

    Parameters
    ----------
    :type volume_id: int
    :param volume_id: Unique identifier for a volume

    Returns
    -------
    :type ``model.FdsError`` or list(``Subscription``)
    '''
    subscriptions = []
    subscription = Subscription(digest="abcdef01",
        name="name1",
        volume_id=volume_id)
    subscriptions.append(subscription)
    subscription = Subscription(digest="abcdef02",
        name="name2",
        volume_id=volume_id)
    subscriptions.append(subscription)
    return subscriptions

def mock_get_request(session, url):
    print url
    response = FdsError()
    return response

def mock_get_url_preamble():
    return "http://localhost:7777/fds/config/v09"

class VolumeSafeGuardTest( BaseCliTest ):
    '''Tests plugin and service client functionality for 'volume safeguard' command.

    IS-A unittest.TestCase.
    '''
    @patch("plugins.volume_plugin.VolumePlugin.pretty_print_volume", side_effect=mock_functions.empty_one)
    @patch("services.response_writer.ResponseWriter.writeTabularData", side_effect=mock_functions.empty_one)
    @patch("services.subscription.subscription_client.SubscriptionClient.list_subscriptions", side_effect=mock_list_subscriptions)
    def test_list_by_volume(self, mockListSubscriptions, mockTabular, mockPretty):
        '''Tests the volume plugin for 'volume safeguard'.
        The subscription service calls are replaced by mock functions.

        Parameters
        ----------
        :type mockListSubscriptions: ``unittest.mock.MagicMock``
        mockTabular (unittest.mock.MagicMock)
        mockPretty (unittest.mock.MagicMock)
        '''
        args = ["volume", "safeguard", "list", "-volume_id=11"]

        self.callMessageFormatter(args)
        self.cli.run(args)
        assert mockListSubscriptions.call_count == 1

        volume_id = mockListSubscriptions.call_args[0][0]
        assert volume_id == 11

        print("test_list_by_volume passed.\n\n")

    @patch("plugins.volume_plugin.VolumePlugin.pretty_print_volume", side_effect=mock_functions.empty_one)
    @patch("services.response_writer.ResponseWriter.writeTabularData", side_effect=mock_functions.empty_one)
    @patch("services.abstract_service.AbstractService.get_url_preamble", side_effect=mock_get_url_preamble)
    @patch("services.rest_helper.RESTHelper.get", side_effect=mock_get_request)
    def test_client_list_subscriptions(self, mockServiceGet, mockUrlPreamble, mockTabular, mockPretty):
        '''Directly tests the real SubscriptionClient.list_subscriptions API.

        Parameters
        ----------
        :type mockServiceGet: ``unittest.mock.MagicMock``
        :param mockServiceGet: Replace REST helper get() with mock empty

        :type mockUrlPreamble: ``unittest.mock.MagicMock``
        :param mockUrlPreamble: Returns the string to prepend for GET Url

        :type mockTabular: ``unittest.mock.MagicMock``
        :type mockPretty: ``unittest.mock.MagicMock``
        '''
        volume_id = 11

        session = FdsAuth()
        client = SubscriptionClient(session)
        client.list_subscriptions(volume_id)

        # The client list_subscription is a url producer
        assert mockServiceGet.call_count == 1
        url = mockServiceGet.call_args[0][1]
        assert url == "http://localhost:7777/fds/config/v09/subscriptions/11"

        print("test_client_list_subscriptions passed.\n\n")

