from .exceptions import Ahoyhoy500Exception


def raise_for_status(resp):
    """
    Classify a 500 response as a Ahoyhoy500Exception
    """
    if 500 <= resp.status_code < 600:
        http_error_msg = '%s Server Error: %s for url: %s' % (resp.status_code, resp.reason, resp.url)
        raise Ahoyhoy500Exception(http_error_msg, response=resp)
    else:
        return resp
