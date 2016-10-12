#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import asyncio
from bubble.bserver import interface, watcher


class BubbleWorker:
    def __init__(self):
        self.startedTimestamp = time.time()
        self.killed = False
        self.runLocally = False
        self.waxsWatcher = watcher.Watcher(interface.Iwaxs())
        self.saxsWatcher = watcher.Watcher(interface.Isaxs())
        self.pardict = {
            'kill': self.kill,
            'state': self.state,
            'saxs': self.saxs,
            'waxs': self.waxs,
        }

    def saxs(self, request):
        return self.setIntegrator(request, self.saxsWatcher)

    def waxs(self, request):
        return self.setIntegrator(request, self.waxsWatcher)

    # noinspection PyUnusedLocal
    def kill(self, request=None):
        loop = asyncio.get_event_loop()
        loop.call_soon(self.saxsWatcher.stopWatching)
        loop.call_soon(self.waxsWatcher.stopWatching)
        loop.call_later(0.5, loop.stop)
        self.killed = True
        return {}

    # noinspection PyUnusedLocal
    def state(self, request=None):
        return {
            'server': self.stateServer(),
            'saxs': self.stateSAXS(),
            'waxs': self.stateWAXS(),
        }

    def stateSAXS(self):
        state = self.saxsWatcher.state()
        if self.killed:
            state['running'] = False
        return state

    def stateWAXS(self):
        state = self.waxsWatcher.state()
        if self.killed:
            state['running'] = False
        return state

    def stateServer(self):
        return {
            'startedTimestamp': self.startedTimestamp,
            'killed': self.killed,
        }

    def setIntegrator(self, params, watcherObject):
        watcherObject.setParameters(params)
        state = {}
        if watcherObject.errors:
            state['errors'] = watcherObject.errors
        if watcherObject.warnings:
            state['warnings'] = watcherObject.warnings
        return state

    def parse(self, request):
        state = {}
        for key in request:
            if key in self.pardict:
                state.update(self.pardict[key](request[key] if key in request else None))
        return state

    def resetSent(self):
        self.waxsWatcher.resetSent()
        self.saxsWatcher.resetSent()
