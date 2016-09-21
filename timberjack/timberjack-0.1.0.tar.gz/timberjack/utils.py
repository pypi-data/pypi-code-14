# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

ANONYMOUS_USER = 'anonymous'


def get_username_from_request(request):
    """
    Extract the username from the *request*.

    Looks up the username for the user associated with the *request* and returns
    it. This requires a logged in user. If the request has an anonymous user
    `anonymous` is returned.

    Args:
        request: A Django request.

    Returns:
        A string corresponding to the username of the user making this request
        or the string `anonymous` if no logged in user can be found.
    """
    try:
        user = request.user
    except AttributeError:
        return ANONYMOUS_USER

    if user.is_authenticated():
        return user.username

    return ANONYMOUS_USER


def get_client_ip(request):
    """
    Get the client IP address from the *request* object.

    Looks up the IP address that sent the *request* by checking the
    `HTTP_X_FORWARDED_FOR` header or `REMOTE_ADDR` in the request's metadata.

    Args:
        request: a Django request.

    Returns:
        An IP address as a string or an empty string if no IP could be found.
    """
    client_ip = request.META.get("HTTP_X_FORWARDED_FOR", '')

    try:
        # X_FORWARDED_FOR returns client1, proxy1, proxy2,...
        client_ip = client_ip.split(',')[0]
    except IndexError:
        pass

    if not client_ip:
        client_ip = request.META.get('REMOTE_ADDR', '')

    return client_ip.strip()
