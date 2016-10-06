import json
import os
import httplib


class Version:
    def __init__(
            self,
            id="",
            number=0,
            download_url="",
            metadata={},
            created=None,
            modified=None,
            asset=None,
            client=None):
        self.id = id
        self.number = number
        self.download_url = download_url
        self.metadata = metadata
        self.created = created
        self.modified = modified
        self.asset = asset

        self.meta_json = ""
        self.client = client

    def delete(self):
        '''
        delete this version of the asset from ktrlio
        '''
        if not self.asset:
            raise ValueError("cannot delete version with no associated asset")
        if not self.id:
            raise ValueError("cannot delete verison with empty id")
        if not self.client:
            raise RuntimeError(
                "cannot delete version with no associated client")
        # TODO routes should be configured
        resp = self.client.make_request(
            method="DELETE",
            route="/assets/{}/versions/{}".format(self.asset.id, self.id))

        if resp.status == httplib.OK:
            return

        elif resp.status == httplib.NOT_FOUND:
            raise ValueError("cannot delete version: it cannot be found")

        else:
            raise RuntimeError(
                "unhandled error deleting verison ({}): {}".format(
                    resp.status, resp.read()))

    def save_to(self, filepath):
        '''
        saves the associated asset file to the given filepath.
        for the best compatibility, use absolute paths

        Args:
            filepath (str): the location and name to save the asset to
        '''
        dirname = os.path.dirname(filepath)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

        with open(filepath, 'w+') as f:
            data = self.read()
            f.write(data)

    def read(self):
        '''
        read the asset binary data for this version

        Returns:
            the asset object data
        '''
        resp = self.client.make_request(
            method="GET",
            route=self.download_url,
            route_is_abs=True)

        if resp.status == httplib.OK:
            return resp.read()

        elif resp.status == httplib.NOT_FOUND:
            raise ValueError("cannot read, version not found on server")

        else:
            raise RuntimeError(
                "failed to read asset data ({}): {}".format(
                    resp.status, resp.read()))

    def deserialize(self, data):
        '''
        deserialize a data dictionary into this class instance

        Args:
            data (string|dict): raw json or json dict to deserialize
        '''
        if isinstance(data, basestring):
            data = json.loads(data)

        self.id = data["vid"]
        self.number = data["version"]
        self.download_url = data["download_url"]
        self.metadata = data["metadata"]
        self.created = data["created"]
        self.modified = data["modified"]

    def serialize(self):
        '''
        serialize this class into proper json

        Returns:
            a json string
        '''
        return json.dumps({
            "vid": self.id,
            "version": self.number,
            "download_url": self.download_url,
            "metadata": self.metadata,
            "created": self.created,
            "modified": self.modified,
        })


def version_from_json(data, client=None, asset=None):
    '''
    creates a new version instance from the provided json data

    Args:
        data (string|dict): the raw json string or parsed dict object
        client (Client): the client to associate to this version
        asset (Asset): the asset that this version is for
    Returns:
        a new version instance
    '''
    version = Version(client=client, asset=asset)
    version.deserialize(data)
    return version
