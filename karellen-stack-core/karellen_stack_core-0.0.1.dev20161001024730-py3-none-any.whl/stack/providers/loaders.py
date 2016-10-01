#
#  -*- coding: utf-8 -*-
#
# (C) Copyright 2016 Karellen, Inc. (http://karellen.co/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import hashlib
import os.path

from karellen.stack.core import to_query_dict
from karellen.stack.core.spi import UrlLoader, Url
from karellen.stack.utils import inherit_doc


@inherit_doc
class FileUrlLoader(UrlLoader):
    def __init__(self, context, source, base=None):
        super().__init__(context, source, base)

    def _resolve(self):
        abs_url = self.absolute

        path = abs_url.path
        path = os.path.realpath(path)
        hash = hashlib.sha256()

        with open(path, "rb") as f:
            hash.update(f.read(65535))

        self._version = hash.hexdigest()
        self._canonical_url = Url(scheme=abs_url.scheme, netloc=abs_url.netloc, path=path, query=abs_url.query,
                                  fragment=abs_url.fragment)

    def _stream(self, url):
        q_dict = {k: v[0] for k, v in to_query_dict(url.query).items()}
        options = {}
        if "mode" in q_dict:
            options["mode"] = q_dict["mode"]

        return open(url.path, **options)

    def _content(self, url):
        with self._stream(url) as f:
            return f.read()
