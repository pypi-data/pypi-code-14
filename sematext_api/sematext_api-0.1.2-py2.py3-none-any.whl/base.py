#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Sematext API
# Copyright (c) 2008-2016 Hive Solutions Lda.
#
# This file is part of Hive Sematext API.
#
# Hive Sematext API is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Sematext API is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Sematext API. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2016 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import json

import appier

BASE_URL = "https://logsene-receiver.sematext.com/"
""" The default base url to be used when no other
base url value is provided to the constructor """

class Api(
    appier.Api
):

    def __init__(self, *args, **kwargs):
        appier.Api.__init__(self, *args, **kwargs)
        self.token = appier.conf("SEMATEXT_TOKEN", None)
        self.base_url = kwargs.get("base_url", BASE_URL)
        self.token = kwargs.get("token", self.token)
        self._build_url()

    def log(self, type, payload, silent = True):
        url = self.token_url + type
        contents = self.post(url, data_j = payload, silent = silent)
        return contents

    def log_bulk(self, type, logs, silent = True):
        url = self.base_url + "_bulk"
        buffer = []
        header = {
            "index" : {
                "_index" : self.token,
                "_type" : type
            }
        }
        header_s = json.dumps(header)
        header_s = appier.legacy.bytes(header_s, encoding = "utf-8")
        for log in logs:
            log_s = json.dumps(log)
            log_s = appier.legacy.bytes(log_s, encoding = "utf-8")
            buffer.append(header_s)
            buffer.append(log_s)
        data = b"\n".join(buffer)
        contents = self.post(url, data = data, silent = silent)
        return contents

    def _build_url(self):
        self.token_url = "%s%s/" % (self.base_url, self.token)
