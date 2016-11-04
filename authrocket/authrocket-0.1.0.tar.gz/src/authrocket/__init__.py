"""
AuthRocket API client
"""

import urlparse

import requests
import uritemplate

class HeaderProperty(object):
    """
    Header value proxy for a `requests.Session` object.
    """

    def __init__(self, header_name):
        self.header_name = header_name

    def __get__(self, instance, owner=None):
        if not instance:
            raise AttributeError()
        return instance.headers.get(self.header_name, None)

    def __set__(self, instance, value):
        if not instance:
            raise AttributeError()
        instance.headers[self.header_name] = value

class API(requests.Session):
    """
    AuthRocket API client.

    Behaves like a `requests.Session`, but:
        * Sets auth headers.
        * Uses `url` as a root URL.

    Examples:
        * `authrocket = AuthRocket("http://authrocket", "my-account", "my-api-key")`
        * `response = authrocket.get("orgs")`
        * `response = authrocket.post("users/authenticate_key", json={"key": "user-api-key"})``


    ## URI templates

    AuthRocket takes some parameters via the path, e.g "users/{username}".
    To support this style, URI template support is provided via the `variables`
    arg.

    Example:
        response = authrocket.get("users/{username}", variables={"username": "my-user"})

    For security reasons, URI templates are strongly recommended over string
    interpolation.
    """

    def __init__(self, url, key, realm_id=None):
        super(API, self).__init__()

        self.url = url
        self.key = key

        if realm_id:
            self.realm_id = realm_id

    def request(self, method, url, *args, **kwargs):
        """
        Request a URL. Overloads `requests.request` as mentioned in the class
        docstring.
        """

        variables = kwargs.pop("variables", None)
        if variables is not None:
            url = uritemplate.expand(url, variables)

        url = urlparse.urljoin(self.url.rstrip("/") + "/", url)

        return super(API, self).request(method, url, *args, **kwargs)

    def iter_from_pages(self, *args, **kwargs):
        """
        Yields each item from an API, iterating through pages if available.

        Takes the parameters normally passed to `request`, e.g:

            for org in authrocket.iter_from_pages("GET", "org"):
                print org
        """

        kwargs.setdefault("params", {})
        after = None
        while True:
            kwargs["params"]["after"] = after

            response = self.request(*args, **kwargs)
            if response.status_code != 200:
                raise Exception("Expected HTTP {} from {}, but received {}".format(
                    200, response.status_code, response.url
                ))
            data = response.json()

            for item in data["collection"]:
                after = item["id"]
                yield item

            if not data["more_results"]:
                break

    key = HeaderProperty("X-Authrocket-Api-Key")
    realm_id = HeaderProperty("X-Authrocket-Realm")
