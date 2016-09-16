#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file is part of store_pypeline.
# https://github.com/rfloriano/store-pypeline

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2014 Rafael Floriano da Silva rflorianobr@gmail.com

import exec_pypeline
from store_pypeline import store


class Action(exec_pypeline.Action, store.ActionStore):
    def __init__(self, name=None, *args, **kwargs):
        if name is not None:
            self.name = name
        exec_pypeline.Action.__init__(self, *args, **kwargs)
        store.Store.__init__(self, *args, **kwargs)

    def to_dict(self):
        data = exec_pypeline.Action.to_dict(self)
        data.update(store.ActionStore.to_dict(self))
        return data
