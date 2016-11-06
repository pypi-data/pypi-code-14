from .exceptions import ConfigValueError
from enum import Enum


class Tasks(Enum):
    pre_tasks = 'pre_tasks'
    tasks = 'tasks'
    post_tasks = 'post_tasks'

MASTER_TASKS = {
    Tasks.pre_tasks.value: {
        "get": ["version"]
    },
    Tasks.tasks.value: {
        "tag": ["docker"],
        "version": ["npm"]
    },
    Tasks.post_tasks.value: {
        "publish": ["npm", "dockerhub"],
        "release": ["versioner", "github"],
        "trigger": ["cd"]
    }
}


def verify_task(task_type, task_input):
    """

    :param task_input:
    :return:
    """
    command_type, command = task_input.split(' ')
    if command in MASTER_TASKS.get(task_type).get(command_type):
        return task_input
    raise ConfigValueError('{} is a bad {} value'.format(task_input, task_type))
