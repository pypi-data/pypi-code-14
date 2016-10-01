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

from voluptuous import Schema, Required, Optional

from karellen.stack.core.schema.validation import IdName, List, Include, UrlValidator

ID_NAME = IdName()

EXTENSION = {
    ID_NAME: {
        Required("extension"): str,
        Required("plugin"): str,
        Optional("dependencies"): List(UrlValidator())
    }
}

MINIMAL_SCHEMA_STACK_CORE = Schema({
    Optional("inherit"): Include(),
    Optional("include"): List(Include()),
    Optional("extensions"): EXTENSION,
    Optional("config"): dict
})

INHERIT_JSON_SCHEMA = {}
INCLUDE_JSON_SCHEMA = {}
