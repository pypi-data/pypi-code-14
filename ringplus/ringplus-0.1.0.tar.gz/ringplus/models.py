"""Models for returned RingPlus objects."""

from __future__ import absolute_import
from __future__ import print_function

import iso8601

from ringplus.error import RingPlusError


class ResultSet(list):
    """A list like object that holds results from a RingPlus API query."""
    def __init__(self, max_id=None, since_id=None):
        super(ResultSet, self).__init__()
        self._max_id = max_id
        self._since_id = since_id

    @property
    def max_id(self):
        if self._max_id:
            return self._max_id
        ids = self.ids()
        # Max id is always set to the *smallest* id, minus one,. in the set
        return (min(ids) - 1) if ids else None

    @property
    def since_id(self):
        if self._since_id:
            return self._since_id
        ids = self.ids()
        # Since_id is always set to the *greatest id in the set
        return max(ids) if ids else None

    def ids(self):
        return [item.id for item in self if hasattr(item, 'id')]


class Model(object):

    def __init__(self, api=None):
        self._api = api

    def __getstate__(self):
        # pickle
        pickle = dict(self.__dict__)
        try:
            del pickle['_api']  # do not pickle the API reference
        except KeyError:
            pass
        return pickle

    def __repr__(self):
        state = ['%s=%s' % (k, repr(v)) for (k, v) in vars(self).items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(state))

    @classmethod
    def parse(cls, api, json):
        """Parse a JSON object into a model instance."""
        service = cls(api)
        setattr(service, '_json', json)
        for k, v in json.items():
            setattr(service, k, v)
        return service

    @classmethod
    def parse_list(cls, api, json_list):
        """ Parse a list of JSON objects into result set of model instances."""
        if isinstance(json_list, list):
            item_list = json_list
        else:
            raise RingPlusError("Cannot parse list: %s" % json_list)

        results = ResultSet()
        for obj in item_list:
            results.append(cls.parse(api, obj))
        return results


# Account Classes

class Account(Model):
    """Object that encapsulates a mobile device on a plan.

    Accounts are the object that encapsulate a mobile device on a plan.
    They belong to a User and are a base model for many other routes on
    the API.
    """

    @classmethod
    def parse(cls, api, json):
        if 'account' in json:
            account = Account.parse(api, json['account'])
        else:
            account = cls(api)
            setattr(account, '_json', json)
            for k, v in json.items():
                if k.endswith('_on'):
                    setattr(account, k, iso8601.parse_date(v))
                elif k == 'account_services':
                    setattr(account, k, AccountService.parse_list(api, v))
                elif k == 'active_device':
                    setattr(account, k, ActiveDevice.parse(api, v))
                elif k == 'voicemail_box':
                    setattr(account, k, VoicemailBox.parse(api, v))
                elif 'billing_subscriptions' in k:
                    setattr(account, k, BillingSubscription.parse_list(api, v))
                else:
                    setattr(account, k, v)
        return account

    @classmethod
    def parse_list(cls, api, json_list):
        if isinstance(json_list, list):
            item_list = json_list
        else:
            item_list = json_list['accounts']

        results = ResultSet()
        for obj in item_list:
            results.append(cls.parse(api, obj))
        return results


class AccountService(Model):
    """Account Service Object."""

    pass


class ActiveDevice(Model):
    """Active Device Object."""

    @classmethod
    def parse(cls, api, json):
        device = cls(api)
        setattr(device, '_json', json)
        for k, v in json.items():
            if k == 'registered_on':
                setattr(device, k, iso8601.parse_date(v))
            else:
                setattr(device, k, v)
        return device


class BillingSubscription(Model):
    """Billing Subscription Object."""

    @classmethod
    def parse(cls, api, json):
        subscr = cls(api)
        setattr(subscr, '_json', json)
        for k, v in json.items():
            if 'date' in k or k.endswith('at'):
                setattr(subscr, k, iso8601.parse_date(v))
            else:
                setattr(subscr, k, v)
        return subscr


# User Classes

class User(Model):
    """Base object for a user on the system.

    User accounts are the base object representing a user on the system.
    You can view and update various properties of users, and use User IDs to
    query many other objects in the system.
    """

    @classmethod
    def parse(cls, api, json):
        if 'user' in json:
            user = User.parse(api, json['user'])
        else:
            user = cls(api)
            setattr(user, '_json', json)
            for k, v in json.items():
                if k == 'accounts':
                    setattr(user, k, Account.parse_list(api, v))
                elif k == 'registered_on':
                    setattr(user, k, iso8601.parse_date(v))
                else:
                    setattr(user, k, v)
        return user

    @classmethod
    def parse_list(cls, api, json_list):
        if isinstance(json_list, list):
            item_list = json_list
        else:
            item_list = json_list['users']

        results = ResultSet()
        for obj in item_list:
            results.append(cls.parse(api, obj))
        return results


# Calls, Texts, and Data

class Call(Model):
    """Phone Call Model."""

    @classmethod
    def parse(cls, api, json):
        call = cls(api)
        setattr(call, '_json', json)
        for k, v in json.items():
            if k == 'start_time':
                setattr(call, k, iso8601.parse_date(v))
            else:
                setattr(call, k, v)
        return call

    @classmethod
    def parse_list(cls, api, json_list):
        if isinstance(json_list, list):
            item_list = json_list
        else:
            item_list = json_list['phone_calls']

        results = ResultSet()
        for obj in item_list:
            results.append(cls.parse(api, obj))
        return results


class Text(Model):
    """Phone Text Model."""

    @classmethod
    def parse(cls, api, json):
        text = cls(api)
        setattr(text, '_json', json)
        for k, v in json.items():
            if k == 'occurred_at':
                setattr(text, k, iso8601.parse_date(v))
            else:
                setattr(text, k, v)
        return text

    @classmethod
    def parse_list(cls, api, json_list):
        if isinstance(json_list, list):
            item_list = json_list
        else:
            item_list = json_list['phone_texts']

        results = ResultSet()
        for obj in item_list:
            results.append(cls.parse(api, obj))
        return results


class Data(Model):
    """Phone Data Model."""

    @classmethod
    def parse(cls, api, json):
        data = cls(api)
        setattr(data, '_json', json)
        for k, v in json.items():
            if k == 'occurred_at':
                setattr(data, k, iso8601.parse_date(v))
            else:
                setattr(data, k, v)
        return data

    @classmethod
    def parse_list(cls, api, json_list):
        if isinstance(json_list, list):
            item_list = json_list
        else:
            item_list = json_list['phone_data']

        results = ResultSet()
        for obj in item_list:
            results.append(cls.parse(api, obj))
        return results


# Voicemail Classes

class Voicemail(Model):
    """Voicemail object."""

    @classmethod
    def parse(cls, api, json):
        voicemail = cls(api)
        setattr(voicemail, '_json', json)
        for k, v in json.items():
            if k == 'received_on':
                    setattr(voicemail, k, iso8601.parse_date(v))
            else:
                setattr(voicemail, k, v)
        return voicemail

    @classmethod
    def parse_list(cls, api, json_list):
        if isinstance(json_list, list):
            item_list = json_list
        else:
            item_list = json_list['voicemail_messages']

        results = ResultSet()
        for obj in item_list:
            results.append(cls.parse(api, obj))
        return results


class VoicemailBox(Model):
    """Voicemail Box Object."""

    pass


# Request Status

class Request(Model):
    """Object for all status messages of different requests."""

    @classmethod
    def parse(cls, api, json):
        for k, v in json.items():
            if k in ('phone_number_change_request',
                     'device_change_request',
                     'account_registration_request'):
                request = Request.parse(api, json[k])
        else:
            request = cls(api)
            setattr(request, '_json', json)
            for k, v in json.items():
                if k == 'requested_on':
                    setattr(request, k, iso8601.parse_date(v))
                elif k == 'account':
                    setattr(request, k, Account.parse(api, v))
                else:
                    setattr(request, k, v)
        return request

    @classmethod
    def parse_list(cls, api, json_list):
        """ Parse a list of JSON objects into result set of model instances."""
        if isinstance(json_list, list):
            item_list = json_list
        else:
            item_list = [json_list]

        results = ResultSet()
        for obj in item_list:
            results.append(cls.parse(api, obj))
        return results


# Enforced Carrier Service

class CarrierService(Model):
    """Object for Enforced Carrier Services."""

    @classmethod
    def parse_list(cls, api, json_list):
        if isinstance(json_list, list):
            item_list = json_list
        else:
            item_list = json_list['enforced_carrier_services']

        results = ResultSet()
        for obj in item_list:
            results.append(cls.parse(api, obj))
        return results


# Fluid Call

class FluidCall(Model):
    """Object for fluid call credentials."""

    @classmethod
    def parse(cls, api, json):
        call = cls(api)
        setattr(call, '_json', json)
        for k, v in json.items():
            if k.endswith('_at'):
                setattr(call, k, iso8601.parse_date(v))
            else:
                setattr(call, k, v)
        return call

    @classmethod
    def parse_list(cls, api, json_list):
        if isinstance(json_list, list):
            item_list = json_list
        else:
            item_list = json_list['fluidcall_credentials']

        results = ResultSet()
        for obj in item_list:
            results.append(cls.parse(api, obj))
        return results


# Utility Classes

class JSONModel(Model):

    @classmethod
    def parse(cls, api, json):
        return json


class IDModel(Model):

    @classmethod
    def parse(cls, api, json):
        if isinstance(json, list):
            return json
        else:
            return json['ids']


class ModelFactory(object):
    """Used by parsers for creating instances of models.

    You may subclass this factory to add your own extended models.
    """

    user = User
    account = Account
    voicemail = Voicemail
    call = Call
    text = Text
    data = Data
    request = Request

    voicemailbox = VoicemailBox
    active_device = ActiveDevice
    account_service = AccountService
    billing_subscription = BillingSubscription
    fluidcall = FluidCall
    carrier_service = CarrierService

    json = JSONModel
    id = IDModel
