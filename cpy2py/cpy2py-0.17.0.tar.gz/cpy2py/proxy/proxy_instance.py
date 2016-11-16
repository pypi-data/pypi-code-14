# - # Copyright 2016 Max Fischer
# - #
# - # Licensed under the Apache License, Version 2.0 (the "License");
# - # you may not use this file except in compliance with the License.
# - # You may obtain a copy of the License at
# - #
# - #     http://www.apache.org/licenses/LICENSE-2.0
# - #
# - # Unless required by applicable law or agreed to in writing, software
# - # distributed under the License is distributed on an "AS IS" BASIS,
# - # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# - # See the License for the specific language governing permissions and
# - # limitations under the License.
import operator

from cpy2py.kernel import kernel_state
from cpy2py.proxy import proxy_tracker
from cpy2py.proxy import proxy_object


class Twinstance(object):
    """
    Twins of an existing instance
    """
    __twin_id__ = None
    __instance_id__ = None
    __kernel__ = None
    __import_mod_name__ = (__module__, None)
    __is_twin_proxy__ = True

    def __new__(cls, obj=None, __twin_id__=None, __instance_id__=None):
        self = object.__new__(cls)
        if obj is not None:
            assert __twin_id__ is None and __instance_id__ is None, \
                "%s received internal and public parameters" % cls.__name__
            object.__setattr__(self, '__twin_id__', kernel_state.TWIN_ID)
            object.__setattr__(self, '__instance_id__', proxy_object.instance_id(self))
            object.__setattr__(self, '__wrapped__', obj)
            object.__setattr__(self, '__is_twin_proxy__', True)
            # register our reference for lookup
        else:
            object.__setattr__(self, '__twin_id__', __twin_id__)
            object.__setattr__(self, '__instance_id__', __instance_id__)
            object.__setattr__(self, '__is_twin_proxy__', False)
        proxy_tracker.__active_instances__[self.__twin_id__, self.__instance_id__] = self
        return self


Twinstance.__import_mod_name__ = (Twinstance.__module__, Twinstance.__name__)