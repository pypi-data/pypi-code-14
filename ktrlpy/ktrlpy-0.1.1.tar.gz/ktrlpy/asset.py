import json
import httplib
import re

from .version import version_from_json


class Asset:
    def __init__(self, id="", client=None):
        self.id = id
        self.client = client

    def update(self, metadata, data=None):
        '''
        update this asset, creating a new version

        Args:
            metadata: the json serializable object to use as the new metadata
            data (file): the actual binary asset data to upload to the server
        Returns:
            the new version that was created
        '''
        if not self.id:
            raise ValueError("cannot update asset with empty id")
        if not self.client:
            raise RuntimeError("cannot update asset with no associated client")

        method = "PUT"
        if data is None:
            method = "PATCH"

        # TODO routes should be configured
        resp = self.client.make_multipart_asset_request(
            method=method,
            route="/assets/" + self.id,
            metadata=metadata,
            data=data)

        if resp.status == httplib.OK:
            pass
        else:
            raise RuntimeError(
                "unhandled update asset status code({}): {}".format(
                    resp.status, resp.read()))

        return version_from_json(resp.read())

    def versions(self):
        '''
        fetched a list of all versions of this asset

        Returns:
            a list of versions
        '''
        if not self.id:
            raise ValueError("cannot get versions, asset has empty id")
        if not self.client:
            raise ValueError("asset has no associated client")

        versions = []
        next_page = self.client.get_request_url(
            "/assets/{}/versions".format(self.id))
        link_re = re.compile('<(.*)>; rel="next"')

        while next_page:

            resp = self.make_request("GET", next_page, route_is_abs=True)

            version_data = json.loads(resp.read())
            for data in version_data:
                v = version_from_json(data)
                versions.append(v)

            m = link_re.match(resp.getheader("Link", ""))
            if m:
                next_page = m.group(1)
            else:
                next_page = None

        return versions

    def latest(self):
        '''
        fetches the latest version of this asset
        note that this data is never cached and repeated calls will
        invoke repeated network requests

        Returns:
            the latest Version instance for this asset
        '''
        if not self.id:
            raise ValueError("cannot get versions, asset has empty id")
        if not self.client:
            raise ValueError("asset has no associated client")

        # TODO routes should be configured
        resp = self.client.make_request(
            method="GET",
            route="/assets/" + self.id)

        body = resp.read()

        if resp.status == httplib.OK:
            return version_from_json(body, client=self.client, asset=self)

        elif resp.status == httplib.NOT_FOUND:
            raise RuntimeError("cannot get latest version, asset not found")

        else:
            raise RuntimeError(
                "cannot get latest version ({}): {}".format(resp.status, body))

    def delete(self):
        '''
        delete this asset, a psudonym for asset.client.delete_asset(asset.id)
        '''
        self.client.delete_asset(self.id)

    def deserialize(self, data):
        '''
        deserialize a data dictionary into this class instance

        Args:
            data (string|dict): raw json or json dict to deserialize
        '''
        if isinstance(data, basestring):
            data = json.loads(data)

        self.id = data["id"]

    def serialize(self):
        '''
        serialize this class into proper json

        Returns:
            a json string
        '''
        return json.dumps({
            "id": self.id
        })


def asset_from_json(data, client=None):
    '''
    creates a new asset instance from the provided json data

    Args:
        data (string|dict): the raw json string or parsed dict object
        client (Client): the client to associate to this asset
    Returns:
        a new asset instance
    '''
    asset = Asset(client=client)
    asset.deserialize(data)
    return asset
