#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file is part of store_pypeline.
# https://github.com/rfloriano/store-pypeline

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2014 Rafael Floriano da Silva rflorianobr@gmail.com

import json
import os
import sys
import re

import exec_pypeline
from store_pypeline import store


class Pipeline(exec_pypeline.Pipeline, store.Store):
    action_list = None

    def __init__(self, action_list=None, pipeline=None, stdout=None, stderr=None):
        self.pipeline = pipeline
        if pipeline is None:
            self.pipeline = json.loads(os.environ.get('PIPELINE', 'null'))
            if self.pipeline is None:
                self.pipeline = []

        if stdout is None:
            stdout = sys.stdout

        if stderr is None:
            stderr = sys.stderr

        self.stdout = stdout
        self.stderr = stderr
        exec_pypeline.Pipeline.__init__(
            self, action_list or self.action_list,
            before_action=self.before_action,
            after_action=self.after_action,
            before_forward=self.before_forward,
            before_backward=self.before_backward
        )
        store.Store.__init__(self, self.stdout, self.stderr)
        self._init_actions()
        self.notify_actions()
        self._failed_action = None
        self._failed_err = None

    def _init_actions(self):
        for action in self.action_list:
            action.initialize(self.stdout, self.stderr)

    def before_forward(self, act, ctx):
        self.log(u'Running action - {0}'.format(act.name))

    def before_backward(self, act, ctx):
        self.log(u'Rolling back - {0}'.format(act.name))
        error = act.to_dict().get('error', {})
        if error:
            self.log(error.get('traceback'))

    def actions_to_dict(self, *args, **kwargs):
        actions = super(Pipeline, self).actions_to_dict(*args, **kwargs)
        return self.pipeline + actions

    def before_action(self, act, ctx, exception):
        self.notify_actions()

    def after_action(self, act, ctx, exception):
        self.notify_actions()

    def notify_actions(self):
        self.stdout.write(json.dumps(self.actions_to_dict()) + '\n')
        self.stdout.flush()
