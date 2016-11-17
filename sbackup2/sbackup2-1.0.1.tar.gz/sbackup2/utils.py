# coding: utf-8

import re
import os
import json
import socket
import datetime
import subprocess
from logging import info, warning


def get_task_files(path):
    abs_path = os.path.abspath(path)
    items = os.listdir(abs_path)
    re_conf = re.compile('.+\.conf')
    tasks = []

    for item in items:
        if re_conf.match(item):
            tasks.append(os.path.join(abs_path, item))

    return tasks


def read_task_conf(path):
    try:
        with open(path, 'r') as f:
            conf = json.load(f)
    except FileNotFoundError:
        return {}

    return conf


def build_file_name(task_options):
    dt = datetime.datetime.now()

    d = {
        'host_name': socket.gethostname(),
        'year': dt.strftime('%Y'),
        'month': dt.strftime('%m'),
        'day': dt.strftime('%d'),
        'hour': dt.strftime('%H'),
        'minutes': dt.strftime('%M'),
        'seconds': dt.strftime('%S'),
    }

    try:
        file_name = task_options['file_name_tpl']
    except ValueError:
        info('Option \'file_name_tpl\' not found, using default a file name for'
             ' an archive')
        file_name = '{host_name}_{year}_{month}_{day}__{hour}_{minutes}' \
                    '_{seconds}.tar.bz2'

    return file_name.format(**d)


def mysql_dump(tmp_dir, db):
    dump_file = os.path.join(tmp_dir, db) + '.sql'
    command = 'mysqldump {db} > {dump_file}'.format(db=db, dump_file=dump_file)

    exit_code = sub_process(command)

    if exit_code == 0:
        return dump_file
    else:
        # todo: same action
        warning('DB \'{db}\' was not back up, return code {code}'.format(
            db=db, code=exit_code))

    raise RuntimeError


def dump_db(tmp_dir, dbs):
    dump_files = []

    for db in dbs:
        db_type = db.pop(0)
        db_name = db.pop()

        if db_type == 'mysql':
            try:
                dump_files.append(mysql_dump(tmp_dir, db_name))
            except RuntimeError:
                continue

        elif db_type == 'psql':
            pass

        else:
            warning('Unknown DB \'{db_type}\''.format(db_type=db_type))
            continue

    return dump_files


def sub_process(command):
    return subprocess.call(
        command, shell=True, stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL)


def create_tar(tar_file, fd_str):
    command = 'tar jcf {} {}'.format(tar_file, fd_str)

    return sub_process(command)


def file_ask(tmp_dir, archive, backup_dir):
    f = os.path.join(tmp_dir, 'sftp_command')

    with open(f, 'w') as file:
        file.write('cd {}\n'.format(backup_dir))
        file.write('put {}\n'.format(archive))
        file.write('quit\n')

    return f


def sent_file(tmp_dir, options, file_name):
    sftp_file_ask = file_ask(tmp_dir, file_name, options.get('sftp_remote_dir'))

    options.update({'sftp_conf': sftp_file_ask})

    command = 'sshpass -p {sftp_password} sftp {sftp_options} -b {sftp_conf} ' \
              '{sftp_user}@{sftp_host}'.format(**options)

    r = sub_process(command)
    os.remove(sftp_file_ask)
    return r
