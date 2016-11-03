#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest
import os
import time
import shutil
import tarfile
import tempfile
import reusables
import subprocess
import logging

log = reusables.get_logger('tasking')


class ExampleSleepTasker(reusables.Tasker):

    @staticmethod
    def perform_task(task, queue):
        time.sleep(task)
        queue.put(task)


class ExampleAddTasker(reusables.Tasker):

    @staticmethod
    def perform_task(task, queue):
        queue.put(task, task + task)

tasker = ExampleAddTasker(list(range(100)))
log.info("about to start")
log.info(tasker.get_state())
tasker.run()
time.sleep(0.1)
tasker.change_task_size(1)
log.info(tasker.get_state())
for i in range(100):
    log.info(tasker.result_queue.get())
tasker.stop()
