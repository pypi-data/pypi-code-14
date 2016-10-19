__author__ = 'marcoantonioalberoalbero'
from helpers.task import Task
from ants.command import Command
from helpers.env import read_config
from validators.json_validator import JsonValidator
from validators.tasks_schema import TasksSchema
from helpers.valdano import Log
import json
import os
import uuid


class Loader:

    env = read_config()
    logger = Log().setup(config=env, task_id=__name__)

    @staticmethod
    def load_from_file(file):
        try:
            with open(file) as data_file:
                build = json.load(data_file)
                task = Loader.build_root_task(build)
                if not task:
                    Log.id_log(Loader.logger, "Build file format not valid (" + file + ")")
                return task
        except json.decoder.JSONDecodeError:
            Log.id_log(Loader.logger, file + ": JSON not valid.")

    @staticmethod
    def build_root_task(build):
        result = JsonValidator.validate(build, TasksSchema.schema)
        if result['valid'] is True:
            os.environ['MYBICI_BUILD_ID'] = str(uuid.uuid1())
            Log.id_log(Loader.logger, "Loading build '" + build["build"] + "'")
            task = Loader.load(build["starter"])
            Log.id_log(Loader.logger, "Load of '" + build["build"] + "' [OK], BUILD ID: " + os.environ['MYBICI_BUILD_ID'])
            return task
        return None

    @staticmethod
    def load(json_data):
        if "cmd" in json_data:
            result = Loader.load_command(json_data)
        else:
            result = Loader.load_task(json_data)
        return result

    @staticmethod
    def load_task(json_data):
        task = Task(Loader.env, json_data["id"])
        if "env" in json_data:
            for entry in json_data["env"]:
                for k in entry.keys():
                    task.add_env_var(k, entry[k])
        if "parallel_tasks" in json_data:
            for t in json_data["parallel_tasks"]:
                if Loader.is_command(t):
                    task.add_task(Loader.load_command(t), sequential=False)
                else:
                    task.add_task(Loader.load_task(t), sequential=False)
        if "sequential_tasks" in json_data:
            for t in json_data["sequential_tasks"]:
                if Loader.is_command(t):
                    task.add_task(Loader.load_command(t))
                else:
                    task.add_task(Loader.load_task(t))
        return task

    @staticmethod
    def load_command(json_data):
        cmd = Command(Loader.env, json_data["id"])
        if "env" in json_data:
            for entry in json_data["env"]:
                for k in entry.keys():
                    cmd.add_env_var(k, entry[k])
        if "cmd" in json_data:
            cmd.set_command(json_data["cmd"])
        return cmd

    @staticmethod
    def is_command(json_data):
        if "cmd" in json_data:
            return True
        else:
            return False
