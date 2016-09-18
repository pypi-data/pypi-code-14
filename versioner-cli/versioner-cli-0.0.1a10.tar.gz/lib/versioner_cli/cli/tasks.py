MASTER_TASKS = {
    "pre_tasks": {
        "get": []
    },
    "tasks": {
        "tag": ["docker"],
        "version": ["npm"]
    },
    "post_tasks": {
        "publish": ["npm", "dockerhub"],
        "release": ["versioner", "github"]
    }
}


def verify_task(task_input):
    """

    :param task_input:
    :return:
    """
    task_type, command = task_input.split(' ')
    if task_type in MASTER_TASKS.keys():
        if command in MASTER_TASKS.get(task_type):
            return True
    return False
