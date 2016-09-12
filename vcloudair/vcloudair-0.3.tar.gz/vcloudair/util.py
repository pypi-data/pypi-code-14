# coding=utf-8
"""
Description
===========

This is a small utility module where common functions can be stored and
exported from.

"""

__author__ = 'Scott Schaefer'


def check_http_response_error(response):
    """
    Verify that the HTTP request did not return an error.
    If error is returned, raise a runtime exception with the status and
    reason.

    :param response: Requests response object
    :return: None
    :raises: RuntimeError
    """
    if response.status_code >= 400:
        errormsg = '{}, {}\n{}'.format(response.status_code,
                                       response.reason,
                                       response.text)
        raise RuntimeError(errormsg)
