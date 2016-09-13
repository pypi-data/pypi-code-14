from tornado.web import HTTPError


def unwrap_items(response, *, single_item=False, columns=None):
    """
    Project response items always comeback in a list
    even when they are GETs for an ID. Single Item tells
    this unwrapper that you're expecting a single item out.
    """
    try:
        # Dont know the resource name but should be the only key
        assert len(response) == 1
        resources = list(response.values())[0]

        if single_item and len(resources) != 1:
            ValueError('More then one resource was returned.')

        resources = [
            {k: v for k, v in r.items() if not columns or k in columns}
            for r in resources]

        return resources[0] if single_item else resources
    except (AssertionError, KeyError):
        unwrap_error(response)


def unwrap_error(zoho_error):
    try:
        # Dont know the error name but should ony be one key left
        code        = zoho_error['error']['code']
        message     = zoho_error['error']['message']
        status_code = http_status_code(zoho_code=code)

        raise HTTPError(status_code, reason=message)
    except (AssertionError, KeyError, IndexError):
        raise ValueError("Couldn't parse zoho result")


def http_status_code(*, zoho_code):  # pragma: no cover
    zoho_code = str(zoho_code)

    if zoho_code in [6401, 6891, 6403, 6831, 6832, 6500]:  # noqa
        return 400  # bad request
    elif zoho_code in [6401, 6890]:
        return 401  # unauthorised
    elif zoho_code in [6504, 6404]:
        return 404  # not found
    else:
        return 500  # internal server error
