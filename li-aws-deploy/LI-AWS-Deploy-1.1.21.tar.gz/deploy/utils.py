# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, with_statement, nested_scopes
import subprocess


def run_command(command_list, title=None):
    if title:
        print("\n\n>> {}".format(title))
        print("{:*^{num}}".format('', num=len(title) + 3))
    # try:
    for task in command_list:
        if task['run_stdout']:
            new_command = ""
            ret = subprocess.call(
                task['command'].split(" "),
                shell=True,
                stdout=new_command
                )

            if ret != 0:
                print('Ocorreu um erro. Processo abortado')
                return False

            ret = subprocess.call(
                new_command.split(" "),
                shell=True
                )
        else:
            ret = subprocess.call(
                task['command'].split(" "),
                shell=True
                )

        if ret != 0:
            print('Ocorreu um erro. Processo abortado')
            return False

    return True
