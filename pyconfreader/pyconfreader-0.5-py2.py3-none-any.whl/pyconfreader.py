#######################################################################
# Loads configuration files written in Python.
#
# Copyright 2011-2016 True Blade Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Notes:
#  There are obviously security implications with running arbitrary
# python scripts as your config files. Only use in appropriate
# situations.
#
#  This code uses a single 'vars' namespace, instead of globals and
# locals for exec-ing into.  This is because, as per the exec docs, at
# module level globals is the same as locals.  And since we're
# executing as modules, that's the behavior we want.

#  to_namedtuple isn't strictly required, but it's used often enough
# with this code (and it's small enough) that I'm including it.
########################################################################

import os
import stat
import types
import collections

__all__ = ['loads', 'load', 'validator_fl_has_uid_gid_mode', 'SimpleFileLoader', 'to_namedtuple']


def loads(s, vars=None, name='<string>', namespace_name=None):
    if vars is None:
        vars = {}

    # call compile() so that errors have a decent context
    code = compile(s, name, 'exec')
    exec(code, vars)

    # delete builtins: the caller will never care about them
    try:
        del vars['__builtins__']
    except KeyError:
        pass

    return vars


def load(fl, vars=None, name=None, namespace_name=None):
    """Load from a file-like object. It is the caller's responsibility
       to close the file."""
    return loads(fl.read(), vars, name, namespace_name)


# define the default namedtuple: ignore modules
def _predicate(key, value):
    return not isinstance(value, types.ModuleType)


def to_namedtuple(dict, type_name='Namespace', predicate=None):
    if predicate is None:
        predicate = _predicate
    # create the namedtuple
    type = collections.namedtuple(type_name, [key for key, value in dict.items() if not key.startswith('_') and predicate(key, value)])
    return type(*[dict[key] for key in type._fields])


def validator_fl_has_uid_gid_mode(owner_uid=None, owner_gid=None, mode_mask=None):
    def validator(fl, filename):
        st = os.fstat(fl.fileno())

        # make sure this is a real file
        if not stat.S_ISREG(st.st_mode):
            raise IOError('{} is not a regular file'.format(filename))

        # make sure it's owned by the right uid, if we care
        if owner_uid is not None:
            if st.st_uid != owner_uid:
                raise IOError('owner of {} is not uid {}'.format(filename, owner_uid))
        if owner_gid is not None:
            if st.st_gid != owner_gid:
                raise IOError('owner of {} is not gid {}'.format(filename, owner_gid))

        # make sure the permissions match what we want
        if mode_mask is not None:
            if st.st_mode & mode_mask != 0:
                raise IOError('{} permissions are too permissive: got {:#o} with extra bits {:#o}'.format(filename, st.st_mode, st.st_mode & mode_mask))

    return validator


class SimpleFileLoader(object):
    '''A simple loader that reads from local files, and has an include() function to load additional files.'''

    def __init__(self, dirname, vars=None, include_fn_name='include', builtins=None, fl_validator=None):
        self.dirname = dirname
        self.fl_validator = fl_validator
        self.vars = vars
        self.include_fn_name = include_fn_name

        if self.vars is None:
            self.vars = {}

        if builtins is not None:
            self.vars['__builtins__'] = builtins

        if self.include_fn_name is not None:
            self.vars[self.include_fn_name] = self._include


    def __call__(self, filename):
        result = self._include(filename)

        # if we added the include function, delete it
        if self.include_fn_name is not None:
            del self.vars[self.include_fn_name]

        return result


    def _include(self, filename):
        fullname = os.path.join(self.dirname, filename)
        with open(fullname) as fl:
            if self.fl_validator is not None:
                self.fl_validator(fl, fullname)
            return load(fl, vars=self.vars, name=filename)
