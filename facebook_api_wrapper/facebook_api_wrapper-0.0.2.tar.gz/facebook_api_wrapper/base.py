import os
import logging
from functools import wraps

from facebookads.exceptions import FacebookRequestError
from facebookads.api import FacebookAdsApi
from facebookads.objects import (AdAccount, Campaign, AdUser, Ad, AdCreative)


def on_success(func):
    @wraps(func)
    def inner_function(self, *args, **kwargs):
        callback = kwargs.pop('on_success', None)
        result = func(self, *args, **kwargs)
        if callback is not None and callable(callback):
            callback(result)
        return result
    return inner_function


def on_failure(func):
    @wraps(func)
    def inner_function(self, *args, **kwargs):
        result = []
        callback = kwargs.pop('on_failure', None)
        try:
            result = func(self, *args, **kwargs)
        except FacebookRequestError as e:
            self.log.error(e.api_error_message(), {'code': e.api_error_code()})
            if callback is not None and callable(callback):
                callback()
        except ValueError as e:
            self.log.error(str(e))

        return result
    return inner_function


class Api:
    def __init__(self, **kwargs):
        self._app_id = kwargs.get('app_id', os.getenv('app_id'))
        self._app_secret = kwargs.get('app_secret', os.getenv('app_id'))
        self._token = kwargs.get('token')
        self.log = kwargs.get('logger', logging)
        self._api = FacebookAdsApi.init(app_id=self._app_id, app_secret=self._app_secret, access_token=self._token)

    def set_token(self, token=None):
        if token is not None and isinstance(token, str):
            self._token = token
        else:
            raise ValueError('Invalid token')

    @on_failure
    @on_success
    def get_accounts(self):
        me = AdUser(fbid='me', api=self._api)
        response = list(me.get_ad_accounts(fields=self.get_class_vars(AdAccount.Field).values()))
        return [account.export_all_data() for account in response]

    @on_failure
    @on_success
    def get_campaigns(self, account_id):
        if not account_id.startswith('act_'):
            raise ValueError('invalid account_id {}'.format(account_id))

        account = AdAccount(str(account_id))
        response = list(account.get_campaigns(fields=self.get_class_vars(Campaign.Field).values()))
        return [campaign.export_all_data() for campaign in response]

    @on_failure
    @on_success
    def get_ads(self, campaign_id=None):
        if campaign_id is None:
            raise ValueError('invalid campaign_id {}'.format(campaign_id))

        campaign = Campaign(fbid=str(campaign_id))
        response = list(campaign.get_ads(fields=self.get_class_vars(Ad.Field).values()))
        ads = []
        for ad in response:
            tmp = None
            creative = list(ad.get_ad_creatives(fields=self.get_class_vars(AdCreative.Field)))
            tmp = ad.export_all_data()
            tmp['creative'] = creative[0].export_all_data() if len(creative) > 0 else tmp['creative']
            ads.append(tmp)

        return ads

    @staticmethod
    def get_class_vars(cls):
        fields = {key: value for key, value in cls.__dict__.items() if not key.startswith('_') and not callable(key)}
        return fields