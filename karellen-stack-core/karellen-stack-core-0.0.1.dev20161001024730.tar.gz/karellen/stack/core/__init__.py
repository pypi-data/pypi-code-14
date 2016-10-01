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

from urllib.parse import SplitResult, urlsplit, urljoin, parse_qs

to_query_dict = parse_qs  #: Converts a query string component of the Url into a dict


def url(*args, **kwargs):
    """Converts string into a Url"""
    return Url(*urlsplit(*args, **kwargs))


class Url(SplitResult):
    __slots__ = ()

    def __str__(self):
        return self.geturl()

    def as_abs_base(self, relative: 'Url', allow_fragments=True) -> 'Url':
        """Converts ``relative`` url to the absolute, using self as base"""
        return url(urljoin(self.geturl(), relative.geturl(), allow_fragments))


__all__ = ("UrlLoader",
           "ContextUnavailable",
           "InteractiveShellRequired",
           "Provider",
           "OsProvider",
           "OsCloudProvider",
           "PackageProvider")
