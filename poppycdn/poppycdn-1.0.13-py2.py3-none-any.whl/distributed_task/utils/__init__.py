# Copyright (c) 2015 Rackspace, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import importlib


def exc_loader(exc_class):
    """Exception Loader

    Creates of the instance of the specified
    exception class given the fully-qualified name.
    The module is dynamically imported.

    """

    pos = exc_class.rfind('.')
    module_name = exc_class[:pos]
    class_name = exc_class[pos + 1:]

    mod = importlib.import_module(module_name)
    return getattr(mod, class_name)
