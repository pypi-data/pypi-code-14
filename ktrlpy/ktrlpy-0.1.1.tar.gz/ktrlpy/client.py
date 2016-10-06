from urlparse import urlparse
import httplib
import ssl
import re
import json

from .multipart import encode_multipart_formdata
from .asset import (Asset, asset_from_json)
from .errors import (
    AuthenticationError, NotFoundError
)


class Client():
    '''
    Client is the main interface for connecting to ktrl.io
    and using its api. The Client manages the connection to ktrl.io
    '''

    def __init__(
            self,
            base_url,
            auth_method,
            api_version=1,
            insecure_skip_verify=False):
        '''
        create a new instance of the Client class

        Args:
            base_url (str): valid url denoting the base url to use in
                making requests to ktrl.io (https://example.com/)
            auth_method (object): a ktrl.io auth method such as UserInfo or
                APIKey. Basically this is an object with an auth(client) method
            api_version (int): optional api version number to use (default=1)
            insecure_skip_verify (bool): if true, do not validate the servers
                certificate (only safe for testing locally)(default=False)
        Returns:
            new Client instance
        '''

        self.token_data = None
        self.token_raw = ""

        # parse and validate the base url
        parsed = urlparse(base_url)
        if not parsed.scheme or not parsed.hostname:
            raise ValueError("invalid base_url provided")
        self.base_url = base_url
        self.api_version = api_version
        self.insecure_skip_verify = insecure_skip_verify

        if parsed.scheme == "https":
            # default ssl context for now
            context = ssl.create_default_context()
            if insecure_skip_verify:
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE

            # create the connection we will use
            self.__connection = httplib.HTTPSConnection(
                host=parsed.hostname,
                port=parsed.port,
                context=context)

        else:
            self.__connection = httplib.HTTPConnection(
                host=parsed.hostname,
                port=parsed.port)

        # allow direct access to request / response on this connection
        self.request = self.__connection.request
        self.getresponse = self.__connection.getresponse

        # authenticate the client before returning a success
        if not auth_method:
            raise ValueError("auth_method must be provided")
        if not hasattr(auth_method, "auth") or not callable(auth_method.auth):
            raise ValueError("auth_method has no callable auth method")
        err = auth_method.auth(self)
        if err:
            raise err

    def token_claims(self):
        '''
        returns the claims dictionary from the clients json web token
        '''
        return self.token_data

    def get_request_url(self, route):
        '''
        build the request url based on the way this client is configured

        Args:
            route (str): the api route the request will be for
        Returns:
            the url string
        '''
        return "{}/api/v{}{}".format(self.base_url, self.api_version, route)

    def make_request(self, method, route, body="", route_is_abs=False):
        '''
        performs a request, calling the ktrlio api, setting
        proper headers etc

        Args:
            method (string): the http method for the request
            route (string): the api route to call
            body (object): the body of the request to send
            route_is_abs (bool): if true, the route is not appended to
                                 the client base_url
        Raises:
            AuthenticationError: when client has not been initialized
        '''
        if not self.token_data:
            raise AuthenticationError(
                "client has not been authenitcated")

        url = route
        if not route_is_abs:
            url = self.get_request_url(route)

        self.__connection.request(
            method,
            url,
            body,
            {"X-Auth-Token": self.token_raw})

        return self.getresponse()

    def make_multipart_asset_request(
            self, method, route, metadata, data=None):
        '''
        builds and makes a multipart asset request based on the given data
        '''
        if not self.token_data:
            raise AuthenticationError(
                "client has not been authenitcated")

        url = self.get_request_url(route)

        if not isinstance(metadata, basestring):
            metadata = json.dumps(metadata)
        fields = {
            "meta": metadata
        }

        files = {}
        if data is not None:
            files["object"] = ("", data)

        content_type, body = encode_multipart_formdata(fields, files)

        headers = {
            "Content-Type": content_type,
            "X-Auth-Token": self.token_raw,
            "Content-Length": len(str(body))
        }

        self.request(method, url, body, headers)
        return self.getresponse()

    def create_asset(self, metadata, data):
        '''
        create and return a new asset

        Args:
            metadata (string|dict): json string or json-serializable object
                                    to server as the metadata
            data (file): the actual binary asset data to upload to the server
        Returns:
            the new asset instance
        '''
        # TODO routes should be configured
        resp = self.make_multipart_asset_request(
            method="PUT",
            route="/assets",
            metadata=metadata,
            data=data)

        if resp.status == httplib.OK:
            return asset_from_json(resp.read(), client=self)
        else:
            raise RuntimeError(
                "unhandled create asset status code({}): {}".format(
                    resp.status, resp.read()))

    def asset_by_id(self, id):
        '''
        attempts to get an asset from the ktrlio server by id

        Args:
            id (string): the id of the asset to request
        Returns:
            an Asset object
        Raises:
            ValueError: if provided id is empty or falsy
            NotFoundError: if the server returns 404 on the asset id
        '''
        if not id:
            raise ValueError("cannot get asset, id is empty")

        # TODO routes should be configured
        resp = self.make_request("GET", "/assets/{}".format(id), None)

        if resp.status == httplib.OK:
            asset = Asset("", self)
            asset.deserialize(json.loads(resp.read()))
            return asset
        elif resp.status == httplib.NOT_FOUND:
            raise NotFoundError(
                "asset with id {} does not exist".format(id))
        else:
            raise RuntimeError(
                "unhandled asset by id status code({}): {}".format(
                    resp.status, resp.read()))

    def delete_asset(self, id):
        '''
        deletes the asset with the given id

        Args:
            id (str): the id of the asset to delete
        '''
        if not id:
            raise ValueError("supplied id cannot be empty")

        resp = self.make_request(
            method="DELETE",
            route="/assets/" + id,
            body=None)

        body = resp.read()

        if resp.status == httplib.OK:
            return
        elif resp.status == httplib.NOT_FOUND:
            raise ValueError("cannot delete asset, it does not exist")
        else:
            raise RuntimeError(
                "error deleting asset({}): {}".format(resp.status, body))

    def asset_list(self):
        '''
        requests a list of all assets from the ktrl.io servers

        Returns:
            tuple list of assets
        '''
        assets = []
        next_page = self.get_request_url("/assets")
        link_re = re.compile('<(.*)>; rel="next"')

        while next_page:

            resp = self.make_request("GET", next_page, route_is_abs=True)

            asset_data = json.loads(resp.read())
            for data in asset_data:
                a = asset_from_json(data, client=self)
                assets.append(a)

            m = link_re.match(resp.getheader("Link", ""))
            if m:
                next_page = m.group(1)
            else:
                next_page = None

        return assets
