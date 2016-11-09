# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging
import argparse
import warnings

from privacy.util import clean_temp_files

from privacy.console.base import get_main_parser_argv
from privacy.console.base import execute_command_version
from privacy.console.keys import execute_command_list
from privacy.console.keys import execute_command_create
from privacy.console.keys import execute_command_import
from privacy.console.keys import execute_command_show_public
from privacy.console.keys import execute_command_show_private
from privacy.console.keys import execute_command_show_passphrase
from privacy.console.keys import execute_command_show
from privacy.console.keys import execute_command_delete
from privacy.console.crypto import execute_command_encrypt
from privacy.console.crypto import execute_command_decrypt
from privacy.console.crypto import execute_command_sign
from privacy.console.crypto import execute_command_verify
from privacy.console.operations import execute_command_quickstart
from privacy.console.operations import execute_command_wipe
from privacy.console.operations import execute_command_generate_backup
from privacy.console.operations import execute_command_recover_from_backup


warnings.catch_warnings()
warnings.simplefilter("ignore")


def entrypoint():
    handlers = {
        'quickstart': execute_command_quickstart,
        'delete': execute_command_delete,
        'list': execute_command_list,
        'sign': execute_command_sign,
        'show': execute_command_show,
        'create': execute_command_create,
        'import': execute_command_import,
        'decrypt': execute_command_decrypt,
        'verify': execute_command_verify,
        'public': execute_command_show_public,
        'encrypt': execute_command_encrypt,
        'private': execute_command_show_private,
        'version': execute_command_version,
        'passphrase': execute_command_show_passphrase,
        'backup': execute_command_generate_backup,
        'recover': execute_command_recover_from_backup,
        'wipe': execute_command_wipe,
    }
    parser = argparse.ArgumentParser(prog='privacy')
    options = ", ".join(handlers.keys())
    help_msg = 'Available commands:\n\n{0}\n'.format(options)

    parser.add_argument('command', help=help_msg, choices=handlers.keys())

    argv = get_main_parser_argv()

    args = parser.parse_args(argv)

    if args.command not in handlers:
        parser.print_help()
        raise SystemExit(1)

    try:
        clean_temp_files()
    except:
        pass

    try:
        handlers[args.command]()
    except KeyboardInterrupt:
        print "\033[A\r                        "
        print "\033[A\r\rYou hit Control-C. Bye"
        raise SystemExit(1)

    except Exception:
        logging.exception("Failed to execute %s", args.command)
        raise SystemExit(1)


def __main__():
    entrypoint()

if __name__ == '__main__':
    entrypoint()
