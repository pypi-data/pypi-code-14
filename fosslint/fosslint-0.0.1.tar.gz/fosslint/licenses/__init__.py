# Copyright (c) 2013-2016 Spotify AB
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import pkg_resources

class License:
    def __init__(self, full, header):
        self.full = full
        self.header = header


class LicenseInstance:
    def __init__(self, full, header):
        self.full = full
        self.header = header

    def render_full(self, **kw):
        for line in self.full:
            yield line.format(**kw)

    def render_header(self, **kw):
        for line in self.header:
            yield line.format(**kw)


LICENSES = {}

LICENSES['Apache 2.0'] = License('apache_2.0.txt', 'apache_2.0_header.txt')


def read_license(path):
    content = pkg_resources.resource_string(__name__, path).decode('utf-8')
    content = content.split(u'\n')

    if len(content) > 0:
        content = content[:-1]

    return content


def load_license(key):
    try:
        license = LICENSES[key]
    except KeyError:
        raise Exception('Unsupported license (' + key + ')')

    full = read_license(license.full)
    header = read_license(license.header)

    return LicenseInstance(full, header)
