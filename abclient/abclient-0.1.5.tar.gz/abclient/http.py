#    Copyright (c) 2016 Shanghai EISOO Information Technology Corp.
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json

from oslo_log import log as logging
import requests


LOG = logging.getLogger(__name__)
USER_AGENT = "karbor-AnyBackupclient"


class HTTPClient(object):
    def __init__(self, endpoint, **kwargs):
        self.endpoint_url = endpoint
        self.timeout = 1200

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
            kwargs["data"] = json.dumps(kwargs["data"])

        resp = self._http_request(method, url, **kwargs)
        body = resp.content

        if body and resp.status_code != 204:
            try:
                body = resp.json()
            except ValueError:
                LOG.error("Could not decode response body as JSON")
                raise
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
        except Exception:
            LOG.error(('HTTP request failed. url : %s.'),
                      self.endpoint_url+url)
            raise

        LOG.info("URL: %(url)s \n"
                 "Response status code %(status_code)s",
                 {"url": self.endpoint_url + url,
                  "status_code": resp.status_code})
        return resp
