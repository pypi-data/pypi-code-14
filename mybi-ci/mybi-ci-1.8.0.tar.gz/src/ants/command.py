__author__ = 'marcoantonioalberoalbero'

import os
import subprocess
import datetime
from helpers.valdano import Log


class Command:
    def __init__(self, config, name):
        self.parent = None
        self.name = name
        self.config = config
        self.consolidate_only = True if config.get('global', 'log_consolidate_only') == "True" else False
        self.command = None
        self.finish_status = None
        self.env = dict(os.environ)
        self.id = __name__ + '.' + name
        self.start_time = datetime.datetime.now()
        self.log_file = self.id + '-' + self.start_time.strftime("%Y-%m-%d_%H:%M:%S") + '.log'
        # log to its own file
        self.build_id = os.getenv('MYBICI_BUILD_ID', None)
        self.log = Log().setup(config=config, task_id=self.id, build_id=self.build_id, log_file=self.log_file)

    def set_command(self, command):
        self.command = command

    def add_env_var(self, key, value):
        self.env[key] = os.path.expandvars(value)

    def run(self, result_queue=None):
        if not self.consolidate_only:
            Log.consolidate_log(task=self, hierarchy_node=self.parent)
        else:
            Log.set_log(self, consolidate_only=True)

        Log.id_log(self.log, "running command " + self.command)
        result = subprocess.Popen(self.command,
                                  shell=True,
                                  env=self.env,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,
                                  universal_newlines=True)

        # Poll process for new output until finished
        while True:
            line = result.stdout.readline()
            self.finish_status = result.poll()
            if isinstance(self.finish_status, int) and not line:
                break
            Log.id_log(self.log, line)
        if result_queue:
            result_queue.put(self.finish_status)
        Log.id_log(self.log, "Task " + self.name + " finished with status: " + str(self.finish_status))
        return self.finish_status
