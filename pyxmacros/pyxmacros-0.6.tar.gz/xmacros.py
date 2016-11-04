#!/usr/bin/env python


import time
from threading import Thread
import os
import sys
import logging
import logging.handlers
import Queue
from glob import glob
from subprocess import PIPE, Popen
from datetime import datetime
from collections import namedtuple
import pyxhook as hooklib
from Xlib import error

class xmacros(object):
    LOGLEVEL = logging.WARN

    MOD_ALT_L = "MOD_ALT_L"
    MOD_ALT_R = "MOD_ALT_R"
    MOD_SHIFT_L = "MOD_SHIFT_L"
    MOD_SHIFT_R = "MOD_SHIFT_R"
    MOD_CTRL_L = "MOD_CTRL_L"

    Action = namedtuple("Action", ["key", "mod", "callback", "time"])

    def __init__(self, log = None, enable_lirc = False):

        self.actions = {}

        if log:
            self.logger = log
        else :
            FORMAT="%(asctime)-15s : %(message)s"
            logHandler = logging.StreamHandler(sys.stdout)
            logHandler.setFormatter(logging.Formatter(FORMAT))
            self.logger = logging.getLogger('log')
            self.logger.addHandler(logHandler)

            self.logger.setLevel(self.LOGLEVEL)

            self.logger.debug("Startup at %s" % str(datetime.now()))


        #############################
        # X Keypress Monitoring

        self.MODS = {
            self.MOD_ALT_L     : [64,  False],
            self.MOD_ALT_R     : [108, False],
            self.MOD_SHIFT_L   : [50,  False],
            self.MOD_SHIFT_R   : [62,  False],
            self.MOD_CTRL_L    : [37,  False],
        }

        self._keyTimer = {}

        self.currentMod = 0
        self.keyPressQueue = Queue.Queue()

        self.xt = Thread(target=self._keepHooksRunningThread)
        self.xt.daemon = True # thread dies with the program
        self.xt.start()

        self.kt = Thread(target=self._monitorKeypressThread)
        self.kt.daemon = True # thread dies with the program
        self.kt.start()


        #############################
        # Lirc Keypress Monitoring

        self.irw_proc = None
        self.irw_thread = None

        if enable_lirc:
            ON_POSIX = 'posix' in sys.builtin_module_names
            self.irw_proc = Popen(['irw'], stdout=PIPE, stdin=PIPE, bufsize=1, close_fds=ON_POSIX)
            self.irw_thread = Thread(target=self._lirc_irw_output, args=(self.irw_proc.stdout,))
            self.irw_thread.daemon = True # thread dies with the program
            self.irw_thread.start()

    def register_action(self, key, callback, mod = None, holdTime = 0):
        if not isinstance(key, int):
            key = str(key).upper() if key is not None else None
        if holdTime:
            holdTime = float(holdTime)
        if mod:
            assert mod in self.MODS

        self.actions[key] = self.Action(key, mod, callback, holdTime)

    def flush(self):
        try:
            while True:
                self.keyPressQueue.get_nowait()
        except Queue.Empty:
            pass

    #############################
    # X Keypress Monitoring

    def _OnKeyDownEvent(self, event, source):
        keypress = {"display": source, "window":event.WindowName, "scancode":event.ScanCode, "ascii":event.Ascii, "key":event.Key, "dir":"down"}
        self.logger.debug("key press: %s"%(str(keypress)))
        self.keyPressQueue.put(keypress)

    def _OnKeyUpEvent(self, event, source):
        keypress = {"display": source, "window":event.WindowName, "scancode":event.ScanCode, "ascii":event.Ascii, "key":event.Key, "dir":"up"}
        self.logger.debug("key press: %s"%(str(keypress)))
        self.keyPressQueue.put(keypress)

    #############################
    # Lirc Keypress Monitoring

    def _lirc_irw_output(self, out):
        for _ in iter(out.readline, b''):
            keypress = str(out) # Needs testing
            self.logger.debug("lirc press: %s" % keypress)
            self.keyPressQueue.put(keypress)

    def _createHookManager(self, disp):
        hm = hooklib.HookManager(disp)
        hm.KeyDown = lambda event: self._OnKeyDownEvent(event, disp)
        hm.KeyUp   = lambda event: self._OnKeyUpEvent(event, disp)
        hm.start()
        return hm

    def _keepHooksRunningThread(self):
        hms = {}
        while True:

            # Check xhooks
            Xservers = {os.path.basename(xf).replace("-lock","").replace(".X", ":") : xf for xf in glob(os.path.join('/', 'tmp','.X*-lock'))}
            for serv in Xservers:
                with open(Xservers[serv], "r") as pidfile:
                    try:
                        pid = int(pidfile.read().strip())
                    except ValueError:
                        pid = -1

                if serv not in hms:
                    hms[serv] = {"pid":pid}
                else:
                    if hms[serv]["pid"] != pid:
                        hms[serv] = {"pid":pid}

            stale = []
            for disp in hms:
                if disp not in Xservers:
                    stale.append(disp)
                else:
                    try:
                        try:
                            if not hms[disp]["hm"].isAlive():
                                raise AttributeError
                        except (AttributeError, KeyError) as ex:
                            time.sleep(1)
                            if hms[disp].get("failed", 0) <= 3:
                                self.logger.info("Starting xhook on display %s" % str(disp))
                                hms[disp]["hm"] = self._createHookManager(disp) # can block indefinitely

                    except error.DisplayConnectionError:
                        if "failed" not in hms[disp]:
                            hms[disp]["failed"] = 1
                        else:
                            hms[disp]["failed"] += 1
                        self.logger.warn("Could not connect to display %s on attempt %d" % (str(disp), hms[disp]["failed"]))

                    except Exception as e:
                        self.logger.critical("Error in xhook on display %s" % str(disp))
                        self.logger.exception(e)
                        time.sleep(5)
            for disp in stale:
                hms.pop(disp)
            time.sleep(10)

    def _CheckMods(self, ScanCode, direction):
        for k,v in self.MODS.iteritems():
            if ScanCode == v[0]:
                if direction == "up":
                    self.MODS[k][1] = False
                elif direction == "down":
                    self.MODS[k][1] = True

    def _runCallback(self, key, callback):
        try:
            try:
                callback(key)
            except TypeError:
                callback()
        except Exception as ex:
            self.logger.exception(ex)
            self.logger.critical("Error running callback for key: %s" % str(key))


    def _monitorKeypressThread(self):
        handle_rate = 0.25
        while True:

            try:
                keyevent = self.keyPressQueue.get()

                WindowName  = keyevent["window"]
                ScanCode    = int(keyevent["scancode"])
                Ascii       = keyevent["ascii"]
                Key         = str(keyevent["key"]).upper()
                direction   = keyevent["dir"]

                self._CheckMods(ScanCode,direction)

                action = None
                if ScanCode in self.actions:
                    action = self.actions[ScanCode]
                elif Key in self.actions:
                    action = self.actions[Key]
                elif None in self.actions:
                    action = self.actions[None]

                if action:
                    if direction == 'up':
                        if ScanCode in self._keyTimer:
                            keyTime = time.time() - self._keyTimer[ScanCode]
                            del self._keyTimer[ScanCode]
                            if action.time and keyTime > action.time:
                                if action.mod:
                                    if self.MODS[action.mod][1]:
                                        self._runCallback(keyevent, action.callback)

                                else:
                                    self._runCallback(keyevent, action.callback)

                    if direction == 'down' and action.callback is not None:
                        if ScanCode not in self._keyTimer:
                            self._keyTimer[ScanCode] = time.time()

                        if not action.time:
                            if action.mod:
                                if self.MODS[action.mod][1]:
                                    self._runCallback(keyevent, action.callback)

                            else:
                                self._runCallback(keyevent, action.callback)

                if direction == 'up':
                    self._keyTimer = {}


            except Queue.Empty:
                time.sleep(handle_rate)

            except KeyboardInterrupt:
                break
            except Exception as e:
                self.logger.exception(e)
                self.logger.critical("exception in xmacros")

