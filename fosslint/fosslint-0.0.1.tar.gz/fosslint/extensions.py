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
class Extension:
    def __init__(self, path, opt):
        pass

    def find_header_end(self, lines):
        """
        Find which line number (zero-based) that the license header ends at.
        """
        return 0

    def render_header_comment(self, lines):
        for line in lines:
            yield line


class Java(Extension):
    def __init__(self, path, opt):
        self.path = path
        self.opt = opt

    def find_header_end(self, lines):
        for i, line in enumerate(lines):
            if i == 0:
                if not line.startswith('/**'):
                    return i

            if line.startswith(' *'):
                continue

            if line == ' **/':
                return i + 1

        return 0

    def render_header_comment(self, lines):
        yield u"/**"

        for line in lines:
            yield u" * " + line.rstrip()

        yield " **/"


class Python(Extension):
    def __init__(self, path, opt):
        self.path = path
        self.opt = opt

    def find_header_end(self, lines):
        for i, line in enumerate(lines):
            if not line.startswith('#'):
                return i

        return 0

    def render_header_comment(self, lines):
        for line in lines:
            s = line.rstrip()

            if len(s) == 0:
                yield u"#"
            else:
                yield u"# " + s


EXTENSIONS = {}
EXTENSIONS['.py'] = Python
EXTENSIONS['.java'] = Java

def load_extension(ext, path, opt):
    try:
        ext = EXTENSIONS[ext]
    except KeyError:
        ext = Extension

    return ext(path, opt)
