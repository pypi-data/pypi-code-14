__author__ = 'marcoantonioalberoalbero'

from queue import Queue
import threading
import datetime
from helpers.logging import Log
from helpers.constants import Constants
import os


class Task:
    def __init__(self, config, name):
        self.parent = None
        self.name = name
        self.finish_status = Constants.CMD_OK
        self.config = config
        self.env = dict(os.environ)
        self.consolidate_only = True if config.get('global', 'log_consolidate_only') == "True" else False
        self.parallel_tasks = Queue()
        self.sequential_tasks = Queue()
        self.id = __name__ + '.' + name
        self.start_time = datetime.datetime.now()
        self.log_file = self.id+'-'+self.start_time.strftime("%Y-%m-%d_%H:%M:%S")+'.log'
        # log to its own file
        self.build_id = os.getenv('MYBICI_BUILD_ID', None)
        self.log = Log().setup(config=config, task_id=self.id, build_id=self.build_id, log_file=self.log_file)

    def is_runnable(self, task):
        op = getattr(task, "run", None)
        if op and callable(op):
            return True
        return False

    def add_task(self, task, sequential=True):
        if self.is_runnable(task):
            task.parent = self
            if sequential:
                self.sequential_tasks.put(task)
            else:
                self.parallel_tasks.put(task)

    def add_env_var(self, key, value):
        self.env[key] = os.path.expandvars(value)
        # set it up in the os environment in order to be passed to the child tasks
        os.environ[key] = os.path.expandvars(value)

    def run(self, result_queue=None, stop_on_error=True):
        parallels = []
        if not self.consolidate_only:
            Log.consolidate_log(task=self, hierarchy_node=self.parent)
        else:
            Log.set_log(self, consolidate_only=True)

        Log.id_log(self.log, "running task " + self.name)
        t_queue = Queue()
        while not self.parallel_tasks.empty():
            task = self.parallel_tasks.get()
            t = threading.Thread(target=task.run, args=[t_queue])
            parallels.append(t)
            t.start()
        while not self.sequential_tasks.empty():
            task = self.sequential_tasks.get()
            task.run()
            if task.finish_status != Constants.CMD_OK:
                self.finish_status = task.finish_status
                if stop_on_error:
                    break
        for t in parallels:
            t.join()
            result = t_queue.get_nowait()
            if result != Constants.CMD_OK:
                self.finish_status = result

        if result_queue:
            result_queue.put(self.finish_status)
        Log.id_log(self.log, "Task " + self.name + " finished with status: " + str(self.finish_status))
        return self.finish_status
