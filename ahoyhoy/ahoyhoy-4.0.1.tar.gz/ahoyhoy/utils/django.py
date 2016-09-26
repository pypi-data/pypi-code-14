"""
All Django-related stuff goes here.
"""

import logging


logger = logging.getLogger(__name__)


def _pre_process_header_name(header_name):
    """
    Convert HTTP headers names according to the Django docs.

    There's no way to access Django headers directly,
    only through the request META keys, see:
    https://code.djangoproject.com/ticket/20147

    request.META contains both HTTP headers and other META keys.
    Non-HTTP META keys are described here:
    http://wsgi.readthedocs.io/en/latest/definitions.html

    From Django docs 
    (https://docs.djangoproject.com/en/1.9/ref/request-response/#django.http.HttpRequest.META)
    
    "With the exception of CONTENT_LENGTH and CONTENT_TYPE,
    as given above, any HTTP headers in the request are converted to META keys
    by converting all characters to uppercase,
    replacing any hyphens with underscores and adding an HTTP_ prefix to the name.
    So, for example, a header called X-Bender would be mapped to the META key 
    HTTP_X_BENDER."
    """
    
    # Standard WSGI supported headers
    _wsgi_headers = ["REQUEST_METHOD", "SCRIPT_NAME", "PATH_INFO",
                     "QUERY_STRING", "CONTENT_TYPE", "CONTENT_LENGTH",
                     "SERVER_NAME", "SERVER_PORT", "SERVER_PROTOCOL",
                     "REMOTE_ADDR", "REMOTE_HOST", "REMOTE_USER"]

    logger.debug("Input header name: %s", header_name)
    header_name = header_name.upper().replace('-', '_')
    logger.debug("Converted header name: %s", header_name)
    
    if header_name not in _wsgi_headers:
        header_name = "HTTP_{header}".format(header=header_name)
        logger.debug("Add HTTP_ prefix to the header name: %s", header_name)
        return header_name.upper()
    else:
        return header_name


def get_headers(request, headers_names_lst):
    """
    Extract headers from the request.
    :param request: HttpRequest object
    :param headers_names_lst: list or tuple with names of headers to extract
    :return: dictionary with headers and their values
    :rtype dict:
    """

    headers_dict = {}

    for header_name in headers_names_lst:
        logger.debug("Looking for the header '%s'", header_name)
        header_val = request.META.get(
            _pre_process_header_name(header_name)
        )
        if header_val:
            logger.debug("Extracting header from the request: '%s': '%s'",
                        header_name, header_val)
            headers_dict[header_name] = header_val
        else:
            logger.debug("Header %s wasn't found in request headers: %s",
                        header_name, request.META)

    return headers_dict


def get_cookies(request, cookies_names_lst):
    """
    Extract cookies from the request.
    :param request: HttpRequest object
    :param cookies_names_lst: list or tuple with names of cookies to extract
    :return: dictionary with cookies and their values
    :rtype dict:
    """
    cookies_dict = {}
    
    for cookie_name in cookies_names_lst:
        logger.debug("Looking for the cookie '%s'", cookie_name)
        cookie_val = request.COOKIES.get(cookie_name)
        if cookie_val:
            logger.debug("Extracting cookie from the request: '%s': '%s'",
                        cookie_name, cookie_val)
            cookies_dict[cookie_name] = cookie_val
        else:
            logger.debug("Cookie %s wasn't found in request cookies: %s",
                        cookie_name, request.COOKIES)

    return cookies_dict
