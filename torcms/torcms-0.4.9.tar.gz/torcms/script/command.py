# -*- coding: utf-8 -*-

import sys, getopt

from .script_migrate import run_migrate
from .get_category import run_gen_category
from .script_init_database_shema import run_init_tables
from .script_update_count import run_update_count
from .script_sendemail_all import run_send_all, run_send_nologin
from .script_edit_diff import run_edit_diff

def entry(argv):
    try:
        # 这里的 h 就表示该选项无参数，i:表示 i 选项后需要有参数
        opts, args = getopt.getopt(argv, "hi:")
    except getopt.GetoptError:
        print ('Error: helper.py -i cmd')
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print ('helper.py -i cmd')
            print ('cmd list----------------------')
            print ('       migrate: ')
            print ('     edit_diff: ')
            print ('  gen_category: ')
            print ('   init_tables: ')
            print ('  update_count: ')
            print ('      send_all: ')
            print ('  send_nologin: ')
            sys.exit()
        elif opt in ("-i"):
            helper_app = arg
            eval('run_' + helper_app + '()')
