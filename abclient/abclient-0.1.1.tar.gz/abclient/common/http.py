from six.moves import http_cookiejar
import socket

from oslo_log import log as logging
from oslo_serialization import jsonutils
import requests

from abclient.common import exception as exc

LOG = logging.getLogger(__name__)
USER_AGENT = "karbor-AnyBackupclient"


class HTTPClient(object):
    def __init__(self, endpoint, **kwargs):
        self.endpoint_url = endpoint
        self.cookie = http_cookiejar.CookieJar()
        self.timeout = 1200

    def _construct_json_header(self):
        self.headers = {
            "Connection": "keep-alive",
            "Content-Type": "application/json"
        }

    def json_request(self, method, url, **kwargs):
        kwargs.setdefault("headers", {})
        kwargs['headers'].setdefault("Content-Type", "application/json")

        if "body" in kwargs:
            if "data" in kwargs:
                raise ValueError("Can't provide both 'data' and "
                                 "'body' to a request")
            LOG.warning("Use of 'body' is deprecated; use 'data' instead")
            kwargs["data"] = kwargs.pop("body")
        if "data" in kwargs:
            kwargs["data"] = jsonutils.dumps(kwargs["data"])

        resp = self._http_request(method, url, **kwargs)
        body = resp.content

        if body and resp.status_code != 204:
            try:
                body = resp.json()
            except ValueError:
                LOG.error("Could not decode response body as JSON")
                body = "Invalid-JSON"
        else:
            body = None

        return body

    def _http_request(self, method, url, **kwargs):
        kwargs["headers"].setdefault("User-Agent", USER_AGENT)
        kwargs.setdefault("verify", False)
        if self.timeout is not None:
            kwargs["timeout"] = float(self.timeout)

        try:
            resp = requests.request(method, self.endpoint_url + url, **kwargs)
        except socket.gaierror as e:
            message("Error finding address for %(url)s: %(e)s" %
                    {"url": self.endpoint_url + url,
                     'e': e})
            raise exc.EndpointException(message)
        except (socket.error, socket.timeout,
                requests.exceptions.ConnectionError) as e:
            endpoint = self.endpoint_url
            message = ("Error communicating with %(endpoint)s %(e)s" %
                       {'endpoint': endpoint,
                        'e': e})
            raise exc.ConnectionRefused(message)

        LOG.info("URL: %(url)s \n"
                 "Response status code %(status_code)s",
                 {"url": self.endpoint_url + url,
                  "status_code": resp.status_code})
        return resp


def _construct_http_client(*args, **kwargs):
    return HTTPClient(*args, **kwargs)
