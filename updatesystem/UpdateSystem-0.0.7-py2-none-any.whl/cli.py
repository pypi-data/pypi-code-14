
# -*- coding: UTF-8 -*-
import sys
from log import logger as logging

import argparse

def get_parser():
    """
    update system OptParser
    cm command  [args]

    Command:
     install  [--path PATH]  [ --all ]  [ NAME ]
     status
     check  [--path PATH] [--before | --after]
    
    """
    parser = argparse.ArgumentParser(description="""
    this is update system command line
    """, )#usage="%(prog)s [-h] [install|status|check] <args>")


    parser.add_argument('-V','--version',action='version', version="%(prog)s 0.1")
    subparsers = parser.add_subparsers(title="commands", dest="subparser_name")

    parser_install = subparsers.add_parser("install",help="install some patch")

    parser_install.add_argument("--path",help="install path")
    #parser_install_group = parser_install.add_mutually_exclusive_group()
    #parser_install.add_argument("--all",dest="install_all_patch", action="store_true",help="install all patch")
    parser_install.add_argument("patch_name",metavar="PATCH_NAME", nargs="*", default=["ALL"],
            help="install a  patch(default: %(default)s )")

    parser_status  = subparsers.add_parser("status",help="get the system status ")
    parser_check   = subparsers.add_parser("check", help="check the environment")


    parser_check.add_argument("--path",help="install path")
    parser_check_group = parser_check.add_mutually_exclusive_group()

    parser_check_group.add_argument("--before", action="store_true",help="check status before update ")
    parser_check_group.add_argument("--after", action="store_true",help="check status after update ")

    return parser

def get_args_config(parser,args_input):
    """
    传入解析器和参数，获得updatesystem的参数字典
    返回 dict
    """
   
    config = dict()
    config['install'] = False
    config['check'] = False
    config['status'] = False
    
    args = parser.parse_args(args_input)
    logging.debug("get args:{}".format(args))
    if args.subparser_name == "install":
        if args.path is not None:
            config['patch_path'] = args.path
            logging.debug("patch path:{}".format(args.path))
        if args.patch_name == ['ALL']:
            config['install_all'] = True
            config['install'] = True
            logging.info("install all patch")
        elif args.patch_name is not None: 
            config['install'] = True
            config['install_patch'] =  args.patch_name
            logging.info("install patch:{}".format(args.patch_name))
        else:
            logging.error("not option for install command ")
    elif args.subparser_name == "check":
        config['check'] = True
        if args.path is not None:
            config['patch_path'] = args.path
            logging.debug("patch path:{}".format(args.path))
        if args.before:
            logging.info("check before update")
            config["check_time"] = "before"
        elif args.after:
            logging.info("check after update")
            config["check_time"] = "after"
        else:
            config["check_time"] = "after"
            logging.info("default: check after update")
    elif args.subparser_name == "status":
        config['status'] = True
        logging.info("look up status")
    else:
        logging.error("unknown command:{}".format(args.subparser_name))
    logging.debug("config:{}".format(config))
    return config
    


if __name__  == "__main__":
    parser = get_parser()
    a = get_args_config(parser,sys.argv[1:])
    print(a)
else:
    parser = get_parser()

