import os
import time
import re

from pypicloud_client.http import request_factory


class PypicloudError(Exception):
    """Exception raised by a failed on the pypicloud api"""


class PypicloudClient(object):
    """Pypicloud API client, the client can e set ny environment variables.

    Args:
        kwargs (dict) :
            user (str): User for basic authentication
            password (str): Password for basic authentication
            host (str): Pypicloud host

    """
    def __init__(self, **kwargs):
        self.host = kwargs.get("host", os.environ.get("PYPICLOUD_HOST", None))
        self.auth = (
            kwargs.get("user", os.environ.get("PYPICLOUD_USER", None)),
            kwargs.get("password", os.environ.get("PYPICLOUD_PASSWORD", None))
        )

        if self.host is None:
            raise ValueError("host have to be set, not equal to {0}".format(self.host))

        if None in self.auth:
            raise ValueError("auth have to be set, not equal to {0}".format(self.auth))

    def get_versions(self, package, sort_by=None, desc=True, filters=None, strict=True, exclude=False, limit=None):
        """Get the wheel versions of an package, ordered by date from most recent to least recent.

        Args:
            package: Package whose versions to get
            sort_by: Sort the output by a field
            desc: Ordering the output list
            filters: Provide a key-value pair to filter the versions
            strict: strict matching, True by default
            exclude: If True, excludes the matches of the filters
            limit: Return a certain number of results

        Returns:
            list of dict: List of package info.
        """
        endpoint = "/api/package/{package}/".format(package=package)
        versions = request_factory(self.host, "GET", endpoint, auth=self.auth)
        pkg_versions = versions["packages"]
        if filters:
            if exclude:
                pkg_versions = [pkg for pkg in pkg_versions if not all(re.search(value, pkg[key])
                    for key, value in filters.items())]
            elif strict:
                pkg_versions = [pkg for pkg in pkg_versions if set(filters.items()).issubset(set(pkg.items()))]
            else:
                pkg_versions = [pkg for pkg in pkg_versions if all(re.search(value, pkg[key])
                    for key, value in filters.items())]
        sort_key = sort_by if sort_by else "last_modified"
        return sorted(pkg_versions, key=lambda pkg: pkg[sort_key], reverse=desc)[:limit]

    def delete_package(self, package, version, retries=30, sleep=3):
        """Delete package ona specific version

            Args:
                package (str): the package name
                version (str): the package version to delete
        """
        target = dict()

        for pkg in self.get_versions(package):
            if pkg["version"] == version:
                target = pkg


        try:
            endpoint = "api/package/{0}/{1}".format(package, target["filename"])
        except KeyError:
            return None


        for _ in xrange(retries):
            resp = request_factory(self.host, "DELETE", endpoint, auth=self.auth)
            if not any([_ for pkg in self.get_versions(package) if pkg["version"] == version]):
                return resp

            time.sleep(sleep)

        raise PypicloudError("The delete package failed, check your cache backend or pypicloud logs")
