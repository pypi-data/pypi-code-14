# coding: utf-8

import os
import shutil
import tempfile
from logging import error

import sbackup2.utils


def execute_task(task_file, rm_tmp):
    task_conf = sbackup2.utils.read_task_conf(task_file)
    task_options = task_conf.get('options', {})
    tasks = task_conf.get('tasks', [])
    tmp_dir = tempfile.mkdtemp(prefix='sbackup2_')
    tar_file = os.path.join(
        tmp_dir, sbackup2.utils.build_file_name(task_options))

    if not tasks:
        return False

    for task in tasks:
        db_dumps = sbackup2.utils.dump_db(tmp_dir, task.get('db', []))
        fd = task.get('fd', [])

        for item in db_dumps:
            fd.append(item)

        if not fd:
            continue

        if sbackup2.utils.create_tar(tar_file, ' '.join(fd)):
            error('Tar file was not created')

            if not rm_tmp:
                return False

        if sbackup2.utils.sent_file(tmp_dir, task_options, tar_file) != 0:
            error('Tar file was not sent to remote host')

            if not rm_tmp:
                return False

        if rm_tmp:
            shutil.rmtree(tmp_dir)

    return True
