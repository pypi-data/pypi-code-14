#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

# Tyler - a python tail
# Copyright (C) 2016 Davide Mastromatteo - @mastro35


from os import stat


class Tyler(object):
    """
    Creates an iterable object that returns only unread lines.

    Keyword arguments:
    offset_file   File to which offset data is written (default: <logfile>.offset).
    paranoid      Update the offset file every time we read a line (as opposed to
                  only when we reach the end of the file (default: False))
    every_n       Update the offset file every n'th line (as opposed to only when
                  we reach the end of the file (default: 0))
    on_update     Execute this function when offset data is written (default False)
    copytruncate  Support copytruncate-style log rotation (default: True)
    """

    def __init__(self, filename, os_is_windows=False):
        self.filename = filename
        self.offset = 0
        self._fh = None
        self.os_is_windows = os_is_windows
        self.opened_before = False

    def __del__(self):
        if self._fh:
            self._fh.close()

    def __iter__(self):
        return self

    def next(self):
        """
        Return the next line in the file, updating the offset.
        """
        line = None
        try:
            line = self._get_next_line()
        except StopIteration:
            raise

        return line

    def __next__(self):
        """`__next__` is the Python 3 version of `next`"""
        return self.next()

    def _get_next_line(self):
        line = str(self._filehandle().readline(),
                   encoding='utf-8', errors='ignore')
        self.offset = self._fh.tell()
        if not line:
            raise StopIteration
        return line

    def _filehandle(self):
        """
        Return a filehandle to the file being tailed, with the position set
        to the current offset.
        """
        if self._fh:
            size = 0
            try:
                # size = stat(self.filename).st_size
                old_file_position = self._fh.tell()
                self._fh.seek(0, os.SEEK_END)
                size = self._fh.tell()
                self._fh.seek(old_file_position, os.SEEK_SET)
            except Exception:
                size = 0

#            print(size, self.offset)
            if size < self.offset:
                #                print("rolled")

                try:
                    # print(self.offset)
                    # print(size)
                    # print(type(self.offset))
                    # print("close " + self.filename)
                    # time.sleep(5)
                    self._fh.close()
                except Exception:
                    pass

                self._fh = None
                self.offset = 0

        if not self._fh:
            #            print("non esiste")

            filename = self.filename
            # print("open " + filename)

            if self.os_is_windows:
                # self._fh = open(filename, "r", 1)

                import win32file  # Ensure you import the module.
                import msvcrt

                handle = win32file.CreateFile(filename,
                                              win32file.GENERIC_READ,
                                              win32file.FILE_SHARE_DELETE |
                                              win32file.FILE_SHARE_READ |
                                              win32file.FILE_SHARE_WRITE,
                                              None,
                                              win32file.OPEN_EXISTING,
                                              0,
                                              None)
                detached_handle = handle.Detach()
                file_descriptor = msvcrt.open_osfhandle(
                    detached_handle, os.O_RDONLY)

                self._fh = open(file_descriptor, "rb")

            else:
                self._fh = open(filename, "rb")

            if not self.opened_before:
                self.opened_before = True
                my_start_position = 0
                try:
                    my_start_position = stat(self.filename).st_size
                    my_start_position = my_start_position - 4096
                    if my_start_position < 0:
                        my_start_position = 0

                    # print("starting from " + str(my_start_position) )
                except:
                    pass

                self._fh.seek(my_start_position)
                self.offset = self._fh.tell()

        return self._fh


#!/usr/bin/env python

'''
TailAction.py
-------------

Copyright 2016 Davide Mastromatteo
'''

import random
import datetime
import time
import os.path
import re
# from pygtail import Pygtail
from flows.Actions.Action import Action

import flows.Global


class TailAction(Action):
    """
    TailAction Class
    """

    type = "tail"

    path = ""
    my_log_file = None
    file_is_opened = False
    offset_file_name = ""

    enable_buffer = False
    buffer = None
    regex = ""

    #capture_own_messages = True
    #need_warmup = True

    def on_init(self):
        super().on_init()

        # Normal init
        self.path = self.configuration["input"]
        self.buffer = []
        self.timeout = 3
        self.last_flush_date = datetime.datetime.now()

        if "regex_new_buffer" in self.configuration:
            self.regex = self.configuration["regex_new_buffer"]
            self.enable_buffer = True

        if "timeout" in self.configuration:
            self.timeout = int(self.configuration["regex_new_buffer"])

        self.try_opening_file()

    def try_opening_file(self):
        '''Try to open the input file'''
        # read all the file to tail til the end...
        if os.path.isfile(self.path):
            #            print(self.path)
            self.my_log_file = Tyler(self.path, os_is_windows=True)

            try:
                for line in self.my_log_file:
                    # print(line)
                    pass
            except StopIteration:
                pass

            # print("fatto")
            self.file_is_opened = True

    def on_stop(self):
        super().on_stop()
        # for _ in range(0, 5):
        #     try:
        #         os.remove(os.path.join(os.curdir, self.offset_file_name))
        #         break
        #     except Exception:
        #         time.sleep(1)

    def bufferize_line(self, line):
        ''' Insert a new line into the buffer '''
        self.buffer.append(line)

    def flush_buffer(self):
        ''' Flush the buffer of the tail '''
        if len(self.buffer) > 0:
            return_value = ''.join(self.buffer)
            self.buffer.clear()
            self.send_message(return_value)
            self.last_flush_date = datetime.datetime.now()


    def on_cycle(self):
        super().on_cycle()

        # tailing...
        for line in self.my_log_file:
            # print(line)
            # WITHOUT BUFFER:
            if not self.enable_buffer:
                self.send_message(line)
                return

            # WITH BUFFER:
            match = re.search(self.regex, line)

            # if the input line is NOT a new buffer expression no match
            if match is None:
                # bufferize and return
                self.bufferize_line(line)
                return

            # if the input line is the start of a new buffer,
            # flush the buffer and bufferize the new line
            self.flush_buffer()
            self.bufferize_line(line)

        # If there's been something in the buffer for a long time, flush the buffer
        # the default value is 3 seconds
        if (datetime.datetime.now() - self.last_flush_date).total_seconds() > self.timeout:
            self.flush_buffer()
