# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import six


def json_to_djorm(data):
    """Return Stripe ORM object from json.

    Wrapper to take a JSON object returned from stripe
    and handle it with an ORM object.

    :param data: JSON data from stripe
    :type data: :class:`dict`
    """
    if not isinstance(data, dict):
        raise TypeError(
            'data Attribute must be a dict'
        )
    if 'object' not in data:
        raise TypeError(
            "JSON data missing object"
        )

    resource_type = data['object']

    Model = get_djorm_model_from_object_key(resource_type)

    return Model


def get_djorm_model_from_object_key(objkey):
    """Return django ORM model from object key.

    :param objkey: "object" key from stripe JSON response
    :type objkey: string
    :returns: Django model from app
    """
    from django.apps import apps

    if not isinstance(objkey, six.text_type):
        raise TypeError(
            "argument must be a string"
        )

    app = apps.get_app_config('stripe_django')
    return app.get_model(objkey)
